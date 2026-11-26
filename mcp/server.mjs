#!/usr/bin/env node
/**
 * Motion Index — Standalone Zero-Dependency stdio MCP Server
 *
 * Implements JSON-RPC 2.0 over stdio (initialize, tools/list, tools/call):
 *   1. search_motions(query, pattern?, trigger?, feel?, stack?, app?, limit?)
 *   2. get_motion_code(id, stack?, designTokens?)
 *   3. extract_motion(url?, videoUrl?, stack?, notes?)
 *
 * Environment variables:
 *   MOTION_INDEX_API_KEY     API key (mi_live_... or mi_test_...)
 *   MOTION_INDEX_API_URL     Base URL (default: https://ai-motion-database.netlify.app; set "local" to force local catalog)
 *   MOTION_INDEX_LOCAL_ONLY  Set "1" to run purely against the local repository catalog without network calls
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..');

const SERVER_INFO = {
  name: 'motion-index',
  version: '1.0.0',
};
const PROTOCOL_VERSION = '2024-11-05';

const API_URL = (process.env.MOTION_INDEX_API_URL || 'https://ai-motion-database.netlify.app').replace(/\/+$/, '');
const API_KEY = (process.env.MOTION_INDEX_API_KEY || '').trim();
const LOCAL_ONLY = process.env.MOTION_INDEX_LOCAL_ONLY === '1' || API_URL.toLowerCase() === 'local';

const TOOLS = [
  {
    name: 'search_motions',
    description:
      'Search the Motion Index UI motion library by query, pattern (use case), trigger, feel, stack, or app. Free and public discovery returning compact matches, IDs, and preview URLs.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Free-text search query (e.g. "progress bar", "spring card", "shader", "Duolingo")' },
        pattern: { type: 'string', description: 'Use-case pattern (e.g. "Micro-interactions", "Navigation and layout", "Typography", "Transitions", "Backgrounds", "Generative")' },
        trigger: { type: 'string', description: 'Trigger type (e.g. "Click", "Hover", "Drag", "Loop", "Tab switch", "Cursor", "Ambient")' },
        feel: { type: 'string', description: 'Motion feel (e.g. "Playful", "Crisp", "Fluid", "Calm", "Tactile", "Silky", "Editorial", "Cinematic")' },
        stack: { type: 'string', description: 'Source stack (e.g. "CSS", "SVG", "Canvas 2D", "WebGL")' },
        app: { type: 'string', description: 'App name or slug (e.g. "duolingo", "linear", "spotify", "apple-wallet")' },
        limit: { type: 'number', description: 'Max results to return (1-50, default 12)' },
      },
      required: ['query'],
    },
  },
  {
    name: 'get_motion_code',
    description:
      'Fetch Motion IR, extractable code, choreography beats, and stack-specific adaptation instructions (CSS, React/Motion, GSAP, SwiftUI, Remotion) for a motion ID. Automatically enforces Team Brand Motion Tokens from your API key or optional designTokens.',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'Motion ID returned by search_motions (e.g. "app-duolingo-progress-surge")' },
        stack: { type: 'string', description: 'Target stack: "CSS", "React/Motion", "GSAP", "SwiftUI", or "Remotion"' },
        designTokens: {
          type: 'object',
          description: 'Optional Brand Motion Token overrides enforced on the Motion IR and adaptation prompt',
          properties: {
            brandName: { type: 'string' },
            springStiffness: { type: 'number' },
            springDamping: { type: 'number' },
            durationScale: { type: 'number' },
            bezierCurve: { type: 'array', items: { type: 'number' } },
            reducedMotionPolicy: { type: 'string', enum: ['respect', 'crossfade', 'instant'] },
          },
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'extract_motion',
    description:
      'Queue a custom motion extraction job from a live web URL or video URL. Requires Pro (30/mo), Teams (150/mo), or API Credits (10 credits/job).',
    inputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string', description: 'Public http(s) URL of a web page with the target motion' },
        videoUrl: { type: 'string', description: 'Public http(s) URL of an MP4/MOV/WebM recording' },
        stack: { type: 'string', description: 'Target output stack (default "React/Motion")' },
        notes: { type: 'string', description: 'Optional instructions describing which interaction to capture' },
      },
    },
  },
];

/* ---------- Local repo fallback loader ---------- */
let localModulesPromise = null;

