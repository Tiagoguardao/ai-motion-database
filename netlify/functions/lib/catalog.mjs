import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sanitizeBrandTokens } from './auth.mjs';

const CATALOG_DIR = path.dirname(fileURLToPath(import.meta.url));

let cachedCatalog = null;
let cachedCatalogPath = null;

function resolveCatalogPath() {
  const candidates = [
    path.resolve(process.cwd(), 'data/motions.json'),
    path.resolve(CATALOG_DIR, '../../../data/motions.json'),
    path.resolve(CATALOG_DIR, '../../data/motions.json'),
    path.resolve(CATALOG_DIR, '../data/motions.json'),
  ];
  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error(`Could not locate data/motions.json. Searched: ${candidates.join(', ')}`);
}

export function loadCatalog(forceReload = false) {
  if (cachedCatalog && !forceReload) return cachedCatalog;
  const catalogPath = resolveCatalogPath();
  const raw = fs.readFileSync(catalogPath, 'utf8');
  const parsed = JSON.parse(raw);
  const motions = Array.isArray(parsed.motions) ? parsed.motions : [];
  const apps = Array.isArray(parsed.apps) ? parsed.apps : [];
  const byId = new Map(motions.map((m) => [m.id, m]));
  cachedCatalogPath = catalogPath;
  cachedCatalog = {
    count: motions.length,
    appsCount: apps.length,
    apps,
    motions,
    byId,
  };
  return cachedCatalog;
}

export function getCatalogPath() {
  if (!cachedCatalogPath) loadCatalog();
  return cachedCatalogPath;
}

export function getMotionById(id) {
  if (!id || typeof id !== 'string') return null;
  const { byId } = loadCatalog();
  return byId.get(id.trim()) || null;
}

function norm(v) {
  return String(v || '').trim().toLowerCase();
}

export function searchMotions(params = {}, baseUrl = 'https://ai-motion-database.netlify.app') {
  const catalog = loadCatalog();
  const q = norm(params.q || params.query);
  const use = norm(params.use || params.pattern);
  const stack = norm(params.stack);
  const trigger = norm(params.trigger);
  const feel = norm(params.feel);
  const collection = norm(params.collection);
  const app = norm(params.app);

  const limitRaw = Number(params.limit);
  const offsetRaw = Number(params.offset);
  const limit = Number.isFinite(limitRaw) && limitRaw > 0 ? Math.min(100, Math.floor(limitRaw)) : 24;
  const offset = Number.isFinite(offsetRaw) && offsetRaw >= 0 ? Math.floor(offsetRaw) : 0;

  const filtered = catalog.motions.filter((m) => {
    if (use && use !== 'all' && use !== 'any') {
      const mUse = norm(m.use);
      if (mUse !== use && !mUse.includes(use)) return false;
    }
    if (stack && stack !== 'any') {
      const mStack = norm(m.stack);
      if (mStack !== stack && !mStack.includes(stack)) return false;
    }
    if (trigger && trigger !== 'any') {
      const mTrigger = norm(m.trigger);
      if (mTrigger !== trigger && !mTrigger.includes(trigger)) return false;
    }
    if (feel && feel !== 'any') {
      const mFeel = norm(m.feel);
      if (mFeel !== feel && !mFeel.includes(feel)) return false;
    }
    if (collection && collection !== 'any') {
      const mColl = norm(m.collection);
      if (mColl !== collection && !mColl.includes(collection)) return false;
    }
    if (app && app !== 'any') {
      const mAppSlug = norm(m.app?.slug);
      const mAppName = norm(m.app?.name);
      if (mAppSlug !== app && mAppName !== app && !mAppName.includes(app) && !mAppSlug.includes(app)) {
        return false;
      }
    }
    if (q) {
      const haystack = [
        m.id,
        m.title,
        m.use,
        m.stack,
        m.trigger,
        m.feel,
        m.collection,
        m.source,
        m.summary,
        m.easingLabel,
        (m.properties || []).join(' '),
        m.app ? [m.app.name, m.app.slug, m.app.category, m.app.bundleId].join(' ') : '',
      ]
        .join(' ')
        .toLowerCase();
      // Support multi-word queries where every token must appear
      const terms = q.split(/\s+/).filter(Boolean);
      if (!terms.every((t) => haystack.includes(t))) return false;
    }
    return true;
  });

  const cleanBase = baseUrl.replace(/\/+$/, '');
  const slice = filtered.slice(offset, offset + limit).map((m) => ({
    id: m.id,
    title: m.title,
    use: m.use,
    stack: m.stack,
    trigger: m.trigger,
    feel: m.feel || null,
    durationMs: m.durationMs,
    easing: m.easing,
    easingLabel: m.easingLabel,
    collection: m.collection,
    app: m.app ? { name: m.app.name, slug: m.app.slug, category: m.app.category } : null,
    summary: m.summary || '',
    previewUrl: `${cleanBase}/#${m.id}`,
    codeEndpoint: `${cleanBase}/api/v1/motions/${encodeURIComponent(m.id)}/code`,
  }));

  return {
    total: filtered.length,
    count: slice.length,
    offset,
    limit,
    catalogCount: catalog.count,
    appsCount: catalog.appsCount,
    filters: {
      q: q || null,
      use: use || null,
      stack: stack || null,
      trigger: trigger || null,
      feel: feel || null,
      collection: collection || null,
      app: app || null,
    },
    motions: slice,
  };
}

