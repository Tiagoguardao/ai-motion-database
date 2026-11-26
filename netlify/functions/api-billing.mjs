import crypto from 'node:crypto';
import {
  corsPreflight,
  DEFAULT_BRAND_TOKENS,
  errorResponse,
  extractApiKey,
  getBaseUrl,
  getQuotaSnapshot,
  issueApiKey,
  jsonResponse,
  sanitizeBrandTokens,
  TIERS,
  verifyApiKey,
} from './lib/auth.mjs';

const PLAN_CATALOG = {
  free: { tier: 'free', mode: 'free', priceEnv: null, credits: 0, label: 'Free ($0)' },
  pro_monthly: { tier: 'pro', mode: 'subscription', priceEnv: 'STRIPE_PRICE_PRO_MONTHLY', credits: 0, label: 'Pro Builder ($19/mo)' },
  pro_annual: { tier: 'pro', mode: 'subscription', priceEnv: 'STRIPE_PRICE_PRO_ANNUAL', credits: 0, label: 'Pro Builder ($15/mo billed annually)' },
  credits_500: { tier: 'credits', mode: 'payment', priceEnv: 'STRIPE_PRICE_CREDITS_500', credits: 500, label: '500 API Credits ($15)' },
  credits_2000: { tier: 'credits', mode: 'payment', priceEnv: 'STRIPE_PRICE_CREDITS_2000', credits: 2000, label: '2,000 API Credits ($49)' },
  credits_7500: { tier: 'credits', mode: 'payment', priceEnv: 'STRIPE_PRICE_CREDITS_7500', credits: 7500, label: '7,500 API Credits ($149)' },
  teams_monthly: { tier: 'teams', mode: 'subscription', priceEnv: 'STRIPE_PRICE_TEAMS_MONTHLY', credits: 0, label: 'Teams / Brand Motion ($149/mo)' },
  teams_annual: { tier: 'teams', mode: 'subscription', priceEnv: 'STRIPE_PRICE_TEAMS_ANNUAL', credits: 0, label: 'Teams / Brand Motion ($119/mo billed annually)' },
};

function resolveAction(url) {
  const q = url.searchParams.get('action');
  if (q) return q.trim().toLowerCase();
  const p = url.pathname.toLowerCase();
  if (p.endsWith('/checkout')) return 'checkout';
  if (p.endsWith('/portal')) return 'portal';
  if (p.endsWith('/webhooks/stripe') || p.endsWith('/webhook')) return 'webhook';
  if (p.endsWith('/keys/issue')) return 'issue-key';
  if (p.endsWith('/keys/verify')) return 'verify-key';
  return 'checkout';
}

function normalizePlanId(plan, billing = 'monthly') {
  const p = String(plan || 'pro_monthly').trim().toLowerCase();
  if (PLAN_CATALOG[p]) return p;
  if (p === 'pro') return billing === 'annual' ? 'pro_annual' : 'pro_monthly';
  if (p === 'teams') return billing === 'annual' ? 'teams_annual' : 'teams_monthly';
  if (p === 'credits') return 'credits_500';
  return null;
}

/**
 * Verify Stripe-Signature header (`t=<ts>,v1=<hex>,...`) using HMAC-SHA256.
 */
export function verifyStripeWebhookSignature(rawBody, sigHeader, webhookSecret, toleranceSeconds = 300) {
  if (!sigHeader || !webhookSecret) {
    return { valid: false, error: 'Missing Stripe signature or webhook secret.' };
  }
  const parts = {};
  for (const segment of String(sigHeader).split(',')) {
    const [k, v] = segment.split('=');
    if (!k || !v) continue;
    if (!parts[k.trim()]) parts[k.trim()] = [];
    parts[k.trim()].push(v.trim());
  }
  const timestamp = Number(parts.t?.[0]);
  const v1Sigs = parts.v1 || [];
  if (!Number.isFinite(timestamp) || !v1Sigs.length) {
    return { valid: false, error: 'Malformed Stripe-Signature header.' };
  }
  const nowSec = Math.floor(Date.now() / 1000);
  if (Math.abs(nowSec - timestamp) > toleranceSeconds) {
    return { valid: false, error: 'Stripe webhook timestamp outside tolerance window.' };
  }
  const signedPayload = `${timestamp}.${rawBody}`;
  const expected = crypto.createHmac('sha256', webhookSecret).update(signedPayload, 'utf8').digest('hex');
  const expectedBuf = Buffer.from(expected, 'utf8');

  const matched = v1Sigs.some((sig) => {
    const sigBuf = Buffer.from(sig, 'utf8');
    return sigBuf.length === expectedBuf.length && crypto.timingSafeEqual(sigBuf, expectedBuf);
  });

  return matched ? { valid: true, timestamp } : { valid: false, error: 'Stripe webhook signature mismatch.' };
}

