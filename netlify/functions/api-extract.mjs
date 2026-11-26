import crypto from 'node:crypto';
import {
  buildQuotaHeaders,
  consumeQuota,
  corsPreflight,
  CREDIT_COSTS,
  errorResponse,
  extractApiKey,
  getBaseUrl,
  getQuotaSnapshot,
  jsonResponse,
  sanitizeBrandTokens,
  verifyApiKey,
} from './lib/auth.mjs';
import { normalizeTargetStack } from './lib/catalog.mjs';

// In-process job store (warm instance lookup + test inspection)
const jobsStore = new Map();

export function resetExtractJobs() {
  jobsStore.clear();
}

function isValidHttpUrl(value) {
  if (!value || typeof value !== 'string') return false;
  try {
    const u = new URL(value.trim());
    return u.protocol === 'http:' || u.protocol === 'https:';
  } catch {
    return false;
  }
}

function parseJobId(url) {
  const qJob = url.searchParams.get('jobId') || url.searchParams.get('id');
  if (qJob) return qJob.trim();
  const m = url.pathname.match(/\/api\/v1\/extract\/([^/]+)\/?$/);
  if (m) return decodeURIComponent(m[1]).trim();
  return '';
}

export default async function handler(req) {
  if (req.method === 'OPTIONS') return corsPreflight();
  if (req.method !== 'GET' && req.method !== 'POST') {
    return errorResponse('Method not allowed. Use GET or POST /api/v1/extract.', 405);
  }

  const rawKey = extractApiKey(req);
  const auth = verifyApiKey(rawKey);
  if (!auth.valid) {
    return errorResponse(auth.error || 'Authentication required.', 401, {
      hint: 'Pass Authorization: Bearer <API_KEY> or X-API-Key header.',
    });
  }

  const url = new URL(req.url);
  const baseUrl = getBaseUrl(req);

  if (req.method === 'GET') {
    const jobId = parseJobId(url);
    const snapshot = getQuotaSnapshot(auth.claims);
    const headers = buildQuotaHeaders({
      tier: auth.claims.tier,
      remaining: auth.claims.tier === 'credits' ? snapshot.credits.remaining : snapshot.extract.remaining,
      limit: auth.claims.tier === 'credits' ? snapshot.credits.total : snapshot.extract.limit,
      creditsRemaining: auth.claims.tier === 'credits' ? snapshot.credits.remaining : undefined,
    });

    if (jobId) {
      const job = jobsStore.get(jobId);
      if (!job || job.sub !== auth.claims.sub) {
        return errorResponse(`Extraction job "${jobId}" not found for this API key.`, 404, { jobId }, headers);
      }
      return jsonResponse({ job, quota: snapshot }, 200, headers);
    }

    const userJobs = [...jobsStore.values()]
      .filter((j) => j.sub === auth.claims.sub)
      .sort((a, b) => b.createdAt.localeCompare(a.createdAt))
      .slice(0, 25);

    return jsonResponse(
      {
        count: userJobs.length,
        creditCostPerJob: CREDIT_COSTS.custom_extract,
        jobs: userJobs,
        quota: snapshot,
      },
      200,
      headers
    );
  }

  // POST /api/v1/extract
  let body;
  try {
    body = await req.json();
  } catch {
    return errorResponse('Invalid JSON request body.', 400);
  }

  const targetUrl = body?.url ? String(body.url).trim() : '';
  const videoUrl = body?.videoUrl ? String(body.videoUrl).trim() : '';
  if (!targetUrl && !videoUrl) {
    return errorResponse('Provide either "url" (live web page) or "videoUrl" (MP4/MOV/WebM recording).', 400);
  }
  if (targetUrl && !isValidHttpUrl(targetUrl)) {
    return errorResponse('Field "url" must be a valid http(s) URL.', 400);
  }
  if (videoUrl && !isValidHttpUrl(videoUrl)) {
    return errorResponse('Field "videoUrl" must be a valid http(s) URL.', 400);
  }

  const meter = consumeQuota(auth.claims, 'custom_extract');
  if (!meter.allowed) {
    return errorResponse(
      meter.error,
      meter.status || 402,
      {
        tier: meter.tier,
        creditCost: CREDIT_COSTS.custom_extract,
        remaining: meter.remaining,
        limit: meter.limit,
        resetAt: meter.resetAt,
        upgradeUrl: `${baseUrl}/#pricing`,
      },
      meter.headers
    );
  }

  const targetStack = normalizeTargetStack(body?.stack, 'React/Motion');
  const brandTokens = sanitizeBrandTokens({
    ...(auth.claims.brandTokens || {}),
    ...(body?.designTokens || {}),
  });

  const jobId = `ext_${crypto.randomBytes(8).toString('hex')}`;
  const nowIso = new Date().toISOString();
  const job = {
    jobId,
    status: 'queued',
    sub: auth.claims.sub,
    tier: auth.claims.tier,
    keyMode: auth.mode,
    sourceType: videoUrl ? 'video' : 'url',
    url: targetUrl || null,
    videoUrl: videoUrl || null,
    targetStack,
    notes: typeof body?.notes === 'string' ? body.notes.trim().slice(0, 500) : null,
    brandTokens: brandTokens || null,
    pipeline: [
      { step: 'capture_frames', status: 'queued', detail: videoUrl ? 'Decode 60fps keyframes from source recording' : 'Headless browser interaction capture at 60fps' },
      { step: 'optical_flow_curve_fit', status: 'pending', detail: 'Estimate spring (k, c) or cubic-bezier timing curve & beat windows' },
      { step: 'choreography_synthesis', status: 'pending', detail: 'Compile structured Motion IR and choreography beat timeline' },
      { step: 'stack_codegen', status: 'pending', detail: `Emit ${targetStack} implementation${brandTokens ? ' with Brand Motion Tokens' : ''}` },
    ],
    estimatedSeconds: videoUrl ? 18 : 25,
    createdAt: nowIso,
    pollUrl: `${baseUrl}/api/v1/extract/${jobId}`,
  };

  jobsStore.set(jobId, job);

  return jsonResponse(
    {
      job,
      billing: {
        tier: meter.tier,
        creditsCharged: meter.cost,
        remaining: meter.remaining,
        limit: meter.limit,
        resetAt: meter.resetAt,
      },
    },
    202,
    meter.headers
  );
}
