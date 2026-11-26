import {
  buildQuotaHeaders,
  corsPreflight,
  errorResponse,
  extractApiKey,
  getBaseUrl,
  jsonResponse,
  verifyApiKey,
} from './lib/auth.mjs';
import { searchMotions } from './lib/catalog.mjs';
import motionCodeHandler from './api-motion-code.mjs';
import extractHandler from './api-extract.mjs';

export const MCP_SERVER_INFO = {
  name: 'motion-index',
  version: '1.0.0',
};

export const MCP_PROTOCOL_VERSION = '2024-11-05';

export const MCP_TOOLS = [
  {
    name: 'search_motions',
    description:
      'Search and filter the Motion Index UI motion library by query, use-case pattern, trigger, feel, stack, or app name. Free and public discovery returning compact matches, IDs, and interactive preview URLs.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Free-text search query (e.g. "progress bar", "spring sheet", "shader", "Duolingo")' },
        pattern: { type: 'string', description: 'Use-case pattern (e.g. "Micro-interactions", "Navigation and layout", "Typography", "Transitions", "Backgrounds", "Generative")' },
        trigger: { type: 'string', description: 'Interaction trigger (e.g. "Click", "Hover", "Drag", "Loop", "Tab switch", "Cursor", "Ambient")' },
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
      'Fetch full Motion IR, extractable code, choreography beats, and stack-specific adaptation instructions (CSS, React/Motion, GSAP, SwiftUI, Remotion) for a motion ID. Applies Team Brand Motion Tokens automatically if configured on your API key or passed via designTokens.',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'Motion ID returned by search_motions (e.g. "app-duolingo-progress-surge")' },
        stack: {
          type: 'string',
          description: 'Target stack for adaptation instructions: "CSS", "React/Motion", "GSAP", "SwiftUI", or "Remotion"',
        },
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
      'Queue a metered custom motion extraction job from a live web URL or video recording URL. Requires Pro (30/mo), Teams (150/mo), or API Credits (10 credits/job).',
    inputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string', description: 'Public http(s) URL of the web page containing the target interaction' },
        videoUrl: { type: 'string', description: 'Public http(s) URL of an MP4/MOV/WebM recording of the UI interaction' },
        stack: { type: 'string', description: 'Target output stack (default "React/Motion")' },
        notes: { type: 'string', description: 'Optional instructions focusing on a specific element or beat' },
      },
    },
  },
];

function rpcOk(id, result, headers = {}) {
  return jsonResponse({ jsonrpc: '2.0', id: id ?? null, result }, 200, headers);
}

function rpcErr(id, code, message, data, status = 200, headers = {}) {
  return jsonResponse(
    {
      jsonrpc: '2.0',
      id: id ?? null,
      error: { code, message, ...(data !== undefined ? { data } : {}) },
    },
    status,
    headers
  );
}

function toolResult(payload, isError = false) {
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

async function handleToolCall(name, args, req, apiKey, baseUrl) {
  const safeArgs = args && typeof args === 'object' ? args : {};

  if (name === 'search_motions') {
    const result = searchMotions(
      {
        q: safeArgs.query || safeArgs.q || '',
        use: safeArgs.pattern || safeArgs.use,
        trigger: safeArgs.trigger,
        feel: safeArgs.feel,
        stack: safeArgs.stack,
        app: safeArgs.app,
        limit: Math.min(50, Math.max(1, Number(safeArgs.limit) || 12)),
      },
      baseUrl
    );
    return { result: toolResult(result), headers: buildQuotaHeaders({ tier: 'free', remaining: 'unlimited' }) };
  }

  if (name === 'get_motion_code') {
    if (!safeArgs.id) {
      return { result: toolResult({ error: 'Argument "id" is required.' }, true), headers: {} };
    }
    const headers = new Headers({ 'Content-Type': 'application/json' });
    if (apiKey) headers.set('Authorization', `Bearer ${apiKey}`);

    const subReq = new Request(`${baseUrl}/api/v1/motions/${encodeURIComponent(safeArgs.id)}/code`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        id: safeArgs.id,
        stack: safeArgs.stack,
        designTokens: safeArgs.designTokens,
      }),
    });
    const res = await motionCodeHandler(subReq);
    const data = await res.json();
    const outHeaders = {};
    for (const h of ['X-MotionIndex-Tier', 'X-MotionIndex-Quota-Remaining', 'X-MotionIndex-Quota-Limit', 'X-MotionIndex-Credits-Remaining']) {
      const v = res.headers.get(h);
      if (v) outHeaders[h] = v;
    }
    return { result: toolResult(data, !res.ok), headers: outHeaders };
  }

  if (name === 'extract_motion') {
    const headers = new Headers({ 'Content-Type': 'application/json' });
    if (apiKey) headers.set('Authorization', `Bearer ${apiKey}`);

    const subReq = new Request(`${baseUrl}/api/v1/extract`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        url: safeArgs.url,
        videoUrl: safeArgs.videoUrl,
        stack: safeArgs.stack,
        notes: safeArgs.notes,
      }),
    });
    const res = await extractHandler(subReq);
    const data = await res.json();
    const outHeaders = {};
    for (const h of ['X-MotionIndex-Tier', 'X-MotionIndex-Quota-Remaining', 'X-MotionIndex-Quota-Limit', 'X-MotionIndex-Credits-Remaining']) {
      const v = res.headers.get(h);
      if (v) outHeaders[h] = v;
    }
    return { result: toolResult(data, !res.ok), headers: outHeaders };
  }

  return { error: { code: -32601, message: `Unknown tool: ${name}` } };
}

