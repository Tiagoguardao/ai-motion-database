# Motion Index — Monetization, Metered API & MCP Architecture

This document covers the 4-tier monetization model, stateless HMAC-SHA256 API keys, Stripe billing integration, Netlify Functions REST API, and MCP server setup for Motion Index.

---

## 1. Monetization Tiers

| Tier | Pricing | Library Browsing & Previews | Code & Prompt Extractions | Custom URL / Video Extractions | Extras |
| --- | --- | --- | --- | --- | --- |
| **Free** | `$0` | Unlimited | `10 / month` | — | Physics specs always free |
| **Pro (Builder)** | `$19/mo` (`$15/mo` annual) | Unlimited | Unlimited (CSS, React/Motion, GSAP, SwiftUI, Remotion) | `30 / month` | Personal API key + MCP access + saved collections |
| **API / Credits** | `$15 / 500`, `$49 / 2,000`, `$149 / 7,500` | Unlimited | `1 credit / fetch` | `10 credits / job` | Pay-as-you-go for AI app builders & agencies |
| **Teams / Brand Motion** | `$149/mo` (`$119/mo` annual) | Unlimited | Unlimited | `150 / month` | Private libraries + shared **Brand Motion Tokens** enforced via MCP & API |

---

## 2. Stateless API Keys (`netlify/functions/lib/auth.mjs`)

API keys are signed with HMAC-SHA256 using `MOTION_INDEX_SIGNING_SECRET`:

```text
mi_<live|test>_<base64url(JSON claims)>.<base64url(HMAC-SHA256)>
```

Claims encoded inside each key:

```json
{
  "tier": "teams",
  "sub": "team@acme.dev",
  "quota": { "code": null, "extract": 150 },
  "credits": 0,
  "brandTokens": {
    "brandName": "Acme Design System",
    "springStiffness": 310,
    "springDamping": 26,
    "durationScale": 0.9,
    "bezierCurve": [0.2, 0.8, 0.2, 1],
    "reducedMotionPolicy": "respect"
  },
  "iat": 1764160000
}
```

Verification uses `crypto.timingSafeEqual`. Every metered response returns:

- `X-MotionIndex-Tier`
- `X-MotionIndex-Quota-Remaining`
- `X-MotionIndex-Quota-Limit`
- `X-MotionIndex-Credits-Remaining` (for `credits` tier)

---

## 3. REST API Endpoints (`netlify/functions/` + `netlify.toml`)

### Discovery (Public / Free)
`GET /api/v1/motions`

Query parameters: `q`, `use` (or `pattern`), `stack`, `trigger`, `feel`, `collection`, `app`, `limit` (default `24`, max `100`), `offset`.

```bash
curl "https://ai-motion-database.netlify.app/api/v1/motions?q=progress&app=duolingo&limit=5"
```

### Metered Motion Code & Adaptation
`GET /api/v1/motions/:id/code?stack=React/Motion` (or `POST` with JSON `{ id, stack, designTokens }`)

Headers: `Authorization: Bearer <API_KEY>` or `X-API-Key: <API_KEY>`.

Supported target stacks: `CSS`, `React/Motion`, `GSAP`, `SwiftUI`, `Remotion`.

```bash
curl -H "Authorization: Bearer $MOTION_INDEX_API_KEY" \
  "https://ai-motion-database.netlify.app/api/v1/motions/app-duolingo-progress-surge/code?stack=React/Motion"
```

### Metered Custom URL / Video Extraction
`POST /api/v1/extract` & `GET /api/v1/extract/:jobId`

Costs `10 credits` on the `credits` tier or `1 monthly slot` on `pro` (30/mo) / `teams` (150/mo).

```bash
curl -X POST https://ai-motion-database.netlify.app/api/v1/extract \
  -H "Authorization: Bearer $MOTION_INDEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://linear.app","stack":"React/Motion"}'
```

### Billing & Key Provisioning
- `POST /api/v1/checkout` — Creates a Stripe Checkout Session when `STRIPE_SECRET_KEY` + matching price ID are set; otherwise falls back to **Sandbox mode** and immediately returns a signed `mi_test_...` key for end-to-end testing.
- `POST /api/v1/portal` — Opens a Stripe Billing Portal session (or returns sandbox status).
- `POST /api/v1/webhooks/stripe` — Verifies `Stripe-Signature` (`t=...,v1=...`) via HMAC-SHA256 when `STRIPE_WEBHOOK_SECRET` is configured and handles `checkout.session.completed`.
- `POST /api/v1/keys/issue` — Issues a free or sandbox API key (with optional `brandTokens`).
- `POST /api/v1/keys/verify` — Verifies any API key and returns decoded claims + quota snapshot.

### Hosted Streamable HTTP MCP Endpoint
`POST /api/mcp` (JSON-RPC 2.0) and `GET /api/mcp` (server metadata).

---

## 4. Stripe & Netlify Configuration

1. Copy `.env.example` to `.env` for local testing (`netlify dev`) or add these variables in **Netlify Site Settings -> Environment variables**:
   - `MOTION_INDEX_SIGNING_SECRET` — strong random 32+ byte secret
   - `MOTION_INDEX_BASE_URL` — `https://ai-motion-database.netlify.app`
   - `STRIPE_SECRET_KEY` — Stripe secret key (`sk_live_...` or `sk_test_...`)
   - `STRIPE_WEBHOOK_SECRET` — Webhook signing secret (`whsec_...`)
   - `STRIPE_PRICE_PRO_MONTHLY`, `STRIPE_PRICE_PRO_ANNUAL`
   - `STRIPE_PRICE_CREDITS_500`, `STRIPE_PRICE_CREDITS_2000`, `STRIPE_PRICE_CREDITS_7500`
   - `STRIPE_PRICE_TEAMS_MONTHLY`, `STRIPE_PRICE_TEAMS_ANNUAL`
2. In Stripe Dashboard -> Developers -> Webhooks, register `https://ai-motion-database.netlify.app/api/v1/webhooks/stripe` listening to `checkout.session.completed`, `customer.subscription.updated`, and `customer.subscription.deleted`.
3. When `STRIPE_SECRET_KEY` is unset, the live UI and API gracefully run in **Sandbox mode** so users can mint `mi_test_...` keys for every tier immediately.

---

## 5. MCP Server Installation

See [`mcp/README.md`](../mcp/README.md) for Claude Code, Cursor, and Codex configuration snippets.

Quick local verification:

```bash
npm run test:monetization
```