async function stripeRequest(endpoint, params, secretKey) {
  const body = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) body.append(k, String(v));
  }
  const res = await fetch(`https://api.stripe.com/v1/${endpoint}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${secretKey}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: body.toString(),
  });
  const data = await res.json();
  if (!res.ok) {
    const errMsg = data?.error?.message || `Stripe API error (${res.status})`;
    throw new Error(errMsg);
  }
  return data;
}

async function handleCheckout(req, baseUrl) {
  let body = {};
  try {
    body = await req.json();
  } catch {
    body = {};
  }

  const planId = normalizePlanId(body.plan, body.billing);
  if (!planId) {
    return errorResponse('Invalid plan. Choose free, pro_monthly, pro_annual, credits_500, credits_2000, credits_7500, teams_monthly, or teams_annual.', 400);
  }

  const spec = PLAN_CATALOG[planId];
  const email = typeof body.email === 'string' && body.email.trim() ? body.email.trim() : `builder_${crypto.randomBytes(3).toString('hex')}@motionindex.dev`;
  const brandTokens = sanitizeBrandTokens(body.brandTokens);

  // Free plan always issues an immediate key (no Stripe Checkout needed)
  if (spec.tier === 'free') {
    const issued = issueApiKey({ tier: 'free', sub: email }, { mode: process.env.STRIPE_SECRET_KEY ? 'live' : 'test' });
    return jsonResponse({
      mode: process.env.STRIPE_SECRET_KEY ? 'live' : 'sandbox',
      plan: planId,
      label: spec.label,
      checkoutUrl: null,
      apiKey: issued.apiKey,
      claims: issued.claims,
      message: 'Free API key issued (10 library code extractions/month; gallery, previews & specs unlimited).',
    });
  }

  const stripeKey = process.env.STRIPE_SECRET_KEY;
  const priceId = spec.priceEnv ? process.env[spec.priceEnv] : null;

  if (stripeKey && priceId) {
    try {
      const sessionParams = {
        mode: spec.mode,
        'line_items[0][price]': priceId,
        'line_items[0][quantity]': '1',
        success_url: `${baseUrl}/?checkout=success&plan=${encodeURIComponent(planId)}&session_id={CHECKOUT_SESSION_ID}#pricing`,
        cancel_url: `${baseUrl}/?checkout=canceled#pricing`,
        'metadata[planId]': planId,
        'metadata[tier]': spec.tier,
        'metadata[credits]': String(spec.credits || 0),
        customer_email: body.email || undefined,
      };
      const session = await stripeRequest('checkout/sessions', sessionParams, stripeKey);
      return jsonResponse({
        mode: 'stripe',
        plan: planId,
        label: spec.label,
        sessionId: session.id,
        checkoutUrl: session.url,
      });
    } catch (err) {
      return errorResponse(`Stripe checkout failed: ${err.message}`, 502);
    }
  }

  // Sandbox / Demo mode fallback: issue a real signed mi_test_ key immediately
  const issued = issueApiKey(
    {
      tier: spec.tier,
      sub: email,
      credits: spec.credits,
      brandTokens: spec.tier === 'teams' ? brandTokens || { ...DEFAULT_BRAND_TOKENS } : brandTokens,
    },
    { mode: 'test' }
  );

  return jsonResponse({
    mode: 'sandbox',
    plan: planId,
    label: spec.label,
    checkoutUrl: null,
    apiKey: issued.apiKey,
    claims: issued.claims,
    message: `Sandbox mode active (STRIPE_SECRET_KEY not configured). Issued a working ${spec.label} test API key so you can exercise every endpoint and MCP tool end-to-end.`,
  });
}

async function handlePortal(req, baseUrl) {
  let body = {};
  try {
    body = await req.json();
  } catch {
    body = {};
  }

  const stripeKey = process.env.STRIPE_SECRET_KEY;
  if (stripeKey && body.customerId) {
    try {
      const session = await stripeRequest(
        'billing_portal/sessions',
        {
          customer: body.customerId,
          return_url: `${baseUrl}/#pricing`,
        },
        stripeKey
      );
      return jsonResponse({
        mode: 'stripe',
        portalUrl: session.url,
      });
    } catch (err) {
      return errorResponse(`Stripe Billing Portal failed: ${err.message}`, 502);
    }
  }

  const rawKey = extractApiKey(req) || body.apiKey;
  const auth = rawKey ? verifyApiKey(rawKey) : { valid: false };

  return jsonResponse({
    mode: 'sandbox',
    portalUrl: null,
    activeTier: auth.valid ? auth.claims.tier : 'free',
    message: stripeKey
      ? 'Provide a Stripe customerId to open the live Billing Portal.'
      : 'Sandbox mode active: manage or switch test plans directly inside the API Key & Plan modal.',
  });
}

