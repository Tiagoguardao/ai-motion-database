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

export default async function handler(req) {
  if (req.method === 'OPTIONS') return corsPreflight();
  if (req.method !== 'GET') {
    return errorResponse('Method not allowed. Use GET /api/v1/motions.', 405);
  }

  const url = new URL(req.url);
  const rawKey = extractApiKey(req);
  let tier = 'free';
  if (rawKey) {
    const check = verifyApiKey(rawKey);
    if (check.valid) tier = check.claims.tier;
  }

  try {
    const result = searchMotions(
      {
        q: url.searchParams.get('q') || url.searchParams.get('query'),
        use: url.searchParams.get('use'),
        pattern: url.searchParams.get('pattern'),
        stack: url.searchParams.get('stack'),
        trigger: url.searchParams.get('trigger'),
        feel: url.searchParams.get('feel'),
        collection: url.searchParams.get('collection'),
        app: url.searchParams.get('app'),
        limit: url.searchParams.get('limit'),
        offset: url.searchParams.get('offset'),
      },
      getBaseUrl(req)
    );

    return jsonResponse(
      result,
      200,
      {
        ...buildQuotaHeaders({ tier, remaining: 'unlimited' }),
        'Cache-Control': 'public, max-age=120',
      }
    );
  } catch (err) {
    return errorResponse('Failed to query motion catalog.', 500, { detail: err.message });
  }
}
