import crypto from 'node:crypto';

const DEFAULT_DEV_SECRET = 'motion-index-sandbox-signing-secret-v1';

export const TIERS = {
  free: {
    id: 'free',
    label: 'Free',
    monthlyPriceUsd: 0,
    annualPriceUsd: 0,
    codeQuotaPerMonth: 10,
    customExtractsPerMonth: 0,
    defaultCredits: 0,
    brandTokensEnabled: false,
  },
  pro: {
    id: 'pro',
    label: 'Pro (Builder)',
    monthlyPriceUsd: 19,
    annualPriceUsd: 15,
    codeQuotaPerMonth: null, // unlimited
    customExtractsPerMonth: 30,
    defaultCredits: 0,
    brandTokensEnabled: false,
  },
  credits: {
    id: 'credits',
    label: 'API / Credits',
    monthlyPriceUsd: 0,
    annualPriceUsd: 0,
    codeQuotaPerMonth: null,
    customExtractsPerMonth: null,
    defaultCredits: 500,
    codeCreditCost: 1,
    customExtractCreditCost: 10,
    brandTokensEnabled: false,
    packs: [
      { id: 'credits_500', label: '500 credits', credits: 500, priceUsd: 15 },
      { id: 'credits_2000', label: '2,000 credits', credits: 2000, priceUsd: 49 },
      { id: 'credits_7500', label: '7,500 credits', credits: 7500, priceUsd: 149 },
    ],
  },
  teams: {
    id: 'teams',
    label: 'Teams / Brand Motion',
    monthlyPriceUsd: 149,
    annualPriceUsd: 119,
    codeQuotaPerMonth: null, // unlimited
    customExtractsPerMonth: 150,
    defaultCredits: 0,
    brandTokensEnabled: true,
  },
};

export const CREDIT_COSTS = {
  code_fetch: 1,
  custom_extract: 10,
};

export const DEFAULT_BRAND_TOKENS = {
  brandName: 'Default Brand',
  springStiffness: 280,
  springDamping: 26,
  durationScale: 1.0,
  bezierCurve: [0.2, 0.8, 0.2, 1],
  reducedMotionPolicy: 'respect', // 'respect' | 'crossfade' | 'instant'
};

export function getSigningSecret(override) {
  return override || process.env.MOTION_INDEX_SIGNING_SECRET || DEFAULT_DEV_SECRET;
}

export function getBaseUrl(req) {
  if (process.env.MOTION_INDEX_BASE_URL) {
    return process.env.MOTION_INDEX_BASE_URL.replace(/\/+$/, '');
  }
  if (req) {
    try {
      const url = new URL(req.url);
      return `${url.protocol}//${url.host}`;
    } catch {
      // fall through
    }
  }
  return 'https://ai-motion-database.netlify.app';
}

function base64UrlEncode(input) {
  const buf = Buffer.isBuffer(input) ? input : Buffer.from(String(input), 'utf8');
  return buf.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
}

function base64UrlDecode(str) {
  const padded = str.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat((4 - (str.length % 4)) % 4);
  return Buffer.from(padded, 'base64').toString('utf8');
}

export function sanitizeBrandTokens(input) {
  if (!input || typeof input !== 'object') return null;
  const out = {};
  if (typeof input.brandName === 'string' && input.brandName.trim()) {
    out.brandName = input.brandName.trim().slice(0, 80);
  }
  if (input.springStiffness !== undefined && input.springStiffness !== null && input.springStiffness !== '') {
    const k = Number(input.springStiffness);
    if (Number.isFinite(k)) out.springStiffness = Math.round(Math.min(1200, Math.max(40, k)));
  }
  if (input.springDamping !== undefined && input.springDamping !== null && input.springDamping !== '') {
    const c = Number(input.springDamping);
    if (Number.isFinite(c)) out.springDamping = Math.round(Math.min(120, Math.max(4, c)));
  }
  if (input.durationScale !== undefined && input.durationScale !== null && input.durationScale !== '') {
    const s = Number(input.durationScale);
    if (Number.isFinite(s)) out.durationScale = Number(Math.min(2.5, Math.max(0.25, s)).toFixed(2));
  }
  if (input.bezierCurve !== undefined && input.bezierCurve !== null && input.bezierCurve !== '') {
    let arr = input.bezierCurve;
    if (typeof arr === 'string') {
      arr = arr
        .replace(/cubic-bezier\(|\)/gi, '')
        .split(',')
        .map((v) => Number(v.trim()));
    }
    if (Array.isArray(arr) && arr.length === 4 && arr.every((n) => Number.isFinite(n))) {
      out.bezierCurve = arr.map((n, i) =>
        i === 0 || i === 2 ? Number(Math.min(1, Math.max(0, n)).toFixed(3)) : Number(Math.min(2, Math.max(-1, n)).toFixed(3))
      );
    }
  }
  if (typeof input.reducedMotionPolicy === 'string') {
    const p = input.reducedMotionPolicy.trim().toLowerCase();
    if (['respect', 'crossfade', 'instant'].includes(p)) {
      out.reducedMotionPolicy = p;
    }
  }
  return Object.keys(out).length ? out : null;
}