export default async function handler(req) {
  if (req.method === 'OPTIONS') return corsPreflight();

  const baseUrl = getBaseUrl(req);

  if (req.method === 'GET') {
    return jsonResponse({
      name: MCP_SERVER_INFO.name,
      version: MCP_SERVER_INFO.version,
      transport: 'streamable-http',
      protocolVersion: MCP_PROTOCOL_VERSION,
      endpoint: `${baseUrl}/api/mcp`,
      tools: MCP_TOOLS.map((t) => ({ name: t.name, description: t.description })),
    });
  }

  if (req.method !== 'POST') {
    return errorResponse('Method not allowed. Send JSON-RPC 2.0 POST requests to /api/mcp.', 405);
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return rpcErr(null, -32700, 'Parse error: invalid JSON body.', undefined, 400);
  }

  if (!body || body.jsonrpc !== '2.0' || typeof body.method !== 'string') {
    return rpcErr(body?.id ?? null, -32600, 'Invalid Request: expected JSON-RPC 2.0 object with method.', undefined, 400);
  }

  const { id, method, params } = body;
  const apiKey = extractApiKey(req) || params?._meta?.apiKey || null;

  if (method === 'notifications/initialized' || method.startsWith('notifications/')) {
    return new Response(null, { status: 202, headers: { 'Access-Control-Allow-Origin': '*' } });
  }

  if (method === 'ping') {
    return rpcOk(id, {});
  }

  if (method === 'initialize') {
    const clientVersion = params?.protocolVersion;
    const auth = apiKey ? verifyApiKey(apiKey) : { valid: false };
    return rpcOk(id, {
      protocolVersion: typeof clientVersion === 'string' && clientVersion ? clientVersion : MCP_PROTOCOL_VERSION,
      capabilities: {
        tools: { listChanged: false },
      },
      serverInfo: MCP_SERVER_INFO,
      instructions:
        'Use search_motions to discover UI motions by query, pattern, trigger, feel, stack, or app; use get_motion_code to pull Motion IR, code, and stack adaptation prompts; use extract_motion for custom URL/video extraction.',
      _meta: {
        authenticated: auth.valid,
        tier: auth.valid ? auth.claims.tier : 'free',
      },
    });
  }

  if (method === 'tools/list') {
    return rpcOk(id, { tools: MCP_TOOLS });
  }

  if (method === 'tools/call') {
    const toolName = params?.name;
    if (!toolName || typeof toolName !== 'string') {
      return rpcErr(id, -32602, 'Invalid params: "name" is required for tools/call.');
    }
    const outcome = await handleToolCall(toolName, params?.arguments, req, apiKey, baseUrl);
    if (outcome.error) {
      return rpcErr(id, outcome.error.code, outcome.error.message);
    }
    return rpcOk(id, outcome.result, outcome.headers);
  }

  return rpcErr(id, -32601, `Method not found: ${method}`);
}
