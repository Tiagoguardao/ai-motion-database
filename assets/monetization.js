/* ---------- Motion Index Monetization, Metering, API Key & MCP UI ---------- */
(function () {
  const FREE_MONTHLY_LIMIT = 10;
  const STORAGE_ACCOUNT = 'mi_account_v1';
  const STORAGE_USAGE = 'mi_free_usage_v1';
  const STORAGE_TOKENS = 'mi_brand_tokens_v1';

  const DEFAULT_TOKENS = {
    brandName: 'Acme Design System',
    springStiffness: 280,
    springDamping: 26,
    durationScale: 1.0,
    bezierCurve: [0.2, 0.8, 0.2, 1],
    reducedMotionPolicy: 'respect',
  };

  const CREDIT_PACKS = [
    { id: 'credits_500', label: '500 cr', credits: 500, price: 15 },
    { id: 'credits_2000', label: '2,000 cr', credits: 2000, price: 49 },
    { id: 'credits_7500', label: '7,500 cr', credits: 7500, price: 149 },
  ];

  const uiState = {
    billing: 'monthly', // 'monthly' | 'annual'
    selectedPack: 'credits_500',
    modalTab: 'plan', // 'plan' | 'mcp' | 'tokens'
    mcpClient: 'claude', // 'claude' | 'cursor' | 'codex' | 'http'
    agentsTab: 'mcp', // 'mcp' | 'rest' | 'tokens'
    revealKey: false,
  };

  const $ = (id) => document.getElementById(id);
  const esc = (s) =>
    String(s ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

  function getApiOrigin() {
    if (location.protocol === 'http:' || location.protocol === 'https:') {
      return location.origin;
    }
    return 'https://ai-motion-database.netlify.app';
  }

  function currentMonthKey() {
    const d = new Date();
    return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}`;
  }

  /* ---------- Local Storage State ---------- */
  function readJson(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  }

  function writeJson(key, val) {
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch {
      // ignore private browsing quota errors
    }
  }

  function getAccount() {
    const acc = readJson(STORAGE_ACCOUNT, null);
    if (!acc || typeof acc !== 'object') {
      return { tier: 'free', mode: 'sandbox', apiKey: '', credits: 0, sub: '', brandTokens: null };
    }
    return acc;
  }

  function saveAccount(acc) {
    writeJson(STORAGE_ACCOUNT, acc);
    if (acc.brandTokens) saveBrandTokens(acc.brandTokens);
    renderPlanPill();
    updateSheetQuotaMeta();
    renderAgentsInteractive();
    if ($('pricingView') && !$('pricingView').hidden) renderPricingView();
  }

  function getBrandTokens() {
    const saved = readJson(STORAGE_TOKENS, null);
    return { ...DEFAULT_TOKENS, ...(saved || {}) };
  }

  function saveBrandTokens(tokens) {
    writeJson(STORAGE_TOKENS, { ...DEFAULT_TOKENS, ...tokens });
  }

  function getFreeUsage() {
    const month = currentMonthKey();
    const u = readJson(STORAGE_USAGE, { month, ids: [] });
    if (!u || u.month !== month || !Array.isArray(u.ids)) {
      return { month, ids: [] };
    }
    return u;
  }

  function recordFreeExtraction(motionId) {
    const u = getFreeUsage();
    if (!u.ids.includes(motionId)) {
      u.ids.push(motionId);
      writeJson(STORAGE_USAGE, u);
    }
    renderPlanPill();
    updateSheetQuotaMeta();
    return u;
  }

  function isUnlimitedTier(acc) {
    return acc.tier === 'pro' || acc.tier === 'teams' || acc.tier === 'credits';
  }

  function maskKey(key) {
    if (!key) return 'No API key saved';
    if (uiState.revealKey) return key;
    if (key.length <= 22) return key;
    return `${key.slice(0, 14)}••••••••••••••••${key.slice(-6)}`;
  }

  /* ---------- Offline-safe Sandbox Key Helper ---------- */
  function decodeKeyPayloadClient(key) {
    const m = String(key || '')
      .trim()
      .match(/^mi_(live|test)_([A-Za-z0-9_-]+)\.([A-Za-z0-9_-]+)$/);
    if (!m) return null;
    try {
      const b64 = m[2].replace(/-/g, '+').replace(/_/g, '/');
      const padded = b64 + '='.repeat((4 - (b64.length % 4)) % 4);
      const claims = JSON.parse(atob(padded));
      return { mode: m[1], claims };
    } catch {
      return null;
    }
  }

  function makeLocalFallbackKey(tier, credits, brandTokens) {
    const claims = {
      tier,
      sub: 'local-sandbox@motionindex.dev',
      quota: {
        code: tier === 'free' ? FREE_MONTHLY_LIMIT : null,
        extract: tier === 'pro' ? 30 : tier === 'teams' ? 150 : 0,
      },
      credits: tier === 'credits' ? credits || 500 : 0,
      brandTokens: tier === 'teams' ? brandTokens || getBrandTokens() : null,
      iat: Math.floor(Date.now() / 1000),
    };
    const b64 = btoa(JSON.stringify(claims)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
    return { apiKey: `mi_test_${b64}.local_preview_sig`, claims, mode: 'sandbox' };
  }

  async function postApi(path, body, apiKeyOverride) {
    const headers = { 'Content-Type': 'application/json' };
    const key = apiKeyOverride || getAccount().apiKey;
    if (key) headers.Authorization = `Bearer ${key}`;
    const res = await fetch(`${getApiOrigin()}${path}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body || {}),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data?.error || `Request failed (${res.status})`);
    return data;
  }

  async function issueSandboxKey(tier, opts = {}) {
    const credits = opts.credits || (tier === 'credits' ? 500 : 0);
    const brandTokens = opts.brandTokens || (tier === 'teams' ? getBrandTokens() : undefined);
    try {
      const data = await postApi('/api/v1/keys/issue', { tier, credits, brandTokens });
      const acc = {
        tier: data.claims.tier,
        mode: data.mode || 'sandbox',
        apiKey: data.apiKey,
        credits: data.claims.credits || 0,
        sub: data.claims.sub || '',
        brandTokens: data.claims.brandTokens || null,
      };
      saveAccount(acc);
      return { acc, source: 'api' };
    } catch {
      const fb = makeLocalFallbackKey(tier, credits, brandTokens);
      const acc = {
        tier: fb.claims.tier,
        mode: 'sandbox',
        apiKey: fb.apiKey,
        credits: fb.claims.credits || 0,
        sub: fb.claims.sub,
        brandTokens: fb.claims.brandTokens || null,
      };
      saveAccount(acc);
      return { acc, source: 'local' };
    }
  }

  async function startCheckout(planId) {
    try {
      const data = await postApi('/api/v1/checkout', {
        plan: planId,
        billing: uiState.billing,
        brandTokens: planId.startsWith('teams') ? getBrandTokens() : undefined,
      });
      if (data.checkoutUrl) {
        window.location.href = data.checkoutUrl;
        return;
      }
      if (data.apiKey && data.claims) {
        saveAccount({
          tier: data.claims.tier,
          mode: data.mode || 'sandbox',
          apiKey: data.apiKey,
          credits: data.claims.credits || 0,
          sub: data.claims.sub || '',
          brandTokens: data.claims.brandTokens || null,
        });
        openAccountModal('plan', data.message || `Activated ${data.label} sandbox key.`);
        return;
      }
    } catch {
      // Static / file:// fallback
      const tier = planId.startsWith('pro')
        ? 'pro'
        : planId.startsWith('teams')
          ? 'teams'
          : planId.startsWith('credits')
            ? 'credits'
            : 'free';
      const pack = CREDIT_PACKS.find((p) => p.id === planId);
      await issueSandboxKey(tier, { credits: pack ? pack.credits : 0 });
      openAccountModal('plan', `Activated local ${tier.toUpperCase()} preview key (run on Netlify for live Stripe Checkout).`);
    }
  }

  async function verifyAndSaveKey(rawKey) {
    const trimmed = String(rawKey || '').trim();
    if (!trimmed) throw new Error('Paste an API key starting with mi_live_ or mi_test_.');
    try {
      const data = await postApi('/api/v1/keys/verify', { apiKey: trimmed }, trimmed);
      const acc = {
        tier: data.claims.tier,
        mode: data.mode || 'live',
        apiKey: trimmed,
        credits: data.claims.credits || 0,
        sub: data.claims.sub || '',
        brandTokens: data.claims.brandTokens || null,
      };
      saveAccount(acc);
      return acc;
    } catch (apiErr) {
      const parsed = decodeKeyPayloadClient(trimmed);
      if (parsed && parsed.claims && parsed.claims.tier) {
        const acc = {
          tier: parsed.claims.tier,
          mode: parsed.mode,
          apiKey: trimmed,
          credits: parsed.claims.credits || 0,
          sub: parsed.claims.sub || '',
          brandTokens: parsed.claims.brandTokens || null,
        };
        saveAccount(acc);
        return acc;
      }
      throw apiErr;
    }
  }

  /* ---------- Config Snippet Generators ---------- */
  function getMcpSnippet(client) {
    const acc = getAccount();
    const key = acc.apiKey || 'mi_test_your_api_key_here';
    const origin = getApiOrigin();
    if (client === 'claude') {
      return `# Claude Code — Hosted HTTP MCP (recommended)\nclaude mcp add --transport http motion-index \\\n  ${origin}/api/mcp \\\n  --header "Authorization: Bearer ${key}"\n\n# Or local stdio MCP from this repo\nclaude mcp add motion-index \\\n  -e MOTION_INDEX_API_KEY="${key}" \\\n  -- node /path/to/ai-motion-database/mcp/server.mjs`;
    }
    if (client === 'cursor') {
      return JSON.stringify(
        {
          mcpServers: {
            'motion-index': {
              command: 'node',
              args: ['/path/to/ai-motion-database/mcp/server.mjs'],
              env: {
                MOTION_INDEX_API_KEY: key,
                MOTION_INDEX_API_URL: origin,
              },
            },
          },
        },
        null,
        2
      );
    }
    if (client === 'codex') {
      return `[mcp_servers.motion_index]\ncommand = "node"\nargs = ["/path/to/ai-motion-database/mcp/server.mjs"]\n\n[mcp_servers.motion_index.env]\nMOTION_INDEX_API_KEY = "${key}"\nMOTION_INDEX_API_URL = "${origin}"`;
    }
    return `curl -X POST ${origin}/api/mcp \\\n  -H "Content-Type: application/json" \\\n  -H "Authorization: Bearer ${key}" \\\n  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'`;
  }

  function getRestSnippets() {
    const acc = getAccount();
    const key = acc.apiKey || 'mi_test_your_api_key_here';
    const origin = getApiOrigin();
    const sampleId = (window.__MOTION_DB && window.__MOTION_DB[0] && window.__MOTION_DB[0].id) || 'app-duolingo-progress-surge';
    return `# 1. Search catalog (public & free)\ncurl "${origin}/api/v1/motions?q=progress&limit=5"\n\n# 2. Fetch Motion IR + stack-adapted code (CSS | React/Motion | GSAP | SwiftUI | Remotion)\ncurl -H "Authorization: Bearer ${key}" \\\n  "${origin}/api/v1/motions/${sampleId}/code?stack=React/Motion"\n\n# 3. Queue custom URL/video extraction (Pro 30/mo · Teams 150/mo · Credits 10 cr)\ncurl -X POST "${origin}/api/v1/extract" \\\n  -H "Authorization: Bearer ${key}" \\\n  -H "Content-Type: application/json" \\\n  -d '{"url":"https://linear.app","stack":"React/Motion"}'`;
  }

  async function copyText(text, btn, doneLabel = 'Copied ✓') {
    const prev = btn ? btn.textContent : '';
    try {
      await navigator.clipboard.writeText(text);
      if (btn) btn.textContent = doneLabel;
    } catch {
      if (btn) btn.textContent = 'Copy failed';
    }
    if (btn) setTimeout(() => (btn.textContent = prev), 1500);
  }

  /* ---------- Sidebar Plan & API Key Pill ---------- */
  function renderPlanPill() {
    const mount = $('planPillMount');
    if (!mount) return;
    const acc = getAccount();
    const usage = getFreeUsage();
    const rem = Math.max(0, FREE_MONTHLY_LIMIT - usage.ids.length);

    let tierLabel = 'Free';
    let meta = `${rem}/${FREE_MONTHLY_LIMIT} extractions left`;
    if (acc.tier === 'pro') {
      tierLabel = 'Pro Builder';
      meta = 'Unlimited code · 30 extracts/mo';
    } else if (acc.tier === 'credits') {
      tierLabel = 'API Credits';
      meta = `${acc.credits || 0} credits available`;
    } else if (acc.tier === 'teams') {
      tierLabel = 'Teams';
      meta = 'Brand Motion Tokens active';
    }

    mount.innerHTML = `
      <button type="button" class="mi-plan-pill" id="miOpenAccountBtn" aria-label="Manage plan and API key">
        <span class="mi-plan-pill-left">
          <span class="mi-plan-pill-tier">
            <span class="mi-plan-dot" data-tier="${esc(acc.tier)}"></span>
            ${esc(tierLabel)}
          </span>
          <span class="mi-plan-pill-meta">${esc(meta)}</span>
        </span>
        <span class="mi-plan-pill-action">API Key</span>
      </button>
    `;
    $('miOpenAccountBtn').onclick = () => openAccountModal('plan');
  }

  /* ---------- Detail Sheet Metering & Share for Agent ---------- */
  function updateSheetQuotaMeta() {
    const el = $('d-quota-meta');
    if (!el || !window.__MOTION_UI) return;
    const current = window.__MOTION_UI.getCurrent();
    const tab = window.__MOTION_UI.getTab();
    if (!current) {
      el.innerHTML = '';
      return;
    }

    const acc = getAccount();
    if (tab === 'spec') {
      el.innerHTML = `
        <span>Motion specs are always 100% free &amp; unmetered</span>
        <span class="sheet-quota-links"><button type="button" id="miSheetKeyLink">API Key</button></span>
      `;
    } else if (acc.tier === 'teams') {
      const bt = acc.brandTokens || getBrandTokens();
      el.innerHTML = `
        <span>Teams · Brand Tokens (${esc(bt.brandName || 'Active')}, k=${bt.springStiffness}, c=${bt.springDamping})</span>
        <span class="sheet-quota-links"><button type="button" id="miSheetKeyLink">Tokens</button></span>
      `;
    } else if (acc.tier === 'pro') {
      el.innerHTML = `
        <span>Pro Builder · Unlimited code &amp; prompt extractions</span>
        <span class="sheet-quota-links"><button type="button" id="miSheetKeyLink">MCP Key</button></span>
      `;
    } else if (acc.tier === 'credits') {
      el.innerHTML = `
        <span>API Credits · ${acc.credits || 0} cr (1 cr/API fetch)</span>
        <span class="sheet-quota-links"><button type="button" id="miSheetKeyLink">Manage</button></span>
      `;
    } else {
      const usage = getFreeUsage();
      const rem = Math.max(0, FREE_MONTHLY_LIMIT - usage.ids.length);
      const alreadyCounted = usage.ids.includes(current.id);
      el.innerHTML = `
        <span>Free plan · ${rem} of ${FREE_MONTHLY_LIMIT} extractions left this month${alreadyCounted ? ' (already unlocked)' : ''}</span>
        <span class="sheet-quota-links">
          <button type="button" id="miSheetUpgradeLink">Upgrade</button>
          <button type="button" id="miSheetKeyLink">API Key</button>
        </span>
      `;
    }

    const keyLink = $('miSheetKeyLink');
    if (keyLink) keyLink.onclick = () => openAccountModal(acc.tier === 'teams' ? 'tokens' : 'plan');
    const upLink = $('miSheetUpgradeLink');
    if (upLink) {
      upLink.onclick = () => {
        if ($('sheet') && $('sheet').open) $('sheet').close();
        window.__MOTION_UI.setView('pricing');
      };
    }
  }

  // Called by build_site.py right before copying from the detail sheet
  window.__MOTION_COPY_GUARD = function (motion, tab, rawText) {
    // Specs are always free and unmetered
    if (tab === 'spec') return { allowed: true, text: rawText };

    const acc = getAccount();
    if (isUnlimitedTier(acc)) {
      if (acc.tier === 'teams') {
        const bt = acc.brandTokens || getBrandTokens();
        const suffix =
          tab === 'prompt'
            ? `\n\n[BRAND MOTION TOKENS — ${bt.brandName || 'Team'}]\nSpring: stiffness=${bt.springStiffness}, damping=${bt.springDamping}\nDuration scale: ${bt.durationScale}x\nBezier: cubic-bezier(${(bt.bezierCurve || [0.2, 0.8, 0.2, 1]).join(', ')})\nReduced motion: ${bt.reducedMotionPolicy || 'respect'}`
            : rawText;
        return { allowed: true, text: tab === 'prompt' ? `${rawText}${suffix}` : rawText };
      }
      return { allowed: true, text: rawText };
    }

    const usage = getFreeUsage();
    if (usage.ids.includes(motion.id)) {
      return { allowed: true, text: rawText };
    }
    if (usage.ids.length >= FREE_MONTHLY_LIMIT) {
      openUpgradeModal(motion);
      return { allowed: false, text: rawText };
    }
    recordFreeExtraction(motion.id);
    return { allowed: true, text: rawText };
  };

  function bindShareForAgent() {
    const shareBtn = $('d-share');
    if (!shareBtn) return;
    shareBtn.onclick = () => {
      const m = window.__MOTION_UI && window.__MOTION_UI.getCurrent();
      if (!m) return;
      const url = `${getApiOrigin()}/#${m.id}`;
      const text = `Motion #${m.id} — pull into Claude Code / Cursor in 1 prompt: ${url}`;
      copyText(text, shareBtn, 'Copied agent link ✓');
    };
  }

  /* ---------- Pricing View ---------- */
  function renderPricingView() {
    const root = $('pricingView');
    if (!root) return;
    const acc = getAccount();
    const isAnnual = uiState.billing === 'annual';
    const proPrice = isAnnual ? 15 : 19;
    const teamsPrice = isAnnual ? 119 : 149;
    const selectedPack = CREDIT_PACKS.find((p) => p.id === uiState.selectedPack) || CREDIT_PACKS[0];
    const totalMotions = Array.isArray(window.__MOTION_DB) ? window.__MOTION_DB.length : 0;

    root.innerHTML = `
      <div class="mi-pricing">
        <div class="mi-pricing-head">
          <div>
            <h2>Browse everything free. Pay when your coding agents ship it.</h2>
            <p>All ${totalMotions ? `${totalMotions} ` : ''}live interactive motion stages and physics specs are 100% free to explore. Upgrade for unlimited extractions, MCP server access, metered API credits, or team-wide Brand Motion Tokens.</p>
          </div>
          <div class="mi-billing-toggle" role="group" aria-label="Billing cadence">
            <button type="button" data-cadence="monthly" aria-pressed="${!isAnnual}">Monthly</button>
            <button type="button" data-cadence="annual" aria-pressed="${isAnnual}">Annual <span class="mi-save-tag">−20%</span></button>
          </div>
        </div>

        <div class="mi-tier-grid">
          <article class="mi-tier-card">
            <div class="mi-tier-top">
              <div class="mi-tier-label-row">
                <h3 class="mi-tier-name">Free</h3>
                ${acc.tier === 'free' ? '<span class="mi-badge">Current</span>' : '<span class="mi-badge">Open</span>'}
              </div>
              <div class="mi-tier-price"><strong>$0</strong><span>/ forever</span></div>
              <p class="mi-tier-desc">Explore the entire live motion library, inspect physics specs, and pull starter prompts.</p>
              <ul class="mi-tier-features">
                <li>Full gallery browsing &amp; live interactive previews</li>
                <li>Unlimited Motion Specs (curves, springs, choreography)</li>
                <li>10 code / prompt extractions per month</li>
                <li>Public REST discovery API (<code>GET /api/v1/motions</code>)</li>
              </ul>
            </div>
            <div>
              <button type="button" class="mi-tier-cta" data-checkout="free">${acc.apiKey && acc.tier === 'free' ? 'View free API key' : 'Issue free API key'}</button>
              <p class="mi-tier-subnote">No credit card required</p>
            </div>
          </article>

          <article class="mi-tier-card" data-featured="true">
            <div class="mi-tier-top">
              <div class="mi-tier-label-row">
                <h3 class="mi-tier-name">Pro (Builder)</h3>
                <span class="mi-badge" data-accent="true">${acc.tier === 'pro' ? 'Active' : 'Most popular'}</span>
              </div>
              <div class="mi-tier-price"><strong>$${proPrice}</strong><span>/ mo${isAnnual ? ' · billed annually' : ''}</span></div>
              <p class="mi-tier-desc">Personal API key + MCP server for solo builders shipping crafted UI with Claude Code, Cursor &amp; Codex.</p>
              <ul class="mi-tier-features">
                <li>Personal API key + stdio &amp; HTTP MCP server access</li>
                <li>Unlimited library code extractions across CSS, React/Motion, GSAP, SwiftUI &amp; Remotion</li>
                <li>Saved collections &amp; stack presets</li>
                <li>30 custom URL / video motion extractions per month</li>
              </ul>
            </div>
            <div>
              <button type="button" class="mi-tier-cta" data-primary="true" data-checkout="${isAnnual ? 'pro_annual' : 'pro_monthly'}">${acc.tier === 'pro' ? 'Manage Pro key' : 'Start Pro Builder'}</button>
              <p class="mi-tier-subnote">Cancel anytime · instant sandbox test key</p>
            </div>
          </article>

          <article class="mi-tier-card">
            <div class="mi-tier-top">
              <div class="mi-tier-label-row">
                <h3 class="mi-tier-name">API / Credits</h3>
                <span class="mi-badge">${acc.tier === 'credits' ? `${acc.credits || 0} cr` : 'Usage-based'}</span>
              </div>
              <div class="mi-tier-price"><strong>$${selectedPack.price}</strong><span>/ ${selectedPack.credits.toLocaleString()} credits</span></div>
              <p class="mi-tier-desc">Pay-as-you-go metered API for AI app builders, design agencies &amp; automated pipelines.</p>
              <div class="mi-pack-picker" role="group" aria-label="Credit pack size">
                ${CREDIT_PACKS.map(
                  (p) => `<button type="button" data-pack="${p.id}" aria-pressed="${p.id === selectedPack.id}">$${p.price}<br>${p.label}</button>`
                ).join('')}
              </div>
              <ul class="mi-tier-features">
                <li>1 credit per library code + IR fetch</li>
                <li>10 credits per custom URL / video extraction job</li>
                <li>Works over REST API &amp; MCP server</li>
                <li>Credits never expire while account is active</li>
              </ul>
            </div>
            <div>
              <button type="button" class="mi-tier-cta" data-checkout="${selectedPack.id}">Buy ${selectedPack.credits.toLocaleString()} credits</button>
              <p class="mi-tier-subnote">$${(selectedPack.price / selectedPack.credits).toFixed(3)} / library fetch</p>
            </div>
          </article>

          <article class="mi-tier-card">
            <div class="mi-tier-top">
              <div class="mi-tier-label-row">
                <h3 class="mi-tier-name">Teams / Brand</h3>
                <span class="mi-badge" data-accent="true">${acc.tier === 'teams' ? 'Active' : 'Brand Physics'}</span>
              </div>
              <div class="mi-tier-price"><strong>$${teamsPrice}</strong><span>/ mo${isAnnual ? ' · billed annually' : ''}</span></div>
              <p class="mi-tier-desc">Private motion libraries + shared Brand Motion Tokens enforced across every engineer’s coding agent.</p>
              <ul class="mi-tier-features">
                <li>Everything in Pro + private team motion libraries</li>
                <li>Shared Brand Motion Tokens (spring k/c, duration scale, bezier curve, reduced-motion policy)</li>
                <li>Automatic token enforcement via MCP &amp; REST API</li>
                <li>150 custom URL / video extractions per month</li>
              </ul>
            </div>
            <div>
              <button type="button" class="mi-tier-cta" data-checkout="${isAnnual ? 'teams_annual' : 'teams_monthly'}">${acc.tier === 'teams' ? 'Edit Brand Tokens' : 'Start Teams'}</button>
              <p class="mi-tier-subnote">Consistent brand physics on every PR</p>
            </div>
          </article>
        </div>

        <div>
          <h3 class="mi-section-title">Compare tiers</h3>
          <div class="mi-table-wrap">
            <table class="mi-table">
              <thead>
                <tr>
                  <th>Capability</th>
                  <th>Free</th>
                  <th>Pro (Builder)</th>
                  <th>API / Credits</th>
                  <th>Teams / Brand</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Gallery browsing &amp; interactive previews</td>
                  <td><strong>Unlimited</strong></td>
                  <td><strong>Unlimited</strong></td>
                  <td><strong>Unlimited</strong></td>
                  <td><strong>Unlimited</strong></td>
                </tr>
                <tr>
                  <td>Physics &amp; choreography specs</td>
                  <td><strong>Unlimited</strong></td>
                  <td><strong>Unlimited</strong></td>
                  <td><strong>Unlimited</strong></td>
                  <td><strong>Unlimited</strong></td>
                </tr>
                <tr>
                  <td>Code &amp; prompt extractions</td>
                  <td>10 / month</td>
                  <td><strong>Unlimited</strong></td>
                  <td>1 credit / fetch</td>
                  <td><strong>Unlimited</strong></td>
                </tr>
                <tr>
                  <td>Stack adapters (CSS, React/Motion, GSAP, SwiftUI, Remotion)</td>
                  <td>Native stack</td>
                  <td><strong>All 5 stacks</strong></td>
                  <td><strong>All 5 stacks</strong></td>
                  <td><strong>All 5 stacks</strong></td>
                </tr>
                <tr>
                  <td>MCP server (Claude Code, Cursor, Codex)</td>
                  <td>Search only</td>
                  <td><strong>Full access</strong></td>
                  <td><strong>Metered</strong></td>
                  <td><strong>Full + Brand Tokens</strong></td>
                </tr>
                <tr>
                  <td>Custom URL / video extraction jobs</td>
                  <td>—</td>
                  <td><strong>30 / month</strong></td>
                  <td>10 credits / job</td>
                  <td><strong>150 / month</strong></td>
                </tr>
                <tr>
                  <td>Private libraries &amp; Brand Motion Tokens</td>
                  <td>—</td>
                  <td>Saved collections</td>
                  <td>Per-request overrides</td>
                  <td><strong>Shared org enforcement</strong></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <section class="mi-revshare" aria-labelledby="miRevshareTitle">
          <div>
            <h3 id="miRevshareTitle">Creator Rev-Share Program</h3>
            <p>Design engineers and motion craftspeople who publish original interaction packs or verified app breakdowns earn recurring revenue share whenever Pro, Credits, or Teams agents extract their motions.</p>
            <p>Submit a curated pack of 5+ interactive motions with clean extractable code and spring/bezier specs — keep full attribution and links to your site or X handle on every tile.</p>
            <div class="mi-revshare-stats">
              <span>50% net extraction pool</span>
              <span>Full author attribution</span>
              <span>Monthly Stripe payouts</span>
            </div>
          </div>
          <form class="mi-revshare-form" id="miCreatorForm">
            <div class="mi-form-row">
              <div class="mi-field">
                <label for="miCrHandle">Name or @handle</label>
                <input id="miCrHandle" type="text" required placeholder="@yourhandle">
              </div>
              <div class="mi-field">
                <label for="miCrStack">Primary stack</label>
                <select id="miCrStack">
                  <option>React/Motion</option>
                  <option>CSS / WAAPI</option>
                  <option>WebGL / GLSL</option>
                  <option>GSAP</option>
                  <option>SwiftUI</option>
                </select>
              </div>
            </div>
            <div class="mi-field">
              <label for="miCrUrl">Portfolio, X post, or GitHub repo URL</label>
              <input id="miCrUrl" type="url" required placeholder="https://x.com/...">
            </div>
            <button type="submit" class="mi-btn" data-primary="true">Apply for Creator Rev-Share</button>
            <div class="mi-status-note" id="miCrStatus"></div>
          </form>
        </section>

        <div>
          <h3 class="mi-section-title">Frequently asked questions</h3>
          <div class="mi-faq">
            <details>
              <summary>Is browsing the gallery still free?</summary>
              <p>Yes — browsing every motion, playing with every live interactive stage, and reading or copying the Motion Spec JSON is 100% free with no login required. Free users also get 10 code/prompt extractions every month.</p>
            </details>
            <details>
              <summary>How does MCP server integration work?</summary>
              <p>Connect Claude Code, Cursor, or Codex to our hosted HTTP endpoint (<code>/api/mcp</code>) or run the zero-dependency stdio server (<code>mcp/server.mjs</code>). Your agent gets <code>search_motions</code>, <code>get_motion_code</code>, and <code>extract_motion</code> directly in its tool list.</p>
            </details>
            <details>
              <summary>What are Brand Motion Tokens on the Teams plan?</summary>
              <p>Teams define one canonical physics profile — spring stiffness &amp; damping, duration scale, default cubic-bezier, and reduced-motion policy. Every API and MCP response automatically rewrites the Motion IR and adaptation instructions to match your brand.</p>
            </details>
            <details>
              <summary>How do API credits work compared to Pro?</summary>
              <p>Pro ($19/mo) is best for individual builders who want unlimited library pulls and 30 custom extractions/mo. API Credits ($15 / $49 / $149 packs) are pay-as-you-go for apps, agencies, and pipelines: 1 credit per library fetch, 10 credits per custom URL/video extraction.</p>
            </details>
          </div>
        </div>
      </div>
    `;

    root.querySelectorAll('[data-cadence]').forEach((btn) => {
      btn.onclick = () => {
        uiState.billing = btn.dataset.cadence;
        renderPricingView();
      };
    });

    root.querySelectorAll('[data-pack]').forEach((btn) => {
      btn.onclick = () => {
        uiState.selectedPack = btn.dataset.pack;
        renderPricingView();
      };
    });

    root.querySelectorAll('[data-checkout]').forEach((btn) => {
      btn.onclick = () => {
        const plan = btn.dataset.checkout;
        if (plan === 'free' && acc.apiKey && acc.tier === 'free') {
          openAccountModal('plan');
          return;
        }
        if (plan.startsWith('teams') && acc.tier === 'teams') {
          openAccountModal('tokens');
          return;
        }
        if (plan.startsWith('pro') && acc.tier === 'pro') {
          openAccountModal('plan');
          return;
        }
        startCheckout(plan);
      };
    });

    const form = $('miCreatorForm');
    if (form) {
      form.onsubmit = (e) => {
        e.preventDefault();
        const handle = $('miCrHandle').value.trim();
        const stack = $('miCrStack').value;
        const url = $('miCrUrl').value.trim();
        const apps = readJson('mi_creator_applications_v1', []);
        apps.push({ handle, stack, url, submittedAt: new Date().toISOString() });
        writeJson('mi_creator_applications_v1', apps);
        $('miCrStatus').textContent = `Application logged for ${handle} (${stack}). We review creator packs weekly.`;
        form.reset();
      };
    }
  }

  /* ---------- Upgraded For Agents View ---------- */
  function renderAgentsInteractive() {
    const mount = $('agentsInteractiveMount');
    if (!mount) return;
    const acc = getAccount();
    const tokens = acc.brandTokens || getBrandTokens();
    const tab = uiState.agentsTab;

    let bodyHtml = '';
    if (tab === 'mcp') {
      const snippet = getMcpSnippet(uiState.mcpClient);
      bodyHtml = `
        <div class="mi-agent-box">
          <div class="mi-subtabs">
            <div class="mi-subtab-group" role="tablist">
              <button type="button" data-ag-mcp="claude" aria-selected="${uiState.mcpClient === 'claude'}">Claude Code</button>
              <button type="button" data-ag-mcp="cursor" aria-selected="${uiState.mcpClient === 'cursor'}">Cursor</button>
              <button type="button" data-ag-mcp="codex" aria-selected="${uiState.mcpClient === 'codex'}">Codex</button>
              <button type="button" data-ag-mcp="http" aria-selected="${uiState.mcpClient === 'http'}">HTTP /api/mcp</button>
            </div>
            <button type="button" class="mi-copy-mini" id="miAgCopyBtn">Copy config</button>
          </div>
          <pre id="miAgCode">${esc(snippet)}</pre>
          <div class="mi-tool-list">
            <div class="mi-tool-item">
              <code>search_motions(query, …)</code>
              <p>Free discovery by query, pattern, trigger, feel, stack, or app. Returns compact IDs &amp; preview URLs.</p>
            </div>
            <div class="mi-tool-item">
              <code>get_motion_code(id, stack?, designTokens?)</code>
              <p>Returns Motion IR, extractable code &amp; stack adaptation for CSS, React/Motion, GSAP, SwiftUI, or Remotion.</p>
            </div>
            <div class="mi-tool-item">
              <code>extract_motion(url?, videoUrl?, stack?)</code>
              <p>Queues a custom URL or video extraction job (Pro 30/mo, Teams 150/mo, or 10 API credits).</p>
            </div>
          </div>
        </div>
      `;
    } else if (tab === 'rest') {
      const snippet = getRestSnippets();
      bodyHtml = `
        <div class="mi-agent-box">
          <div class="mi-subtabs">
            <span style="font:500 12px var(--mono);color:var(--mute)">REST API v1 · Auth via Authorization: Bearer or X-API-Key</span>
            <button type="button" class="mi-copy-mini" id="miAgCopyBtn">Copy curl</button>
          </div>
          <pre id="miAgCode">${esc(snippet)}</pre>
        </div>
      `;
    } else {
      const tokenSnippet = JSON.stringify(tokens, null, 2);
      bodyHtml = `
        <div class="mi-agent-box">
          <div class="mi-subtabs">
            <span style="font:500 12px var(--mono);color:var(--mute)">Teams Brand Motion Tokens · enforced automatically via MCP &amp; API</span>
            <div class="mi-btn-row">
              <button type="button" class="mi-copy-mini" id="miAgEditTokensBtn">Edit Brand Tokens</button>
              <button type="button" class="mi-copy-mini" id="miAgCopyBtn">Copy JSON</button>
            </div>
          </div>
          <pre id="miAgCode">${esc(tokenSnippet)}</pre>
        </div>
      `;
    }

    mount.innerHTML = `
      <div class="mi-agent-tabs" role="tablist">
        <button type="button" data-ag-tab="mcp" aria-selected="${tab === 'mcp'}">MCP Config</button>
        <button type="button" data-ag-tab="rest" aria-selected="${tab === 'rest'}">REST API (curl)</button>
        <button type="button" data-ag-tab="tokens" aria-selected="${tab === 'tokens'}">Brand Motion Tokens</button>
      </div>
      ${bodyHtml}
    `;

    mount.querySelectorAll('[data-ag-tab]').forEach((b) => {
      b.onclick = () => {
        uiState.agentsTab = b.dataset.agTab;
        renderAgentsInteractive();
      };
    });
    mount.querySelectorAll('[data-ag-mcp]').forEach((b) => {
      b.onclick = () => {
        uiState.mcpClient = b.dataset.agMcp;
        renderAgentsInteractive();
      };
    });
    const copyBtn = $('miAgCopyBtn');
    if (copyBtn) {
      copyBtn.onclick = () => copyText($('miAgCode').textContent, copyBtn);
    }
    const editBtn = $('miAgEditTokensBtn');
    if (editBtn) {
      editBtn.onclick = () => openAccountModal('tokens');
    }
  }

  /* ---------- Account / API Key / Brand Tokens Modal ---------- */
  function ensureModals() {
    if (!$('miAccountModal')) {
      const dlg = document.createElement('dialog');
      dlg.id = 'miAccountModal';
      dlg.className = 'mi-modal';
      dlg.setAttribute('aria-labelledby', 'miAccTitle');
      document.body.appendChild(dlg);
    }
    if (!$('miUpgradeModal')) {
      const up = document.createElement('dialog');
      up.id = 'miUpgradeModal';
      up.className = 'mi-modal';
      up.setAttribute('aria-labelledby', 'miUpTitle');
      document.body.appendChild(up);
    }
  }

  function renderAccountModal(notice = '') {
    ensureModals();
    const dlg = $('miAccountModal');
    const acc = getAccount();
    const tokens = acc.brandTokens || getBrandTokens();
    const tab = uiState.modalTab;

    let tabBody = '';
    if (tab === 'plan') {
      const usage = getFreeUsage();
      const rem = Math.max(0, FREE_MONTHLY_LIMIT - usage.ids.length);
      tabBody = `
        <div class="mi-key-card">
          <div class="mi-key-row">
            <strong>Active plan: ${esc(acc.tier.toUpperCase())}${acc.mode === 'sandbox' ? ' (Sandbox)' : ''}</strong>
            <span class="mi-badge">${acc.tier === 'free' ? `${rem}/${FREE_MONTHLY_LIMIT} left this month` : acc.tier === 'credits' ? `${acc.credits || 0} credits` : 'Unlimited code'}</span>
          </div>
          <div class="mi-key-code">${esc(maskKey(acc.apiKey))}</div>
          <div class="mi-btn-row">
            ${acc.apiKey ? `<button type="button" class="mi-btn" id="miToggleReveal">${uiState.revealKey ? 'Hide key' : 'Reveal key'}</button>` : ''}
            ${acc.apiKey ? `<button type="button" class="mi-btn" id="miCopyKeyBtn">Copy API key</button>` : ''}
            <button type="button" class="mi-btn" id="miPortalBtn">Manage billing</button>
            ${acc.apiKey ? `<button type="button" class="mi-btn" id="miResetKeyBtn">Reset to Free</button>` : ''}
          </div>
        </div>

        <div class="mi-field">
          <label for="miPasteKeyInput">Paste existing API key (mi_live_… or mi_test_…)</label>
          <div style="display:flex;gap:8px">
            <input id="miPasteKeyInput" type="text" placeholder="mi_live_... or mi_test_..." style="flex:1">
            <button type="button" class="mi-btn" data-primary="true" id="miVerifyKeyBtn">Save key</button>
          </div>
        </div>

        <div class="mi-field">
          <label>Quick sandbox keys (test any tier end-to-end)</label>
          <div class="mi-sandbox-grid">
            <button type="button" data-mint="free">Free key</button>
            <button type="button" data-mint="pro">Pro key</button>
            <button type="button" data-mint="credits">500 Credits</button>
            <button type="button" data-mint="teams">Teams key</button>
          </div>
        </div>

        <div class="mi-status-note" id="miModalStatus">${esc(notice)}</div>
      `;
    } else if (tab === 'mcp') {
      const snippet = getMcpSnippet(uiState.mcpClient);
      tabBody = `
        <div class="mi-subtabs">
          <div class="mi-subtab-group" role="tablist">
            <button type="button" data-mod-mcp="claude" aria-selected="${uiState.mcpClient === 'claude'}">Claude Code</button>
            <button type="button" data-mod-mcp="cursor" aria-selected="${uiState.mcpClient === 'cursor'}">Cursor</button>
            <button type="button" data-mod-mcp="codex" aria-selected="${uiState.mcpClient === 'codex'}">Codex</button>
            <button type="button" data-mod-mcp="http" aria-selected="${uiState.mcpClient === 'http'}">HTTP</button>
          </div>
          <button type="button" class="mi-copy-mini" id="miModCopyMcp">Copy snippet</button>
        </div>
        <pre id="miModMcpCode">${esc(snippet)}</pre>
        <p style="margin:0;font-size:12.5px;color:var(--mute)">Your active API key is automatically embedded above. Need a key first? Switch to <strong>Plan &amp; API Key</strong> and generate one in 1 click.</p>
      `;
    } else {
      const bezStr = Array.isArray(tokens.bezierCurve) ? tokens.bezierCurve.join(', ') : '0.2, 0.8, 0.2, 1';
      tabBody = `
        <p style="margin:0;font-size:13.5px;color:var(--mute)">Configure your team’s canonical motion physics. On the Teams tier, these tokens are signed into your API key and enforced automatically across MCP and REST code extractions.</p>
        <form id="miTokensForm" style="display:flex;flex-direction:column;gap:12px">
          <div class="mi-field">
            <label for="miBtName">Brand / Design System name</label>
            <input id="miBtName" type="text" value="${esc(tokens.brandName || '')}">
          </div>
          <div class="mi-form-row">
            <div class="mi-field">
              <label for="miBtK">Spring stiffness (k)</label>
              <input id="miBtK" type="number" min="40" max="1200" step="10" value="${esc(tokens.springStiffness)}">
            </div>
            <div class="mi-field">
              <label for="miBtC">Spring damping (c)</label>
              <input id="miBtC" type="number" min="4" max="120" step="1" value="${esc(tokens.springDamping)}">
            </div>
          </div>
          <div class="mi-form-row">
            <div class="mi-field">
              <label for="miBtScale">Duration scale (0.25x–2.5x)</label>
              <input id="miBtScale" type="number" min="0.25" max="2.5" step="0.05" value="${esc(tokens.durationScale)}">
            </div>
            <div class="mi-field">
              <label for="miBtRm">Reduced-motion policy</label>
              <select id="miBtRm">
                <option value="respect" ${tokens.reducedMotionPolicy === 'respect' ? 'selected' : ''}>respect (prefers-reduced-motion)</option>
                <option value="crossfade" ${tokens.reducedMotionPolicy === 'crossfade' ? 'selected' : ''}>crossfade (150ms opacity)</option>
                <option value="instant" ${tokens.reducedMotionPolicy === 'instant' ? 'selected' : ''}>instant (0ms snap)</option>
              </select>
            </div>
          </div>
          <div class="mi-field">
            <label for="miBtBez">Default cubic-bezier (x1, y1, x2, y2)</label>
            <input id="miBtBez" type="text" value="${esc(bezStr)}">
          </div>
          <div class="mi-btn-row">
            <button type="submit" class="mi-btn" data-primary="true">Save Brand Motion Tokens</button>
            <button type="button" class="mi-btn" id="miSaveAndMintTeams">Save &amp; issue Teams key</button>
          </div>
          <div class="mi-status-note" id="miModalStatus">${esc(notice)}</div>
        </form>
      `;
    }

    dlg.innerHTML = `
      <div class="mi-modal-head">
        <h3 id="miAccTitle">API Key, Billing &amp; Brand Motion Tokens</h3>
        <button type="button" class="mi-modal-close" id="miCloseAcc">Close</button>
      </div>
      <div class="mi-modal-tabs" role="tablist">
        <button type="button" data-mtab="plan" aria-selected="${tab === 'plan'}">Plan &amp; API Key</button>
        <button type="button" data-mtab="mcp" aria-selected="${tab === 'mcp'}">MCP Config</button>
        <button type="button" data-mtab="tokens" aria-selected="${tab === 'tokens'}">Brand Motion Tokens</button>
      </div>
      <div class="mi-modal-body">${tabBody}</div>
    `;

    $('miCloseAcc').onclick = () => dlg.close();
    dlg.querySelectorAll('[data-mtab]').forEach((b) => {
      b.onclick = () => {
        uiState.modalTab = b.dataset.mtab;
        renderAccountModal();
      };
    });

    if ($('miToggleReveal')) {
      $('miToggleReveal').onclick = () => {
        uiState.revealKey = !uiState.revealKey;
        renderAccountModal();
      };
    }
    if ($('miCopyKeyBtn')) {
      $('miCopyKeyBtn').onclick = () => copyText(acc.apiKey, $('miCopyKeyBtn'), 'Key copied ✓');
    }
    if ($('miResetKeyBtn')) {
      $('miResetKeyBtn').onclick = () => {
        saveAccount({ tier: 'free', mode: 'sandbox', apiKey: '', credits: 0, sub: '', brandTokens: null });
        renderAccountModal('Signed out. Reverted to Free plan.');
      };
    }
    if ($('miPortalBtn')) {
      $('miPortalBtn').onclick = async () => {
        const statusEl = $('miModalStatus');
        try {
          const data = await postApi('/api/v1/portal', { apiKey: acc.apiKey });
          if (data.portalUrl) {
            window.location.href = data.portalUrl;
          } else if (statusEl) {
            statusEl.textContent = data.message || 'Billing portal available after live Stripe checkout.';
          }
        } catch {
          if (statusEl) statusEl.textContent = 'Sandbox mode: switch plans above or visit Pricing.';
        }
      };
    }
    if ($('miVerifyKeyBtn')) {
      $('miVerifyKeyBtn').onclick = async () => {
        const val = $('miPasteKeyInput').value;
        try {
          const verified = await verifyAndSaveKey(val);
          renderAccountModal(`Verified ${verified.tier.toUpperCase()} key (${verified.mode}).`);
        } catch (err) {
          if ($('miModalStatus')) $('miModalStatus').textContent = err.message || 'Invalid API key.';
        }
      };
    }
    dlg.querySelectorAll('[data-mint]').forEach((btn) => {
      btn.onclick = async () => {
        const t = btn.dataset.mint;
        const { acc: minted } = await issueSandboxKey(t, { credits: t === 'credits' ? 500 : 0 });
        renderAccountModal(`Issued ${minted.tier.toUpperCase()} sandbox key.`);
      };
    });
    dlg.querySelectorAll('[data-mod-mcp]').forEach((btn) => {
      btn.onclick = () => {
        uiState.mcpClient = btn.dataset.modMcp;
        renderAccountModal();
      };
    });
    if ($('miModCopyMcp')) {
      $('miModCopyMcp').onclick = () => copyText($('miModMcpCode').textContent, $('miModCopyMcp'));
    }

    function readTokenForm() {
      const bez = $('miBtBez')
        .value.split(',')
        .map((v) => Number(v.trim()))
        .filter((n) => Number.isFinite(n));
      return {
        brandName: $('miBtName').value.trim() || 'Default Brand',
        springStiffness: Number($('miBtK').value) || 280,
        springDamping: Number($('miBtC').value) || 26,
        durationScale: Number($('miBtScale').value) || 1.0,
        bezierCurve: bez.length === 4 ? bez : [0.2, 0.8, 0.2, 1],
        reducedMotionPolicy: $('miBtRm').value || 'respect',
      };
    }

    if ($('miTokensForm')) {
      $('miTokensForm').onsubmit = (e) => {
        e.preventDefault();
        const next = readTokenForm();
        saveBrandTokens(next);
        const cur = getAccount();
        if (cur.tier === 'teams') {
          saveAccount({ ...cur, brandTokens: next });
        }
        renderAccountModal('Saved Brand Motion Tokens.');
      };
    }
    if ($('miSaveAndMintTeams')) {
      $('miSaveAndMintTeams').onclick = async () => {
        const next = readTokenForm();
        saveBrandTokens(next);
        await issueSandboxKey('teams', { brandTokens: next });
        renderAccountModal('Issued Teams sandbox key with Brand Motion Tokens encoded.');
      };
    }
  }

  function openAccountModal(tab = 'plan', notice = '') {
    uiState.modalTab = tab;
    renderAccountModal(notice);
    const dlg = $('miAccountModal');
    if (dlg && !dlg.open) dlg.showModal();
  }

  function openUpgradeModal(motion) {
    ensureModals();
    const dlg = $('miUpgradeModal');
    dlg.innerHTML = `
      <div class="mi-modal-head">
        <h3 id="miUpTitle">Monthly free extraction limit reached</h3>
        <button type="button" class="mi-modal-close" id="miCloseUp">Close</button>
      </div>
      <div class="mi-modal-body">
        <p style="margin:0;color:var(--mute);font-size:14.5px">
          You’ve used all <strong>${FREE_MONTHLY_LIMIT} of ${FREE_MONTHLY_LIMIT}</strong> Free code &amp; prompt extractions for this month.
          Browsing the gallery, interactive previews, and copying the <strong>Motion spec</strong> tab remain 100% free.
        </p>
        <div class="mi-key-card">
          <div class="mi-key-row">
            <strong>Pro (Builder) — $19/mo ($15/mo annual)</strong>
            <span class="mi-badge" data-accent="true">Unlimited code + MCP</span>
          </div>
          <span style="font-size:13px;color:var(--mute)">Unlock unlimited extractions across CSS, React/Motion, GSAP, SwiftUI &amp; Remotion, plus 30 custom URL/video extractions/mo.</span>
        </div>
        <div class="mi-btn-row">
          <button type="button" class="mi-btn" data-primary="true" id="miUpViewPricing">View Pricing</button>
          <button type="button" class="mi-btn" id="miUpPasteKey">Paste API Key</button>
          <button type="button" class="mi-btn" id="miUpSandboxPro">Try Pro Sandbox Key</button>
        </div>
      </div>
    `;
    $('miCloseUp').onclick = () => dlg.close();
    $('miUpViewPricing').onclick = () => {
      dlg.close();
      if ($('sheet') && $('sheet').open) $('sheet').close();
      window.__MOTION_UI && window.__MOTION_UI.setView('pricing');
    };
    $('miUpPasteKey').onclick = () => {
      dlg.close();
      openAccountModal('plan');
    };
    $('miUpSandboxPro').onclick = async () => {
      await issueSandboxKey('pro');
      dlg.close();
      updateSheetQuotaMeta();
    };
    if (!dlg.open) dlg.showModal();
  }

  /* ---------- Lifecycle Wiring ---------- */
  function init() {
    renderPlanPill();
    bindShareForAgent();
    renderAgentsInteractive();

    window.addEventListener('motionindex:view', (e) => {
      const view = e.detail && e.detail.view;
      if (view === 'pricing') renderPricingView();
      if (view === 'agents') renderAgentsInteractive();
    });

    window.addEventListener('motionindex:sheet', () => {
      updateSheetQuotaMeta();
    });

    // Support direct #pricing or #agents deep links
    if (location.hash === '#pricing' && window.__MOTION_UI) {
      window.__MOTION_UI.setView('pricing');
    } else if (location.hash === '#agents' && window.__MOTION_UI) {
      window.__MOTION_UI.setView('agents');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