export function buildDefaultQuota(tier) {
  const cfg = TIERS[tier] || TIERS.free;
  return {
    code: cfg.codeQuotaPerMonth,
    extract: cfg.customExtractsPerMonth,
  };
}

/**
 * Issue a stateless HMAC-SHA256 signed Motion Index API key.
 * Format: mi_<live|test>_<base64url(json)>.<base64url(hmac)>
 */
export function issueApiKey(input = {}, options = {}) {
  const mode = options.mode === 'live' ? 'live' : 'test';
  const tier = TIERS[input.tier] ? input.tier : 'free';
  const tierCfg = TIERS[tier];
  const brandTokens = sanitizeBrandTokens(input.brandTokens);

  const claims = {
    tier,
    sub: String(input.sub || `user_${crypto.randomBytes(6).toString('hex')}`),
    quota: input.quota && typeof input.quota === 'object' ? input.quota : buildDefaultQuota(tier),
    credits: Number.isFinite(Number(input.credits))
      ? Math.max(0, Math.floor(Number(input.credits)))
      : tierCfg.defaultCredits,
    brandTokens: brandTokens || (tier === 'teams' ? { ...DEFAULT_BRAND_TOKENS } : null),
    iat: Number.isFinite(Number(input.iat)) ? Math.floor(Number(input.iat)) : Math.floor(Date.now() / 1000),
  };

  if (input.exp && Number.isFinite(Number(input.exp))) {
    claims.exp = Math.floor(Number(input.exp));
  }

  const prefix = `mi_${mode}_`;
  const payloadB64 = base64UrlEncode(JSON.stringify(claims));
  const secret = getSigningSecret(options.secret);
  const sig = crypto.createHmac('sha256', secret).update(`${prefix}${payloadB64}`).digest();
  const sigB64 = base64UrlEncode(sig);

  return {
    apiKey: `${prefix}${payloadB64}.${sigB64}`,
    mode,
    claims,
  };
}

/**
 * Verify a Motion Index API key using timing-safe HMAC comparison.
 */
export function verifyApiKey(rawKey, options = {}) {
  if (!rawKey || typeof rawKey !== 'string') {
    return { valid: false, error: 'Missing API key.' };
  }
  const token = rawKey.trim();
  const match = token.match(/^mi_(live|test)_([A-Za-z0-9_-]+)\.([A-Za-z0-9_-]+)$/);
  if (!match) {
    return { valid: false, error: 'Malformed API key format. Expected mi_live_... or mi_test_...' };
  }

  const [, mode, payloadB64, sigB64] = match;
  const secret = getSigningSecret(options.secret);
  const expectedSig = crypto.createHmac('sha256', secret).update(`mi_${mode}_${payloadB64}`).digest();
  const expectedB64 = base64UrlEncode(expectedSig);

  const a = Buffer.from(sigB64, 'utf8');
  const b = Buffer.from(expectedB64, 'utf8');
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
    return { valid: false, error: 'Invalid API key signature.' };
  }

  let claims;
  try {
    claims = JSON.parse(base64UrlDecode(payloadB64));
  } catch {
    return { valid: false, error: 'Corrupted API key payload.' };
  }

  if (!claims || typeof claims !== 'object' || !TIERS[claims.tier]) {
    return { valid: false, error: 'Unsupported API key tier.' };
  }

  if (claims.exp && Math.floor(Date.now() / 1000) > claims.exp) {
    return { valid: false, error: 'API key has expired.' };
  }

  return {
    valid: true,
    mode,
    claims: {
      tier: claims.tier,
      sub: claims.sub || 'anonymous',
      quota: claims.quota || buildDefaultQuota(claims.tier),
      credits: Number.isFinite(Number(claims.credits)) ? Number(claims.credits) : 0,
      brandTokens: sanitizeBrandTokens(claims.brandTokens),
      iat: claims.iat,
      exp: claims.exp,
    },
  };
}

