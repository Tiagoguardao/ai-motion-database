#!/usr/bin/env node
/**
 * End-to-end verification suite for Motion Index Monetization, REST API, Billing, and MCP Server.
 */
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import {
  consumeQuota,
  issueApiKey,
  resetQuotaLedger,
  verifyApiKey,
} from '../netlify/functions/lib/auth.mjs';
import { loadCatalog } from '../netlify/functions/lib/catalog.mjs';
import motionsHandler from '../netlify/functions/api-motions.mjs';
import motionCodeHandler from '../netlify/functions/api-motion-code.mjs';
import extractHandler, { resetExtractJobs } from '../netlify/functions/api-extract.mjs';
import billingHandler, { verifyStripeWebhookSignature } from '../netlify/functions/api-billing.mjs';
import mcpHttpHandler from '../netlify/functions/api-mcp.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const BASE = 'https://ai-motion-database.netlify.app';

let passed = 0;
async function test(name, fn) {
  try {
    await fn();
    passed += 1;
    console.log(`  PASS  ${name}`);
  } catch (err) {
    console.error(`  FAIL  ${name}`);
    console.error(err);
    process.exitCode = 1;
    throw err;
  }
}

async function run() {
  console.log('\nMotion Index — Monetization, REST API & MCP Verification\n');

  const catalog = loadCatalog();
  assert.ok(catalog.count > 0, 'Catalog must contain motions');
  const sampleMotion = catalog.motions[0];

  /* 1. Auth & Quota Enforcement */
  await test('auth: HMAC-SHA256 key signing, verification, and tamper rejection', () => {
    const live = issueApiKey({ tier: 'pro', sub: 'dev@acme.io' }, { mode: 'live' });
    assert.ok(live.apiKey.startsWith('mi_live_'));
    const v = verifyApiKey(live.apiKey);
    assert.equal(v.valid, true);
    assert.equal(v.mode, 'live');
    assert.equal(v.claims.tier, 'pro');
    assert.equal(v.claims.sub, 'dev@acme.io');

    // Tamper signature
    const tampered = live.apiKey.slice(0, -2) + (live.apiKey.endsWith('aa') ? 'bb' : 'aa');
    assert.equal(verifyApiKey(tampered).valid, false);
    assert.equal(verifyApiKey('not-a-key').valid, false);
    assert.equal(verifyApiKey('').valid, false);
  });

  await test('auth: quota enforcement across Free (10/mo), Pro (unlimited/30), Credits (1 & 10), and Teams', () => {
    resetQuotaLedger();

    // Free tier: 10 code fetches allowed, 11th blocked (429), custom_extract blocked (402)
    const freeKey = issueApiKey({ tier: 'free', sub: 'free-user' });
    for (let i = 0; i < 10; i++) {
      const r = consumeQuota(freeKey.claims, 'code_fetch');
      assert.equal(r.allowed, true);
      assert.equal(r.remaining, 9 - i);
    }
    const free11 = consumeQuota(freeKey.claims, 'code_fetch');
    assert.equal(free11.allowed, false);
    assert.equal(free11.status, 429);
    const freeExtract = consumeQuota(freeKey.claims, 'custom_extract');
    assert.equal(freeExtract.allowed, false);
    assert.equal(freeExtract.status, 402);

    // Pro tier: unlimited code fetches, 30 custom extracts
    const proKey = issueApiKey({ tier: 'pro', sub: 'pro-user' });
    const proCode = consumeQuota(proKey.claims, 'code_fetch');
    assert.equal(proCode.allowed, true);
    assert.equal(proCode.remaining, 'unlimited');
    const proExt = consumeQuota(proKey.claims, 'custom_extract');
    assert.equal(proExt.allowed, true);
    assert.equal(proExt.remaining, 29);

    // Credits tier: 1 credit per code fetch, 10 credits per custom extract
    const credKey = issueApiKey({ tier: 'credits', sub: 'cred-user', credits: 11 });
    const c1 = consumeQuota(credKey.claims, 'code_fetch');
    assert.equal(c1.allowed, true);
    assert.equal(c1.remaining, 10);
    const c2 = consumeQuota(credKey.claims, 'custom_extract');
    assert.equal(c2.allowed, true);
    assert.equal(c2.remaining, 0);
    const c3 = consumeQuota(credKey.claims, 'code_fetch');
    assert.equal(c3.allowed, false);
    assert.equal(c3.status, 402);

    // Teams tier: Brand Motion Tokens encoded & unlimited code
    const teamsKey = issueApiKey({
      tier: 'teams',
      sub: 'team-acme',
      brandTokens: { brandName: 'Acme', springStiffness: 340, springDamping: 28, durationScale: 0.8 },
    });
    const tv = verifyApiKey(teamsKey.apiKey);
    assert.equal(tv.claims.brandTokens.brandName, 'Acme');
    assert.equal(tv.claims.brandTokens.springStiffness, 340);
    assert.equal(tv.claims.brandTokens.durationScale, 0.8);
  });

  /* 2. GET /api/v1/motions */
  await test('api-motions: public search, filtering, pagination, and dynamic catalogCount', async () => {
    const res = await motionsHandler(new Request(`${BASE}/api/v1/motions?q=progress&limit=5`));
    assert.equal(res.status, 200);
    assert.equal(res.headers.get('X-MotionIndex-Tier'), 'free');
    const data = await res.json();
    assert.equal(data.catalogCount, catalog.count);
    assert.ok(data.motions.length > 0 && data.motions.length <= 5);
    assert.ok(data.motions[0].previewUrl.includes(`#${data.motions[0].id}`));

    // App filter
    const appRes = await motionsHandler(new Request(`${BASE}/api/v1/motions?app=duolingo`));
    assert.equal(appRes.status, 200);
    const appData = await appRes.json();
    assert.ok(appData.total >= 1);
    assert.ok(appData.motions.every((m) => m.app?.slug === 'duolingo'));
  });

  /* 3. GET /api/v1/motions/:id/code */
  await test('api-motion-code: auth guard, stack adaptation, headers & Brand Motion Tokens', async () => {
    resetQuotaLedger();

    // Missing key -> 401
    const unauth = await motionCodeHandler(new Request(`${BASE}/api/v1/motions/${sampleMotion.id}/code`));
    assert.equal(unauth.status, 401);

    // Valid Teams key with Brand Motion Tokens -> 200
    const teams = issueApiKey({
      tier: 'teams',
      sub: 'brand-team',
      brandTokens: {
        brandName: 'SwissCo',
        springStiffness: 360,
        springDamping: 30,
        durationScale: 0.5,
        reducedMotionPolicy: 'crossfade',
      },
    });
    const res = await motionCodeHandler(
      new Request(`${BASE}/api/v1/motions/${sampleMotion.id}/code?stack=React/Motion`, {
        headers: { Authorization: `Bearer ${teams.apiKey}` },
      })
    );
    assert.equal(res.status, 200);
    assert.equal(res.headers.get('X-MotionIndex-Tier'), 'teams');
    assert.equal(res.headers.get('X-MotionIndex-Quota-Remaining'), 'unlimited');
    const data = await res.json();
    assert.equal(data.id, sampleMotion.id);
    assert.equal(data.stack, 'React/Motion');
    assert.equal(data.brandTokensApplied, true);
    assert.equal(data.motionIR.durationMs, Math.max(60, Math.round(sampleMotion.durationMs * 0.5)));
    assert.ok(data.adaptationPrompt.includes('SwissCo'));
    assert.ok(data.adaptationPrompt.includes('motion/react'));
    assert.ok(data.shareText.includes(`Motion #${sampleMotion.id}`));

    // Unknown ID -> 404
    const missing = await motionCodeHandler(
      new Request(`${BASE}/api/v1/motions/does-not-exist/code`, {
        headers: { 'X-API-Key': teams.apiKey },
      })
    );
    assert.equal(missing.status, 404);
  });

  /* 4. POST & GET /api/v1/extract */
  await test('api-extract: blocks free tier, charges 10 credits on credits tier, queues & retrieves job', async () => {
    resetQuotaLedger();
    resetExtractJobs();

    const free = issueApiKey({ tier: 'free', sub: 'free-ext' });
    const blocked = await extractHandler(
      new Request(`${BASE}/api/v1/extract`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${free.apiKey}` },
        body: JSON.stringify({ url: 'https://linear.app', stack: 'SwiftUI' }),
      })
    );
    assert.equal(blocked.status, 402);

    const cred = issueApiKey({ tier: 'credits', sub: 'agency-ext', credits: 25 });
    const created = await extractHandler(
      new Request(`${BASE}/api/v1/extract`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': cred.apiKey },
        body: JSON.stringify({ url: 'https://linear.app', stack: 'SwiftUI' }),
      })
    );
    assert.equal(created.status, 202);
    assert.equal(created.headers.get('X-MotionIndex-Credits-Remaining'), '15');
    const createdJson = await created.json();
    assert.equal(createdJson.billing.creditsCharged, 10);
    assert.equal(createdJson.job.status, 'queued');
    assert.equal(createdJson.job.targetStack, 'SwiftUI');

    // Poll job by ID
    const poll = await extractHandler(
      new Request(`${BASE}/api/v1/extract/${createdJson.job.jobId}`, {
        headers: { Authorization: `Bearer ${cred.apiKey}` },
      })
    );
    assert.equal(poll.status, 200);
    const pollJson = await poll.json();
    assert.equal(pollJson.job.jobId, createdJson.job.jobId);
  });

  /* 5. Billing (Sandbox mode + Stripe Webhook HMAC verification) */
  await test('api-billing: sandbox checkout, key issue/verify, portal, and Stripe webhook signature check', async () => {
    const prevStripe = process.env.STRIPE_SECRET_KEY;
    const prevWh = process.env.STRIPE_WEBHOOK_SECRET;
    delete process.env.STRIPE_SECRET_KEY;
    delete process.env.STRIPE_WEBHOOK_SECRET;

    try {
      const coRes = await billingHandler(
        new Request(`${BASE}/api/v1/checkout`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ plan: 'pro_annual', email: 'builder@test.dev' }),
        })
      );
      assert.equal(coRes.status, 200);
      const co = await coRes.json();
      assert.equal(co.mode, 'sandbox');
      assert.ok(co.apiKey.startsWith('mi_test_'));
      assert.equal(co.claims.tier, 'pro');

      const verRes = await billingHandler(
        new Request(`${BASE}/api/v1/keys/verify`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ apiKey: co.apiKey }),
        })
      );
      assert.equal(verRes.status, 200);
      const ver = await verRes.json();
      assert.equal(ver.valid, true);
      assert.equal(ver.claims.tier, 'pro');

      const portalRes = await billingHandler(
        new Request(`${BASE}/api/v1/portal`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${co.apiKey}` },
          body: JSON.stringify({}),
        })
      );
      assert.equal(portalRes.status, 200);
      const portal = await portalRes.json();
      assert.equal(portal.mode, 'sandbox');

      // Stripe webhook HMAC verification test
      const secret = 'whsec_test_123456';
      const ts = Math.floor(Date.now() / 1000);
      const payload = JSON.stringify({
        type: 'checkout.session.completed',
        data: { object: { id: 'cs_test_1', customer_email: 'buyer@test.dev', metadata: { tier: 'credits', credits: '2000' } } },
      });
      const sig = crypto.createHmac('sha256', secret).update(`${ts}.${payload}`).digest('hex');
      assert.equal(verifyStripeWebhookSignature(payload, `t=${ts},v1=${sig}`, secret).valid, true);
      assert.equal(verifyStripeWebhookSignature(payload, `t=${ts},v1=deadbeef`, secret).valid, false);

      process.env.STRIPE_WEBHOOK_SECRET = secret;
      const whOk = await billingHandler(
        new Request(`${BASE}/api/v1/webhooks/stripe`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'stripe-signature': `t=${ts},v1=${sig}` },
          body: payload,
        })
      );
      assert.equal(whOk.status, 200);
      const whJson = await whOk.json();
      assert.equal(whJson.received, true);
      assert.equal(whJson.provisioned.tier, 'credits');
      assert.equal(whJson.provisioned.credits, 2000);

      const whBad = await billingHandler(
        new Request(`${BASE}/api/v1/webhooks/stripe`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'stripe-signature': `t=${ts},v1=invalid` },
          body: payload,
        })
      );
      assert.equal(whBad.status, 400);
    } finally {
      if (prevStripe !== undefined) process.env.STRIPE_SECRET_KEY = prevStripe;
      if (prevWh !== undefined) process.env.STRIPE_WEBHOOK_SECRET = prevWh;
      else delete process.env.STRIPE_WEBHOOK_SECRET;
    }
  });

  /* 6. HTTP MCP Endpoint (/api/mcp) */
  await test('api-mcp: JSON-RPC initialize, tools/list, and all 3 tools/call over HTTP', async () => {
    resetQuotaLedger();
    const proKey = issueApiKey({ tier: 'pro', sub: 'mcp-http-user' }).apiKey;

    const rpc = async (payload) => {
      const res = await mcpHttpHandler(
        new Request(`${BASE}/api/mcp`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${proKey}` },
          body: JSON.stringify(payload),
        })
      );
      assert.equal(res.status, 200);
      return res.json();
    };

    const init = await rpc({ jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05' } });
    assert.equal(init.result.serverInfo.name, 'motion-index');
    assert.equal(init.result._meta.tier, 'pro');

    const listed = await rpc({ jsonrpc: '2.0', id: 2, method: 'tools/list' });
    const toolNames = listed.result.tools.map((t) => t.name);
    assert.deepEqual(toolNames, ['search_motions', 'get_motion_code', 'extract_motion']);

    const search = await rpc({
      jsonrpc: '2.0',
      id: 3,
      method: 'tools/call',
      params: { name: 'search_motions', arguments: { query: 'progress', limit: 3 } },
    });
    const searchData = JSON.parse(search.result.content[0].text);
    assert.ok(searchData.motions.length > 0);

    const code = await rpc({
      jsonrpc: '2.0',
      id: 4,
      method: 'tools/call',
      params: { name: 'get_motion_code', arguments: { id: sampleMotion.id, stack: 'GSAP' } },
    });
    assert.ok(!code.result.isError);
    const codeData = JSON.parse(code.result.content[0].text);
    assert.equal(codeData.stack, 'GSAP');

    const ext = await rpc({
      jsonrpc: '2.0',
      id: 5,
      method: 'tools/call',
      params: { name: 'extract_motion', arguments: { url: 'https://stripe.com', stack: 'Remotion' } },
    });
    assert.ok(!ext.result.isError);
    const extData = JSON.parse(ext.result.content[0].text);
    assert.equal(extData.job.targetStack, 'Remotion');
  });

  /* 7. Standalone stdio MCP Server (mcp/server.mjs) */
  await test('mcp/server.mjs: stdio JSON-RPC initialize, tools/list, and 3 tools/call', async () => {
    const proKey = issueApiKey({ tier: 'pro', sub: 'mcp-stdio-user' }).apiKey;
    const serverPath = path.join(ROOT, 'mcp', 'server.mjs');

    const responses = await new Promise((resolve, reject) => {
      const child = spawn(process.execPath, [serverPath], {
        cwd: ROOT,
        env: {
          ...process.env,
          MOTION_INDEX_LOCAL_ONLY: '1',
          MOTION_INDEX_API_KEY: proKey,
        },
        stdio: ['pipe', 'pipe', 'pipe'],
      });

      const out = [];
      let buf = '';
      let stderr = '';
      const timer = setTimeout(() => {
        child.kill();
        reject(new Error(`stdio MCP timed out. stderr=${stderr}`));
      }, 10000);

      child.stderr.on('data', (d) => {
        stderr += d.toString('utf8');
      });
      child.stdout.on('data', (chunk) => {
        buf += chunk.toString('utf8');
        let idx;
        while ((idx = buf.indexOf('\n')) !== -1) {
          const line = buf.slice(0, idx).trim();
          buf = buf.slice(idx + 1);
          if (line) out.push(JSON.parse(line));
        }
      });
      child.on('error', (err) => {
        clearTimeout(timer);
        reject(err);
      });
      child.on('close', (code) => {
        clearTimeout(timer);
        if (code !== 0) reject(new Error(`mcp/server.mjs exited with ${code}: ${stderr}`));
        else resolve(out);
      });

      const requests = [
        { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05' } },
        { jsonrpc: '2.0', method: 'notifications/initialized' },
        { jsonrpc: '2.0', id: 2, method: 'tools/list' },
        { jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'search_motions', arguments: { query: 'spring', limit: 3 } } },
        {
          jsonrpc: '2.0',
          id: 4,
          method: 'tools/call',
          params: {
            name: 'get_motion_code',
            arguments: {
              id: sampleMotion.id,
              stack: 'React/Motion',
              designTokens: { brandName: 'StdioBrand', springStiffness: 320, springDamping: 25 },
            },
          },
        },
        {
          jsonrpc: '2.0',
          id: 5,
          method: 'tools/call',
          params: { name: 'extract_motion', arguments: { videoUrl: 'https://example.com/demo.mp4', stack: 'SwiftUI' } },
        },
      ];

      for (const req of requests) {
        child.stdin.write(JSON.stringify(req) + '\n');
      }
      child.stdin.end();
    });

    assert.equal(responses.length, 5, 'Should receive 5 responses (notification produces no reply)');
    assert.equal(responses[0].id, 1);
    assert.equal(responses[0].result.serverInfo.name, 'motion-index');

    assert.equal(responses[1].id, 2);
    assert.deepEqual(
      responses[1].result.tools.map((t) => t.name),
      ['search_motions', 'get_motion_code', 'extract_motion']
    );

    const searchPayload = JSON.parse(responses[2].result.content[0].text);
    assert.ok(searchPayload.motions.length > 0);
    assert.equal(searchPayload.source, 'local-catalog');

    const codePayload = JSON.parse(responses[3].result.content[0].text);
    assert.equal(codePayload.id, sampleMotion.id);
    assert.equal(codePayload.stack, 'React/Motion');
    assert.equal(codePayload.brandTokensApplied, true);
    assert.ok(codePayload.adaptationPrompt.includes('StdioBrand'));

    const extractPayload = JSON.parse(responses[4].result.content[0].text);
    assert.equal(extractPayload.job.sourceType, 'video');
    assert.equal(extractPayload.job.targetStack, 'SwiftUI');
  });

  /* 8. Built frontend sanity & JS syntax checks */
  await test('frontend: index.html hooks and monetization.js syntax valid', () => {
    const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
    assert.ok(html.includes('assets/monetization.css'));
    assert.ok(html.includes('assets/monetization.js'));
    assert.ok(html.includes('data-view="pricing"'));
    assert.ok(html.includes('id="pricingView"'));
    assert.ok(html.includes('id="planPillMount"'));
    assert.ok(html.includes('id="d-share"'));
    assert.ok(html.includes('id="agentsInteractiveMount"'));

    // Syntax check inline <script> blocks in index.html using Function constructor
    const scriptMatches = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
    assert.ok(scriptMatches.length >= 1, 'Expected inline script block in index.html');
    for (const m of scriptMatches) {
      new Function(m[1]);
    }
    const monJs = fs.readFileSync(path.join(ROOT, 'assets', 'monetization.js'), 'utf8');
    new Function(monJs);
  });

  console.log(`\nAll ${passed} verification tests passed.\n`);
}

run().catch(() => process.exit(1));