async function loadLocalModules() {
  if (localModulesPromise) return localModulesPromise;
  localModulesPromise = (async () => {
    const catalogFile = path.join(REPO_ROOT, 'netlify', 'functions', 'lib', 'catalog.mjs');
    const codeHandlerFile = path.join(REPO_ROOT, 'netlify', 'functions', 'api-motion-code.mjs');
    const extractHandlerFile = path.join(REPO_ROOT, 'netlify', 'functions', 'api-extract.mjs');
    const motionsJsonFile = path.join(REPO_ROOT, 'data', 'motions.json');

    if (fs.existsSync(catalogFile) && fs.existsSync(motionsJsonFile)) {
      const [catalogMod, codeMod, extractMod] = await Promise.all([
        import(pathToFileURL(catalogFile).href),
        import(pathToFileURL(codeHandlerFile).href),
        import(pathToFileURL(extractHandlerFile).href),
      ]);
      return {
        mode: 'repo-handlers',
        searchMotions: catalogMod.searchMotions,
        motionCodeHandler: codeMod.default,
        extractHandler: extractMod.default,
      };
    }
    return null;
  })();
  return localModulesPromise;
}

/* ---------- Remote REST API client with clean local fallback ---------- */
async function callRemoteJson(endpointPath, options = {}) {
  const url = `${API_URL}${endpointPath}`;
  const headers = {
    Accept: 'application/json',
    ...(options.body ? { 'Content-Type': 'application/json' } : {}),
    ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
  };

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 12000);
  try {
    const res = await fetch(url, {
      method: options.method || 'GET',
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: controller.signal,
    });
    const text = await res.text();
    let json;
    try {
      json = JSON.parse(text);
    } catch {
      throw new Error(`Non-JSON response from ${url} (HTTP ${res.status})`);
    }
    return { ok: res.ok, status: res.status, data: json };
  } finally {
    clearTimeout(timer);
  }
}

function asToolOutput(payload, isError = false) {
  return {
    content: [
      {
        type: 'text',
        text: typeof payload === 'string' ? payload : JSON.stringify(payload, null, 2),
      },
    ],
    ...(isError ? { isError: true } : {}),
  };
}

async function execSearchMotions(args = {}) {
  if (!LOCAL_ONLY) {
    try {
      const qs = new URLSearchParams();
      if (args.query) qs.set('q', String(args.query));
      if (args.pattern) qs.set('use', String(args.pattern));
      if (args.trigger) qs.set('trigger', String(args.trigger));
      if (args.feel) qs.set('feel', String(args.feel));
      if (args.stack) qs.set('stack', String(args.stack));
      if (args.app) qs.set('app', String(args.app));
      qs.set('limit', String(Math.min(50, Math.max(1, Number(args.limit) || 12))));

      const res = await callRemoteJson(`/api/v1/motions?${qs.toString()}`);
      if (res.ok) return asToolOutput(res.data, false);
    } catch {
      // Fall through to local catalog when offline or running in local repo
    }
  }

  const local = await loadLocalModules();
  if (!local) {
    return asToolOutput(
      { error: `Could not reach ${API_URL}/api/v1/motions and no local data/motions.json fallback was found.` },
      true
    );
  }

  const result = local.searchMotions(
    {
      q: args.query || '',
      use: args.pattern,
      trigger: args.trigger,
      feel: args.feel,
      stack: args.stack,
      app: args.app,
      limit: Math.min(50, Math.max(1, Number(args.limit) || 12)),
    },
    LOCAL_ONLY ? 'https://ai-motion-database.netlify.app' : API_URL
  );
  return asToolOutput({ ...result, source: 'local-catalog' }, false);
}