export function extractApiKey(req) {
  if (!req) return null;
  const authHeader = req.headers?.get?.('authorization') || req.headers?.authorization || '';
  if (typeof authHeader === 'string' && authHeader.toLowerCase().startsWith('bearer ')) {
    return authHeader.slice(7).trim();
  }
  const xKey = req.headers?.get?.('x-api-key') || req.headers?.['x-api-key'] || '';
  if (typeof xKey === 'string' && xKey.trim()) {
    return xKey.trim();
  }
  try {
    const url = new URL(req.url);
    const qKey = url.searchParams.get('api_key');
    if (qKey && qKey.trim()) return qKey.trim();
  } catch {
    // ignore
  }
  return null;
}

/* ---------- In-process quota & credit ledger ---------- */
// Tracks per-subject usage within the warm serverless instance; resets cleanly each month.
const usageLedger = new Map();

function currentMonthBucket() {
  const now = new Date();
  const y = now.getUTCFullYear();
  const m = String(now.getUTCMonth() + 1).padStart(2, '0');
  return `${y}-${m}`;
}

function nextMonthResetIso() {
  const now = new Date();
  const reset = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + 1, 1, 0, 0, 0));
  return reset.toISOString();
}

function ledgerKey(claims) {
  return `${claims.sub}:${claims.iat || 0}:${currentMonthBucket()}`;
}

function getBucket(claims) {
  const key = ledgerKey(claims);
  if (!usageLedger.has(key)) {
    usageLedger.set(key, {
      codeFetches: 0,
      customExtracts: 0,
      creditsSpent: 0,
    });
  }
  return usageLedger.get(key);
}

export function resetQuotaLedger() {
  usageLedger.clear();
}

export function getQuotaSnapshot(claims) {
  const bucket = getBucket(claims);
  const tier = claims.tier;
  const quota = claims.quota || buildDefaultQuota(tier);
  const creditsTotal = Number.isFinite(Number(claims.credits)) ? Number(claims.credits) : 0;
  const creditsRemaining = Math.max(0, creditsTotal - bucket.creditsSpent);

  const codeLimit = quota.code ?? TIERS[tier]?.codeQuotaPerMonth ?? null;
  const extractLimit = quota.extract ?? TIERS[tier]?.customExtractsPerMonth ?? null;

  return {
    tier,
    month: currentMonthBucket(),
    resetAt: nextMonthResetIso(),
    code: {
      used: bucket.codeFetches,
      limit: codeLimit,
      remaining: codeLimit === null ? 'unlimited' : Math.max(0, codeLimit - bucket.codeFetches),
    },
    extract: {
      used: bucket.customExtracts,
      limit: extractLimit,
      remaining: extractLimit === null ? (tier === 'credits' ? Math.floor(creditsRemaining / CREDIT_COSTS.custom_extract) : 'unlimited') : Math.max(0, extractLimit - bucket.customExtracts),
    },
    credits: {
      total: creditsTotal,
      spent: bucket.creditsSpent,
      remaining: creditsRemaining,
    },
  };
}

/**
 * Consume quota or credits for an authenticated action ('code_fetch' | 'custom_extract').
 */