export const SUPPORTED_TARGET_STACKS = [
  'CSS',
  'React/Motion',
  'GSAP',
  'SwiftUI',
  'Remotion',
];

export function normalizeTargetStack(input, fallback = 'CSS') {
  if (!input || typeof input !== 'string') return fallback;
  const s = input.trim().toLowerCase();
  if (['css', 'vanilla', 'html', 'web'].includes(s)) return 'CSS';
  if (['react', 'react/motion', 'motion', 'framer', 'framer-motion', 'motion/react'].includes(s)) return 'React/Motion';
  if (['gsap', 'greensock'].includes(s)) return 'GSAP';
  if (['swiftui', 'swift', 'ios'].includes(s)) return 'SwiftUI';
  if (['remotion', 'video'].includes(s)) return 'Remotion';
  return input.trim();
}

function buildStackGuidance(targetStack, ir, tokens) {
  const durSec = (ir.durationMs / 1000).toFixed(3).replace(/0+$/, '').replace(/\.$/, '');
  const isSpring = ir.easing?.t === 'spring';
  const k = ir.easing?.k ?? tokens?.springStiffness ?? 280;
  const c = ir.easing?.c ?? tokens?.springDamping ?? 24;
  const bez = Array.isArray(ir.easing?.p) ? ir.easing.p : tokens?.bezierCurve || [0.2, 0.8, 0.2, 1];
  const rm = tokens?.reducedMotionPolicy || 'respect';

  const reducedMotionNote =
    rm === 'instant'
      ? 'Reduced motion policy: snap immediately (0ms) with no spatial translation.'
      : rm === 'crossfade'
        ? 'Reduced motion policy: replace spatial movement with a 150ms opacity crossfade.'
        : 'Reduced motion policy: honor prefers-reduced-motion / Accessibility Reduce Motion by disabling travel and keeping subtle opacity state cues.';

  switch (targetStack) {
    case 'React/Motion':
      return [
        `Target Stack: React + Motion (import { motion, useReducedMotion } from "motion/react").`,
        isSpring
          ? `Transition: { type: "spring", stiffness: ${k}, damping: ${c}, mass: 1 }`
          : `Transition: { duration: ${durSec}, ease: [${bez.join(', ')}] }`,
        `Animate GPU-composited properties (${(ir.properties || ['transform', 'opacity']).join(', ')}) and avoid layout thrashing; use layoutId when morphing shared geometry.`,
        reducedMotionNote,
      ].join('\n');

    case 'GSAP':
      return [
        `Target Stack: GSAP 3 (gsap.timeline / gsap.to).`,
        `Duration: ${durSec}s; Ease: ${isSpring ? `elastic/custom spring approximating k=${k}, c=${c}` : `CustomEase / cubic-bezier(${bez.join(', ')})`}.`,
        `Wrap inside gsap.context() with cleanup and gsap.matchMedia() for prefers-reduced-motion.`,
        reducedMotionNote,
      ].join('\n');

    case 'SwiftUI':
      return [
        `Target Stack: SwiftUI (iOS 17+ / macOS 14+).`,
        isSpring
          ? `Animation: .interpolatingSpring(stiffness: ${k}, damping: ${c})`
          : `Animation: .timingCurve(${bez.join(', ')}, duration: ${durSec})`,
        `Use .matchedGeometryEffect or .phaseAnimator for multi-beat choreography and read @Environment(\\.accessibilityReduceMotion).`,
        reducedMotionNote,
      ].join('\n');

    case 'Remotion':
      return [
        `Target Stack: Remotion (useCurrentFrame, useVideoConfig, spring, interpolate).`,
        isSpring
          ? `Physics: spring({ frame, fps, config: { stiffness: ${k}, damping: ${c}, mass: 1 } })`
          : `Interpolation: interpolate(frame, [0, Math.round(${durSec} * fps)], [0, 1], { easing: Easing.bezier(${bez.join(', ')}), extrapolateRight: "clamp" })`,
        `Drive all motion deterministically from frame (never CSS transitions or timers).`,
        reducedMotionNote,
      ].join('\n');

    case 'CSS':
    default:
      return [
        `Target Stack: Standard CSS / Web Animations API.`,
        `Duration: ${ir.durationMs}ms; Timing: ${isSpring ? `linear() spring approximation (k=${k}, c=${c}) or JS damped spring` : `cubic-bezier(${bez.join(', ')})`}.`,
        `Animate transform & opacity cleanly with @media (prefers-reduced-motion: reduce) fallback.`,
        reducedMotionNote,
      ].join('\n');
  }
}