async function execGetMotionCode(args = {}) {
  if (!args.id) {
    return asToolOutput({ error: 'Argument "id" is required.' }, true);
  }

  if (!LOCAL_ONLY) {
    try {
      const res = await callRemoteJson(`/api/v1/motions/${encodeURIComponent(args.id)}/code`, {
        method: 'POST',
        body: {
          id: args.id,
          stack: args.stack,
          designTokens: args.designTokens,
        },
      });
      return asToolOutput(res.data, !res.ok);
    } catch {
      // Fall through to local catalog handler
    }
  }

  const local = await loadLocalModules();
  if (!local) {
    return asToolOutput(
      { error: `Could not reach ${API_URL}/api/v1/motions/${args.id}/code and no local repo fallback was found.` },
      true
    );
  }

  const headers = new Headers({ 'Content-Type': 'application/json' });
  if (API_KEY) headers.set('Authorization', `Bearer ${API_KEY}`);
  const req = new Request(`https://ai-motion-database.netlify.app/api/v1/motions/${encodeURIComponent(args.id)}/code`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      id: args.id,
      stack: args.stack,
      designTokens: args.designTokens,
    }),
  });
  const res = await local.motionCodeHandler(req);
  const data = await res.json();
  return asToolOutput({ ...data, source: 'local-catalog' }, !res.ok);
}

async function execExtractMotion(args = {}) {
  if (!args.url && !args.videoUrl) {
    return asToolOutput({ error: 'Provide either "url" or "videoUrl".' }, true);
  }

  if (!LOCAL_ONLY) {
    try {
      const res = await callRemoteJson('/api/v1/extract', {
        method: 'POST',
        body: {
          url: args.url,
          videoUrl: args.videoUrl,
          stack: args.stack,
          notes: args.notes,
        },
      });
      return asToolOutput(res.data, !res.ok);
    } catch {
      // Fall through to local handler
    }
  }

  const local = await loadLocalModules();
  if (!local) {
    return asToolOutput(
      { error: `Could not reach ${API_URL}/api/v1/extract and no local repo fallback was found.` },
      true
    );
  }

  const headers = new Headers({ 'Content-Type': 'application/json' });
  if (API_KEY) headers.set('Authorization', `Bearer ${API_KEY}`);
  const req = new Request('https://ai-motion-database.netlify.app/api/v1/extract', {
    method: 'POST',
    headers,
    body: JSON.stringify({
      url: args.url,
      videoUrl: args.videoUrl,
      stack: args.stack,
      notes: args.notes,
    }),
  });
  const res = await local.extractHandler(req);
  const data = await res.json();
  return asToolOutput({ ...data, source: 'local-catalog' }, !res.ok);
}

/* ---------- JSON-RPC 2.0 dispatcher ---------- */
async function handleRequest(msg) {
  if (!msg || msg.jsonrpc !== '2.0' || typeof msg.method !== 'string') {
    return {
      jsonrpc: '2.0',
      id: msg?.id ?? null,
      error: { code: -32600, message: 'Invalid JSON-RPC 2.0 request.' },
    };
  }

  const { id, method, params } = msg;

  // Notifications carry no id and expect no response
  if (method === 'notifications/initialized' || (method.startsWith('notifications/') && id === undefined)) {
    return null;
  }

  if (method === 'ping') {
    return { jsonrpc: '2.0', id, result: {} };
  }

  if (method === 'initialize') {
    const clientVersion = params?.protocolVersion;
    return {
      jsonrpc: '2.0',
      id,
      result: {
        protocolVersion: typeof clientVersion === 'string' && clientVersion ? clientVersion : PROTOCOL_VERSION,
        capabilities: {
          tools: { listChanged: false },
        },
        serverInfo: SERVER_INFO,
        instructions:
          'Motion Index MCP server. Use search_motions to discover UI motions, get_motion_code to retrieve Motion IR + stack-adapted code, and extract_motion to queue custom URL/video extractions.',
      },
    };
  }

  if (method === 'tools/list') {
    return {
      jsonrpc: '2.0',
      id,
      result: { tools: TOOLS },
    };
  }

  if (method === 'tools/call') {
    const toolName = params?.name;
    const args = params?.arguments || {};
    if (toolName === 'search_motions') {
      return { jsonrpc: '2.0', id, result: await execSearchMotions(args) };
    }
    if (toolName === 'get_motion_code') {
      return { jsonrpc: '2.0', id, result: await execGetMotionCode(args) };
    }
    if (toolName === 'extract_motion') {
      return { jsonrpc: '2.0', id, result: await execExtractMotion(args) };
    }
    return {
      jsonrpc: '2.0',
      id,
      error: { code: -32601, message: `Unknown tool: ${toolName}` },
    };
  }

  return {
    jsonrpc: '2.0',
    id,
    error: { code: -32601, message: `Method not found: ${method}` },
  };
}