export function consumeQuota(claims, action) {
  const bucket = getBucket(claims);
  const tier = claims.tier;
  const quota = claims.quota || buildDefaultQuota(tier);
  const resetAt = nextMonthResetIso();

  if (tier === 'credits') {
    const cost = CREDIT_COSTS[action] || 1;
    const totalCredits = Number.isFinite(Number(claims.credits)) ? Number(claims.credits) : 0;
    const remainingBefore = Math.max(0, totalCredits - bucket.creditsSpent);

    if (remainingBefore < cost) {
      return {
        allowed: false,
        status: 402,
        error: `Insufficient credits (${remainingBefore} remaining, ${cost} required for ${action}). Purchase a credit pack at /#pricing.`,
        tier,
        cost,
        remaining: remainingBefore,
        limit: totalCredits,
        resetAt,
        headers: buildQuotaHeaders({ tier, remaining: remainingBefore, limit: totalCredits, creditsRemaining: remainingBefore }),
      };
    }

    bucket.creditsSpent += cost;
    if (action === 'code_fetch') bucket.codeFetches += 1;
    if (action === 'custom_extract') bucket.customExtracts += 1;
    const remainingAfter = Math.max(0, totalCredits - bucket.creditsSpent);

    return {
      allowed: true,
      status: 200,
      tier,
      cost,
      remaining: remainingAfter,
      limit: totalCredits,
      creditsRemaining: remainingAfter,
      resetAt,
      headers: buildQuotaHeaders({ tier, remaining: remainingAfter, limit: totalCredits, creditsRemaining: remainingAfter }),
    };
  }

  if (action === 'code_fetch') {
    const limit = quota.code !== undefined ? quota.code : TIERS[tier]?.codeQuotaPerMonth;
    if (limit === null) {
      bucket.codeFetches += 1;
      return {
        allowed: true,
        status: 200,
        tier,
        cost: 0,
        remaining: 'unlimited',
        limit: 'unlimited',
        resetAt,
        headers: buildQuotaHeaders({ tier, remaining: 'unlimited', limit: 'unlimited' }),
      };
    }
    if (bucket.codeFetches >= limit) {
      return {
        allowed: false,
        status: 429,
        error: `Monthly ${TIERS[tier]?.label || tier} code extraction quota reached (${limit}/${limit}). Upgrade to Pro for unlimited extractions or top up API credits.`,
        tier,
        cost: 0,
        remaining: 0,
        limit,
        resetAt,
        headers: buildQuotaHeaders({ tier, remaining: 0, limit }),
      };
    }
    bucket.codeFetches += 1;
    const rem = Math.max(0, limit - bucket.codeFetches);
    return {
      allowed: true,
      status: 200,
      tier,
      cost: 0,
      remaining: rem,
      limit,
      resetAt,
      headers: buildQuotaHeaders({ tier, remaining: rem, limit }),
    };
  }

  if (action === 'custom_extract') {
    const limit = quota.extract !== undefined ? quota.extract : TIERS[tier]?.customExtractsPerMonth;
    if (!limit || limit <= 0) {
      return {
        allowed: false,
        status: 402,
        error: `Custom URL/video extraction is not included on the ${TIERS[tier]?.label || tier} plan. Upgrade to Pro (30/mo), Teams (150/mo), or API Credits (10 credits/job).`,
        tier,
        cost: 0,
        remaining: 0,
        limit: 0,
        resetAt,
        headers: buildQuotaHeaders({ tier, remaining: 0, limit: 0 }),
      };
    }
    if (bucket.customExtracts >= limit) {
      return {
        allowed: false,
        status: 429,
        error: `Monthly custom extraction quota reached (${limit}/${limit}). Wait until ${resetAt} or purchase an API credit pack.`,
        tier,
        cost: 0,
        remaining: 0,
        limit,
        resetAt,
        headers: buildQuotaHeaders({ tier, remaining: 0, limit }),
      };
    }
    bucket.customExtracts += 1;
    const rem = Math.max(0, limit - bucket.customExtracts);
    return {
      allowed: true,
      status: 200,
      tier,
      cost: 0,
      remaining: rem,
      limit,
      resetAt,
      headers: buildQuotaHeaders({ tier, remaining: rem, limit }),
    };
  }

  return {
    allowed: false,
    status: 400,
    error: `Unknown metered action: ${action}`,
    tier,
    headers: buildQuotaHeaders({ tier, remaining: 0, limit: 0 }),
  };
}

export function buildQuotaHeaders({ tier, remaining, limit, creditsRemaining }) {
  const h = {
    'X-MotionIndex-Tier': String(tier || 'free'),
    'X-MotionIndex-Quota-Remaining': String(remaining ?? 'unlimited'),
  };
  if (limit !== undefined && limit !== null) {
    h['X-MotionIndex-Quota-Limit'] = String(limit);
  }
  if (creditsRemaining !== undefined && creditsRemaining !== null) {
    h['X-MotionIndex-Credits-Remaining'] = String(creditsRemaining);
  }
  return h;
}

/* ---------- HTTP response helpers ---------- */

export const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key, Mcp-Session-Id',
  'Access-Control-Expose-Headers': 'X-MotionIndex-Tier, X-MotionIndex-Quota-Remaining, X-MotionIndex-Quota-Limit, X-MotionIndex-Credits-Remaining',
};

export function corsPreflight() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export function jsonResponse(data, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      ...CORS_HEADERS,
      ...extraHeaders,
    },
  });
}

export function errorResponse(message, status = 400, extra = {}, extraHeaders = {}) {
  return jsonResponse({ error: message, ...extra }, status, extraHeaders);
}