async function handleWebhook(req) {
  const rawBody = await req.text();
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  const sigHeader = req.headers.get('stripe-signature') || '';

  if (webhookSecret) {
    const check = verifyStripeWebhookSignature(rawBody, sigHeader, webhookSecret);
    if (!check.valid) {
      return errorResponse(check.error, 400);
    }
  }

  let event;
  try {
    event = JSON.parse(rawBody);
  } catch {
    return errorResponse('Invalid JSON webhook payload.', 400);
  }

  const type = event?.type || 'unknown';
  const obj = event?.data?.object || {};
  const meta = obj.metadata || {};

  if (type === 'checkout.session.completed') {
    const tier = TIERS[meta.tier] ? meta.tier : 'pro';
    const credits = Number(meta.credits) || 0;
    const sub = obj.customer || obj.customer_email || `stripe_${obj.id || 'session'}`;
    const issued = issueApiKey(
      { tier, sub, credits },
      { mode: process.env.STRIPE_SECRET_KEY ? 'live' : 'test' }
    );
    return jsonResponse({
      received: true,
      eventType: type,
      provisioned: {
        tier: issued.claims.tier,
        sub: issued.claims.sub,
        credits: issued.claims.credits,
        keyPrefix: issued.apiKey.slice(0, 14) + '…',
      },
    });
  }

  return jsonResponse({
    received: true,
    eventType: type,
    verified: Boolean(webhookSecret),
  });
}

async function handleIssueKey(req) {
  let body = {};
  try {
    body = await req.json();
  } catch {
    body = {};
  }

  const requestedTier = TIERS[body.tier] ? body.tier : 'free';
  const isStripeLive = Boolean(process.env.STRIPE_SECRET_KEY);

  // In live production (when Stripe is configured), unauthenticated direct issuance is restricted to free or sandbox test mode.
  const requestedMode = body.mode === 'live' && requestedTier === 'free' && isStripeLive ? 'live' : 'test';
  const sub = typeof body.email === 'string' && body.email.trim()
    ? body.email.trim()
    : typeof body.sub === 'string' && body.sub.trim()
      ? body.sub.trim()
      : `sandbox_${crypto.randomBytes(4).toString('hex')}@motionindex.dev`;

  const credits =
    requestedTier === 'credits'
      ? Math.max(1, Math.min(50000, Math.floor(Number(body.credits) || 500)))
      : 0;

  const brandTokens = sanitizeBrandTokens(body.brandTokens);
  const issued = issueApiKey(
    {
      tier: requestedTier,
      sub,
      credits,
      brandTokens: requestedTier === 'teams' ? brandTokens || { ...DEFAULT_BRAND_TOKENS } : brandTokens,
    },
    { mode: requestedMode }
  );

  return jsonResponse({
    mode: requestedMode === 'live' ? 'live' : 'sandbox',
    apiKey: issued.apiKey,
    claims: issued.claims,
    tierInfo: TIERS[requestedTier],
    quota: getQuotaSnapshot(issued.claims),
  });
}

async function handleVerifyKey(req) {
  let body = {};
  if (req.method === 'POST') {
    try {
      body = await req.json();
    } catch {
      body = {};
    }
  }
  const rawKey = extractApiKey(req) || body.apiKey;
  const check = verifyApiKey(rawKey);
  if (!check.valid) {
    return errorResponse(check.error || 'Invalid API key.', 401, { valid: false });
  }
  return jsonResponse({
    valid: true,
    mode: check.mode,
    claims: check.claims,
    tierInfo: TIERS[check.claims.tier],
    quota: getQuotaSnapshot(check.claims),
  });
}

export default async function handler(req) {
  if (req.method === 'OPTIONS') return corsPreflight();
  const url = new URL(req.url);
  const action = resolveAction(url);
  const baseUrl = getBaseUrl(req);

  if (action === 'verify-key' && (req.method === 'GET' || req.method === 'POST')) {
    return handleVerifyKey(req);
  }
  if (req.method !== 'POST') {
    return errorResponse(`Method not allowed for billing action "${action}". Use POST.`, 405);
  }

  switch (action) {
    case 'checkout':
      return handleCheckout(req, baseUrl);
    case 'portal':
      return handlePortal(req, baseUrl);
    case 'webhook':
      return handleWebhook(req);
    case 'issue-key':
      return handleIssueKey(req);
    default:
      return errorResponse(`Unknown billing action: ${action}`, 400);
  }
}
