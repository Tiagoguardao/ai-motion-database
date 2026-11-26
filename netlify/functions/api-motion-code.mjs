import {
  consumeQuota,
  corsPreflight,
  errorResponse,
  extractApiKey,
  getBaseUrl,
  jsonResponse,
  sanitizeBrandTokens,
  verifyApiKey,
} from './lib/auth.mjs';
import {
  buildMotionCodePayload,
  getMotionById,
  SUPPORTED_TARGET_STACKS,
} from './lib/catalog.mjs';

function parseMotionId(req, url, body) {
  if (body?.id) return String(body.id).trim();
  const qId = url.searchParams.get('id');
  if (qId) return qId.trim();
  // Match /api/v1/motions/:id/code
  const m = url.pathname.match(/\/api\/v1\/motions\/([^/]+)\/code\/?$/);
  if (m) return decodeURIComponent(m[1]).trim();
  return '';
}

function parseRequestTokens(url, body) {
  if (body?.designTokens && typeof body.designTokens === 'object') {
    return sanitizeBrandTokens(body.designTokens);
  }
  const fromQuery = {};
  if (url.searchParams.has('brandName')) fromQuery.brandName = url.searchParams.get('brandName');
  if (url.searchParams.has('stiffness')) fromQuery.springStiffness = url.searchParams.get('stiffness');
  if (url.searchParams.has('damping')) fromQuery.springDamping = url.searchParams.get('damping');
  if (url.searchParams.has('durationScale')) fromQuery.durationScale = url.searchParams.get('durationScale');
  if (url.searchParams.has('bezier')) fromQuery.bezierCurve = url.searchParams.get('bezier');
  if (url.searchParams.has('reducedMotion')) fromQuery.reducedMotionPolicy = url.searchParams.get('reducedMotion');
  return Object.keys(fromQuery).length ? sanitizeBrandTokens(fromQuery) : null;
}

export default async function handler(req) {
  if (req.method === 'OPTIONS') return corsPreflight();
  if (req.method !== 'GET' && req.method !== 'POST') {
    return errorResponse('Method not allowed. Use GET or POST /api/v1/motions/:id/code.', 405);
  }

  const rawKey = extractApiKey(req);
  const auth = verifyApiKey(rawKey);
  if (!auth.valid) {
    return errorResponse(auth.error || 'Authentication required.', 401, {
      hint: 'Pass Authorization: Bearer <API_KEY> or X-API-Key header. Generate a free or sandbox key via POST /api/v1/keys/issue or on the Pricing page.',
      docsUrl: `${getBaseUrl(req)}/#agents`,
    });
  }

  let body = null;
  if (req.method === 'POST') {
    try {
      body = await req.json();
    } catch {
      body = null;
    }
  }

  const url = new URL(req.url);
  const id = parseMotionId(req, url, body);
  if (!id) {
    return errorResponse('Missing motion id. Use /api/v1/motions/:id/code or ?id=<motion_id>.', 400);
  }

  const motion = getMotionById(id);
  if (!motion) {
    return errorResponse(`Motion "${id}" not found.`, 404, { id });
  }

  const meter = consumeQuota(auth.claims, 'code_fetch');
  if (!meter.allowed) {
    return errorResponse(
      meter.error,
      meter.status || 429,
      {
        tier: meter.tier,
        remaining: meter.remaining,
        limit: meter.limit,
        resetAt: meter.resetAt,
        upgradeUrl: `${getBaseUrl(req)}/#pricing`,
      },
      meter.headers
    );
  }

  const stack = body?.stack || url.searchParams.get('stack') || motion.stack;
  const requestTokens = parseRequestTokens(url, body);
  const accountBrandTokens = auth.claims.brandTokens || null;

  const payload = buildMotionCodePayload(motion, {
    stack,
    accountBrandTokens,
    requestBrandTokens: requestTokens,
    baseUrl: getBaseUrl(req),
  });

  return jsonResponse(
    {
      ...payload,
      supportedStacks: SUPPORTED_TARGET_STACKS,
      tier: auth.claims.tier,
      keyMode: auth.mode,
      quota: {
        tier: meter.tier,
        costCredits: meter.cost,
        remaining: meter.remaining,
        limit: meter.limit,
        resetAt: meter.resetAt,
      },
    },
    200,
    meter.headers
  );
}