/**
 * Compile a Motion IR + Brand Motion Token overrides + stack-specific adaptation prompt.
 */
export function buildMotionCodePayload(motion, options = {}) {
  const targetStack = normalizeTargetStack(options.stack, motion.stack || 'CSS');
  const mergedTokens = sanitizeBrandTokens({
    ...(options.accountBrandTokens || {}),
    ...(options.requestBrandTokens || {}),
  });

  // Start from motion's original physics IR
  let durationMs = Number(motion.durationMs) || 320;
  let easing = motion.easing ? JSON.parse(JSON.stringify(motion.easing)) : { t: 'bezier', p: [0.2, 0.8, 0.2, 1] };
  let easingLabel = motion.easingLabel || '';

  if (mergedTokens) {
    if (mergedTokens.durationScale && mergedTokens.durationScale !== 1) {
      durationMs = Math.max(60, Math.round(durationMs * mergedTokens.durationScale));
    }
    if (easing.t === 'spring') {
      if (mergedTokens.springStiffness) easing.k = mergedTokens.springStiffness;
      if (mergedTokens.springDamping) easing.c = mergedTokens.springDamping;
      easingLabel = `spring(${easing.k}, ${easing.c})`;
    } else if (mergedTokens.bezierCurve) {
      easing = { t: 'bezier', p: mergedTokens.bezierCurve };
      easingLabel = `cubic-bezier(${mergedTokens.bezierCurve.join(', ')})`;
    }
  }

  const motionIR = {
    schemaVersion: '1.0',
    id: motion.id,
    title: motion.title,
    useCase: motion.use,
    trigger: motion.trigger,
    feel: motion.feel || null,
    surface: motion.surface || 'dark',
    durationMs,
    originalDurationMs: motion.durationMs,
    easing,
    easingLabel,
    properties: motion.properties || [],
    choreography: motion.choreography || [],
    brandTokens: mergedTokens || null,
  };

  const stackGuidance = buildStackGuidance(targetStack, motionIR, mergedTokens);
  const tokenBlock = mergedTokens
    ? `\n\n[BRAND MOTION TOKENS ENFORCED${mergedTokens.brandName ? ` — ${mergedTokens.brandName}` : ''}]\n${JSON.stringify(mergedTokens, null, 2)}`
    : '';

  const adaptationPrompt = [
    `Implement "${motion.title}" (Motion #${motion.id}) for ${targetStack}.`,
    '',
    motion.agentPrompt || motion.summary || '',
    '',
    '[STACK ADAPTATION]',
    stackGuidance,
    tokenBlock.trim(),
  ]
    .filter((section) => section !== '')
    .join('\n');

  const baseUrl = (options.baseUrl || 'https://ai-motion-database.netlify.app').replace(/\/+$/, '');
  const previewUrl = `${baseUrl}/#${motion.id}`;

  return {
    id: motion.id,
    title: motion.title,
    stack: targetStack,
    sourceStack: motion.stack,
    collection: motion.collection,
    app: motion.app || null,
    brandTokensApplied: Boolean(mergedTokens),
    motionIR,
    code: motion.code || '',
    agentPrompt: motion.agentPrompt || '',
    adaptationPrompt,
    choreography: motion.choreography || [],
    source: motion.source || '',
    sourceUrl: motion.sourceUrl || '',
    previewUrl,
    shareText: `Motion #${motion.id} — pull into Claude Code / Cursor in 1 prompt: ${previewUrl}`,
  };
}