/* ---------- stdio transport (newline-delimited JSON + Content-Length support) ---------- */
let transportMode = 'ndjson';
let rawBuf = Buffer.alloc(0);

function sendResponse(obj) {
  if (!obj) return;
  const payload = JSON.stringify(obj);
  if (transportMode === 'content-length') {
    const len = Buffer.byteLength(payload, 'utf8');
    process.stdout.write(`Content-Length: ${len}\r\n\r\n${payload}`);
  } else {
    process.stdout.write(`${payload}\n`);
  }
}

async function processRawMessage(jsonStr) {
  const trimmed = jsonStr.trim();
  if (!trimmed) return;
  let parsed;
  try {
    parsed = JSON.parse(trimmed);
  } catch {
    sendResponse({
      jsonrpc: '2.0',
      id: null,
      error: { code: -32700, message: 'Parse error: invalid JSON.' },
    });
    return;
  }
  const response = await handleRequest(parsed);
  if (response) sendResponse(response);
}

let draining = false;
async function drainBuffer() {
  if (draining) return;
  draining = true;
  try {
    while (rawBuf.length > 0) {
      const preview = rawBuf.subarray(0, Math.min(32, rawBuf.length)).toString('utf8');
      if (/^Content-Length:\s*\d+/i.test(preview)) {
        transportMode = 'content-length';
        const headerEnd = rawBuf.indexOf('\r\n\r\n');
        if (headerEnd === -1) break;
        const headerStr = rawBuf.subarray(0, headerEnd).toString('utf8');
        const m = headerStr.match(/Content-Length:\s*(\d+)/i);
        if (!m) {
          rawBuf = rawBuf.subarray(headerEnd + 4);
          continue;
        }
        const contentLen = Number(m[1]);
        const bodyStart = headerEnd + 4;
        if (rawBuf.length < bodyStart + contentLen) break;
        const bodyStr = rawBuf.subarray(bodyStart, bodyStart + contentLen).toString('utf8');
        rawBuf = rawBuf.subarray(bodyStart + contentLen);
        await processRawMessage(bodyStr);
      } else {
        const nl = rawBuf.indexOf(0x0a); // '\n'
        if (nl === -1) break;
        const line = rawBuf.subarray(0, nl).toString('utf8');
        rawBuf = rawBuf.subarray(nl + 1);
        await processRawMessage(line);
      }
    }
  } finally {
    draining = false;
  }
}

process.stdin.on('data', (chunk) => {
  rawBuf = Buffer.concat([rawBuf, chunk]);
  drainBuffer().catch((err) => {
    process.stderr.write(`[motion-index-mcp] error: ${err.message}\n`);
  });
});

process.stdin.on('end', () => {
  if (rawBuf.length > 0) {
    processRawMessage(rawBuf.toString('utf8')).finally(() => process.exit(0));
  } else {
    process.exit(0);
  }
});
