#!/usr/bin/env python3
"""Generates data/packs/apps-ai-dev-utilities.json (25 iconic AI, Dev, Smart Home & Learning apps)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from app_motion_engines import build_motion_entry

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = {a["slug"]: a for a in json.loads((ROOT / ".cache/harvest_200_apps.json").read_text())["apps-ai-dev-utilities"]}

SPECS = {
    "chatgpt": {
        "motionSlug": "advanced-voice-orb-aura",
        "motionName": "Advanced Voice Sky Orb Harmonic Morph",
        "engine": "orb_voice_aura",
        "use": "Generative", "stack": "CSS", "trigger": "Click", "feel": "Organic", "surface": "dark",
        "dur": 520, "ease": {"t": "spring", "k": 260, "c": 20},
        "props": ["transform: scale + border-radius (liquid sky orb)", "transform: scale + opacity (voice halos)"],
        "summary": "ChatGPT's Advanced Voice Mode floats a luminous sky-blue liquid cloud sphere that organically squashes and stretches across Listening, Thinking, and Speaking states.",
        "hint": "Tap voice orb to switch conversation state",
        "choreography": [
            "Continuous: twin radial sky-blue acoustic halos expand over 2.6s.",
            "State shift: central orb smoothly reshapes its border-radius and aspect scale over 520ms cubic-bezier(0.22, 1.25, 0.36, 1)."
        ],
        "agentPrompt": "Build ChatGPT's Advanced Voice Mode orb on #0b0e14 with #38bdf8 -> #2563eb radial sky-cloud gradient: animate organic border-radius & scale morphs across Listening/Thinking/Speaking states over 520ms cubic-bezier(0.22, 1.25, 0.36, 1) with twin 2.6s concentric halos.",
        "cfg": {"bg": "#0b0e14", "card": "#141a26", "accent": "#38bdf8", "accent2": "#2563eb", "states": ["Listening…", "Thinking", "Speaking"]},
    },
    "claude": {
        "motionSlug": "terracotta-thinking-orb",
        "motionName": "Warm Terracotta Reasoning Aura & Artifact Cue",
        "engine": "orb_voice_aura",
        "use": "Backgrounds", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "light",
        "dur": 540, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale + border-radius (warm clay orb)", "transform: scale + opacity (halos)"],
        "summary": "Claude's warm parchment workspace breathes a tactile terracotta orb with soft editorial rings as it transitions from Extended Thinking into Artifact rendering.",
        "hint": "Tap orb to cycle Claude reasoning states",
        "choreography": [
            "Continuous: delicate #D97757 terracotta rings radiate calmly over 2.6s.",
            "Tap: clay orb smoothly morphs silhouette across Thinking, Drafting, and Artifact Ready."
        ],
        "agentPrompt": "Create Claude's warm parchment reasoning orb on #f7f4ee with #D97757 -> #b45309 radial gradient, calm 540ms organic morphs, and delicate expanding terracotta rings.",
        "cfg": {"bg": "#f7f4ee", "card": "#ffffff", "fg": "#1c1917", "accent": "#D97757", "accent2": "#b45309", "states": ["Extended Thinking…", "Drafting Code", "Artifact Ready"]},
    },
    "perplexity": {
        "motionSlug": "citation-pills-stream",
        "motionName": "Live Source Citation Pills & Streaming Answer",
        "engine": "streaming_ai_cards",
        "use": "Typography", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["opacity", "transform: translateY + scale (source chips)"],
        "summary": "Running a Pro Search in Perplexity pops verified teal source chips sequentially into a compact bar before streaming crisp cited synthesis lines below.",
        "hint": "Tap card to replay citation stream",
        "choreography": [
            "0-270ms: 3 verified source pills spring up in #20B2AA teal with 90ms stagger.",
            "160-400ms: synthesized answer lines glide into focus cleanly.",
            "400-460ms: blinking teal cursor signals live token streaming."
        ],
        "agentPrompt": "Recreate Perplexity's source-citation stream on #111618 with #20B2AA teal chips: stagger 3 citation pills upward (translateY 6px -> 0, scale 0.92 -> 1) by 90ms over 380ms cubic-bezier(0.22, 1.2, 0.36, 1) above streaming answer lines.",
        "cfg": {"bg": "#111618", "card": "#192124", "accent": "#20B2AA", "sources": ["[1] MDN Web", "[2] Apple HIG", "[3] Motion IR"], "lines": ["Comparing spring stiffness across iOS 26 & Web", "Optimal range: k=280–360, c=20–26"]},
    },
    "grok": {
        "motionSlug": "think-step-stream-reveal",
        "motionName": "Monochrome Think-Step Cascade & Token Caret",
        "engine": "streaming_ai_cards",
        "use": "Typography", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["opacity", "transform: translateY + scale"],
        "summary": "Grok's stark monochrome Think view cascades reasoning-step badges upward over obsidian black with a razor-sharp blinking token cursor.",
        "hint": "Tap card to replay Think steps",
        "choreography": [
            "0-260ms: Search X, DeepSearch, and Verify pills rise sequentially with 90ms spacing.",
            "160-400ms: high-contrast reasoning lines glide in cleanly.",
            "400-460ms: crisp white cursor blinks at 850ms cadence."
        ],
        "agentPrompt": "Build Grok's monochrome Think step stream on #09090b with stark #e4e4e7 chips staggered upward by 90ms over 380ms cubic-bezier(0.22, 1.2, 0.36, 1).",
        "cfg": {"bg": "#09090b", "card": "#141417", "accent": "#e4e4e7", "sources": ["Think · 1.4s", "Live X Posts", "Verified"], "lines": ["Scanning real-time design engineering posts", "Synthesizing top 5 spring patterns"]},
    },
    "gemini": {
        "motionSlug": "prism-sparkle-stream",
        "motionName": "Gemini Prism Prompt Cascade & Streaming Tokens",
        "engine": "streaming_ai_cards",
        "use": "Typography", "stack": "CSS", "trigger": "Click", "feel": "Fluid", "surface": "dark",
        "dur": 480, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["opacity", "transform: translateY + scale"],
        "summary": "Google Gemini's dark workspace streams luminous cobalt tool-use chips and response lines upward with silky, fluid Material timing.",
        "hint": "Tap card to replay Gemini stream",
        "choreography": [
            "0-270ms: Workspace, Canvas, and Deep Research pills rise smoothly by 90ms stagger.",
            "160-420ms: synthesized response lines fade into full clarity.",
            "420-480ms: luminous #4285F4 caret pulses steadily."
        ],
        "agentPrompt": "Create Google Gemini's streaming response card on #0e1118 with #4285F4 cobalt chips rising sequentially by 90ms over 380ms cubic-bezier(0.22, 1.2, 0.36, 1).",
        "cfg": {"bg": "#0e1118", "card": "#171c28", "accent": "#4285F4", "sources": ["✦ Canvas", "Deep Research", "Code Exec"], "lines": ["Generating interactive motion preview", "All 60fps spring constraints verified"]},
    },
    "poe": {
        "motionSlug": "multi-bot-switcher-pill",
        "motionName": "Fast Multi-Bot Model Switcher Pill Glide",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Crisp", "surface": "dark",
        "dur": 360, "ease": {"t": "spring", "k": 350, "c": 24},
        "props": ["transform: translateX (indigo thumb)", "color", "textContent"],
        "summary": "Switching frontier bots in Poe glides a sharp indigo pill cleanly across Assistant, Claude, and GPT tabs while refreshing live latency readouts.",
        "hint": "Tap model tabs to switch bot",
        "choreography": [
            "0-50ms: selected bot name highlights crisp white.",
            "50-300ms: #5D5CDE indicator slides across columns on spring(350, 24).",
            "300-360ms: token speed readout updates below."
        ],
        "agentPrompt": "Build Poe's fast bot-switcher segmented bar on #12121a with #5D5CDE indigo thumb translating over 360ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#12121a", "card": "#1c1c29", "accent": "#5D5CDE", "tabs": ["Gemini", "Claude", "GPT"], "tabVals": ["142 tok/s", "98 tok/s", "118 tok/s"]},
    },
    "elevenlabs": {
        "motionSlug": "neural-voice-waveform",
        "motionName": "Neural Speech Synthesis Waveform Scrubber",
        "engine": "waveform_audio",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Rhythmic", "surface": "dark",
        "dur": 260, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["background-color (active vocal bars)", "transform: scaleY (speech peak)"],
        "summary": "ElevenLabs renders studio-clean monochrome voice waveforms where generated speech illuminates crisp white bars sequentially with tactile peak lift.",
        "hint": "Tap Play or scrub neural speech",
        "choreography": [
            "Continuous: 18 studio bars illuminate sequentially in crisp monochrome contrast.",
            "Active bar pops scaleY(1.22) in soft silver accent.",
            "Direct click jumps synthesized playback instantaneously."
        ],
        "agentPrompt": "Recreate ElevenLabs' minimalist neural speech waveform on #0b0b0d with crisp #e4e4e7 active bars, 38px play button, and direct click-to-scrub.",
        "cfg": {"bg": "#0b0b0d", "card": "#16161a", "accent": "#a1a1aa", "accent2": "#ffffff", "track": "Flash v2.5 · Studio Voice", "bars": [24, 54, 86, 46, 94, 72, 38, 82, 66, 96, 52, 40, 88, 76, 48, 70, 58, 30]},
    },
    "otter-ai": {
        "motionSlug": "live-transcript-waveform",
        "motionName": "Live Diarized Audio Waveform & Speaker Meter",
        "engine": "waveform_audio",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 260, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["background-color (cobalt speech bars)", "transform: scaleY"],
        "summary": "Otter's real-time transcription bar tracks speaker cadence across 18 clean cobalt audio bars with instant click-to-jump playback.",
        "hint": "Tap Play or scrub meeting audio",
        "choreography": [
            "Continuous: playback index illuminates bars in #1E66F5 Otter blue.",
            "Current bar pops vertically scaleY(1.22) as live speech registers."
        ],
        "agentPrompt": "Build Otter's live meeting waveform scrubber on #f2f6ff with #1E66F5 blue bars and 38px circular play toggle.",
        "cfg": {"bg": "#f2f6ff", "card": "#ffffff", "fg": "#0f172a", "accent": "#1E66F5", "accent2": "#60a5fa", "track": "Speaker 1 · Live Sync", "bars": [32, 60, 78, 44, 90, 68, 50, 84, 72, 38, 76, 94, 58, 42, 70, 82, 52, 34]},
    },
    "suno": {
        "motionSlug": "ai-track-generation-stream",
        "motionName": "AI Song Prompt Tags & Lyric Beat Stream",
        "engine": "streaming_ai_cards",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 330, "c": 21},
        "props": ["opacity", "transform: translateY + scale (genre tags)"],
        "summary": "Generating a track in Suno springs warm vermilion genre tags upward before streaming freshly composed verse lines.",
        "hint": "Tap card to replay track generation",
        "choreography": [
            "0-270ms: Synthwave, 124 BPM, and Female Vocals chips pop in with 90ms stagger.",
            "160-400ms: generated song title and lyric line fade into place.",
            "400-460ms: live generation cursor pulses in #FF4D4D."
        ],
        "agentPrompt": "Build Suno's AI song generation tag cascade on #140f12 with #FF4D4D coral-red chips springing upward by 90ms stagger over 380ms.",
        "cfg": {"bg": "#140f12", "card": "#21181d", "accent": "#FF4D4D", "sources": ["Synthwave", "124 BPM", "v4 Studio"], "lines": ["Neon Harbor (Instrumental Intro)", "♪ City lights ripple on the midnight tide"]},
    },
    "arc-search": {
        "motionSlug": "browse-for-me-assembly",
        "motionName": "'Browse for Me' Live Page Assembly Cascade",
        "engine": "streaming_ai_cards",
        "use": "Transitions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 320, "c": 21},
        "props": ["opacity", "transform: translateY + scale (source tabs)"],
        "summary": "Arc Search's signature 'Browse for Me' animates scanned web-tab pills upward into a custom mini-page summary with airy electric-indigo energy.",
        "hint": "Tap card to replay Browse for Me",
        "choreography": [
            "0-270ms: 3 scanned site pills spring cleanly into view with 90ms stagger.",
            "160-420ms: synthesized mini-page headline and summary glide upward.",
            "420-480ms: glowing #6366f1 caret pulses gently."
        ],
        "agentPrompt": "Recreate Arc Search's 'Browse for Me' live assembly card on #111122 with #6366f1 indigo source pills staggering upward by 90ms over 380ms cubic-bezier(0.22, 1.2, 0.36, 1).",
        "cfg": {"bg": "#111122", "card": "#1b1b33", "accent": "#6366f1", "sources": ["6 pages read", "Best Espresso", "Lisbon Map"], "lines": ["Built a custom page for you", "Top 3 specialty roasters open right now"]},
    },
    "github": {
        "motionSlug": "pr-merge-graph-nodes",
        "motionName": "Pull Request Merge Graph & CI Node Glow",
        "engine": "graph_cursor_canvas",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 800, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["fill + drop-shadow (commit nodes)", "transform: translate (branch badges)"],
        "summary": "Merging a Pull Request in GitHub illuminates branch commit nodes in signature merge purple and CI emerald while branch tags glide into `main`.",
        "hint": "Tap commit graph to advance PR merge",
        "choreography": [
            "0-160ms: active commit nodes glow #8957e5 GitHub merge purple.",
            "80-740ms: `main` and `feat/motion` tags glide smoothly across the commit DAG.",
            "740-800ms: merged branch state settles crisply."
        ],
        "agentPrompt": "Build a GitHub PR commit-graph merge visualizer on #0d1117 with #8957e5 purple and #238636 emerald branch badges gliding across linked SVG commit nodes over 800ms.",
        "cfg": {"bg": "#0d1117", "card": "#161b22", "accent": "#8957e5", "accent2": "#238636", "tag1": "main", "tag2": "CI Passed ✓"},
    },
    "1password": {
        "motionSlug": "vault-unlock-slide-rail",
        "motionName": "Biometric Vault Unlock Slide & Blue Confirm",
        "engine": "swipe_rail_cta",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 520, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateX (vault key)", "transform: scaleX (cobalt wash)"],
        "summary": "Unlocking a 1Password vault sweeps crisp cobalt blue across the security rail before locking into an authenticated Autofill state.",
        "hint": "Click rail to unlock 1Password vault",
        "choreography": [
            "0-100ms: circular #0572EC thumb launches smoothly rightward.",
            "80-440ms: full-width cobalt wash sweeps across behind crisp status text.",
            "440-520ms: handle settles cleanly into ✓ Vault Unlocked."
        ],
        "agentPrompt": "Build 1Password's vault unlock slide rail on #0b111c with #0572EC cobalt scaleX fill and 40px sliding handle animating over 520ms cubic-bezier(0.22, 1.14, 0.36, 1).",
        "cfg": {"bg": "#0b111c", "card": "#141e30", "accent": "#0572EC", "prompt": "Slide to Unlock Vault", "done": "Autofill Ready ✓"},
    },
    "bitwarden": {
        "motionSlug": "totp-30s-countdown-ring",
        "motionName": "30-Second TOTP Radial Countdown Ring",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 680, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (30s TOTP ring)", "textContent (seconds remaining)"],
        "summary": "Bitwarden's authenticator smoothly sweeps a security-blue TOTP countdown ring around remaining validity seconds before cycling to a fresh 6-digit code.",
        "hint": "Tap ring to cycle TOTP interval",
        "choreography": [
            "0-160ms: concentric blue countdown rings prime from 12-o'clock.",
            "160-620ms: #175DDC outer ring sweeps via stroke-dashoffset.",
            "620-680ms: remaining seconds and '482 910' badge lock sharply."
        ],
        "agentPrompt": "Build Bitwarden's 30-second TOTP radial countdown gauge on #0c121e with #175DDC and #38bdf8 concentric SVG arcs sweeping over 680ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#0c121e", "card": "#151f33", "accent": "#175DDC", "accent2": "#38bdf8", "label": "TOTP Valid", "unit": "s", "scores": [28, 19, 11, 30], "tag": "482 910 · Copy"},
    },
    "tailscale": {
        "motionSlug": "mesh-vpn-connect-rail",
        "motionName": "Zero-Config Mesh VPN Slide-to-Connect Rail",
        "engine": "swipe_rail_cta",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 500, "ease": {"t": "spring", "k": 320, "c": 24},
        "props": ["transform: translateX (VPN knob)", "transform: scaleX (connected fill)"],
        "summary": "Connecting your Tailnet glides a crisp monochrome-to-indigo toggle handle across the rail to link every peer device instantaneously.",
        "hint": "Click rail to connect Tailnet",
        "choreography": [
            "0-90ms: circular handle departs left detent cleanly.",
            "70-420ms: indigo-slate wash sweeps across the rail behind monospace IP text.",
            "420-500ms: handle locks right with ✓ Connected."
        ],
        "agentPrompt": "Create Tailscale's mesh VPN slide-to-connect rail on #111216 with #4f46e5 connected wash and 40px thumb gliding over 500ms cubic-bezier(0.22, 1.14, 0.36, 1).",
        "cfg": {"bg": "#111216", "card": "#1c1e24", "accent": "#4f46e5", "prompt": "Slide to Connect Tailnet", "done": "100.64.0.12 · Active ✓"},
    },
    "philips-hue": {
        "motionSlug": "ambient-lamp-color-orb",
        "motionName": "Smart Room Ambient Color-Wash Orb",
        "engine": "orb_voice_aura",
        "use": "Backgrounds", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale + border-radius (lamp glow)", "transform: scale + opacity (ambient rings)"],
        "summary": "Selecting scenes in Philips Hue radiates silky violet-magenta light ripples from a glowing room-lamp sphere across a deep evening backdrop.",
        "hint": "Tap lamp orb to switch lighting scenes",
        "choreography": [
            "Continuous: soft violet light halos expand outward every 2.6s.",
            "Tap: glowing bulb orb shifts organically across Tokyo, Savanna Sunset, and Concentrate."
        ],
        "agentPrompt": "Build Philips Hue's ambient scene orb on #100c18 with #8B5CF6 -> #ec4899 radial lamp gradient, 560ms soft morphs, and 2.6s ambient light rings.",
        "cfg": {"bg": "#100c18", "card": "#1b1429", "accent": "#8B5CF6", "accent2": "#ec4899", "states": ["Tokyo · 72%", "Sunset · 54%", "Concentrate · 100%"]},
    },
    "sonos": {
        "motionSlug": "grouped-room-volume-dial",
        "motionName": "Multi-Room Precision Volume Rotary Dial",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 24},
        "props": ["transform: rotate (volume indicator)", "textContent (dB / level)"],
        "summary": "Sonos' tactile acoustic dial rotates a stark architectural pointer across calibrated ticks to tune Living Room + Studio volume in sync.",
        "hint": "Tap dial to step room volume",
        "choreography": [
            "0-70ms: tap steps grouped speaker volume to the next detent.",
            "40-360ms: crisp white indicator rotates cleanly across radial ticks.",
            "360-420ms: monospace volume percentage locks sharply."
        ],
        "agentPrompt": "Build Sonos' architectural monochrome volume dial on #0d0d0f with #f4f4f5 needle rotating across 13 radial ticks over 420ms cubic-bezier(0.22, 1.22, 0.36, 1).",
        "cfg": {"bg": "#0d0d0f", "card": "#1a1a1e", "accent": "#f4f4f5", "label": "LIVING + STUDIO", "vals": ["18%", "34%", "52%", "70%", "86%"]},
    },
    "tesla": {
        "motionSlug": "vehicle-control-card-tilt",
        "motionName": "Metallic Vehicle Control Card Tilt & Climate Lock",
        "engine": "card_freeze_tilt",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Hover", "feel": "Silky", "surface": "dark",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: rotateX + rotateY", "transform: translateX (metallic sheen)", "clip-path (defrost frost)"],
        "summary": "Preconditioning a Tesla sweeps an icy cabin-climate frost layer over a dark metallic control card with sleek pointer-tracked 3D sheen.",
        "hint": "Hover to tilt or tap Climate Defrost",
        "choreography": [
            "Hover: pointer drives sleek metallic perspective tilt and diagonal sheen.",
            "Tap: frosted climate-control layer wipes smoothly via clip-path across the card."
        ],
        "agentPrompt": "Recreate Tesla's dark metallic cabin-climate card on #0b0c0e with #E82127 -> #3f1d20 gradient, pointer 3D tilt, specular sweep, and clip-path defrost toggle.",
        "cfg": {"bg": "#0b0c0e", "card": "#16181c", "accent": "#E82127", "accent2": "#450a0a", "brand": "MODEL 3 · 284 mi", "num": "CABIN 21°C · LOCKED", "toggle": "Precondition ❄", "toggleAlt": "Cooling 20°C"},
    },
    "rivian": {
        "motionSlug": "drive-mode-pill-switcher",
        "motionName": "Adventure Drive-Mode Segmented Pill Switcher",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Tactile", "surface": "dark",
        "dur": 380, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateX (amber thumb)", "color", "textContent (chassis range)"],
        "summary": "Switching Rivian drive modes glides a rugged golden-amber pill across All-Purpose, Conserve, and Off-Road while updating estimated range.",
        "hint": "Tap drive modes to adjust ride height",
        "choreography": [
            "0-60ms: active drive mode snaps into crisp contrast.",
            "60-320ms: #F59E0B amber pill slides smoothly across columns.",
            "320-380ms: range & clearance readout updates cleanly."
        ],
        "agentPrompt": "Build Rivian's drive-mode switcher on #0f1412 with #F59E0B amber pill translating across All-Purpose/Conserve/Off-Road over 380ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#0f1412", "card": "#19221e", "accent": "#d97706", "tabs": ["Purpose", "Conserve", "Off-Road"], "tabVals": ["314 mi · Std", "348 mi · Low", "268 mi · High"]},
    },
    "carrot-weather": {
        "motionSlug": "live-radar-storm-track",
        "motionName": "Live Storm Radar Path & Precipitation Ping",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 1150, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (storm track)", "transform: translate (front marker)", "transform: scale (radar ping)"],
        "summary": "CARROT Weather tracks an incoming rain band along a glowing cyan storm vector into a pulsing live radar ping over crisp dark cartography.",
        "hint": "Tap radar to replay storm cell path",
        "choreography": [
            "Continuous: city radar beacon radiates #38BDF8 rings.",
            "0-1150ms: storm trajectory draws cleanly while cloud marker sweeps in."
        ],
        "agentPrompt": "Build CARROT Weather's storm radar tracker on #0b131e with #38BDF8 sky-blue SVG trajectory draw over 1150ms cubic-bezier(0.22, 1, 0.36, 1) and pulsing city ping.",
        "cfg": {"bg": "#0b131e", "card": "#132033", "accent": "#38BDF8", "badge": "Rain in 11 min · Meatbag", "marker": "🌧"},
    },
    "flightradar24": {
        "motionSlug": "great-circle-aircraft-glide",
        "motionName": "Live Great-Circle Flight Path & Yellow Jet Glide",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 1200, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (flight path)", "transform: translate (aircraft)", "transform: scale (airport beacon)"],
        "summary": "Flightradar24 glides its signature golden-yellow aircraft icon smoothly along a live great-circle flight track toward a pulsing arrival airport beacon.",
        "hint": "Tap airspace map to replay flight track",
        "choreography": [
            "Continuous: destination airport beacon pulses in #FACC15 radar yellow.",
            "0-1200ms: flight path draws via stroke-dashoffset as the aircraft glides smoothly across."
        ],
        "agentPrompt": "Recreate Flightradar24's live aircraft tracker on #0c1219 with #FACC15 yellow flight path stroke-dashoffset animation over 1200ms cubic-bezier(0.22, 1, 0.36, 1) and moving airplane pin.",
        "cfg": {"bg": "#0c1219", "card": "#151f2b", "accent": "#eab308", "badge": "TP237 · 36,000 ft", "marker": "✈"},
    },
    "speedtest": {
        "motionSlug": "ookla-speedometer-needle-sweep",
        "motionName": "Neon-Cyan Speedometer Needle Sweep & Mbps Gauge",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 300, "c": 20},
        "props": ["transform: rotate (neon speedometer needle)", "textContent (Mbps readout)"],
        "summary": "Running Speedtest by Ookla sweeps a luminous neon-cyan needle rapidly across the midnight gauge dial as live gigabit throughput surges upward.",
        "hint": "Tap gauge to surge Mbps readout",
        "choreography": [
            "0-70ms: tap triggers next live throughput sample.",
            "40-360ms: glowing #22d3ee needle swings across calibrated ticks with spring overshoot.",
            "360-420ms: monospace Mbps telemetry locks sharply."
        ],
        "agentPrompt": "Recreate Ookla Speedtest's dark speedometer dial on #141526 with glowing #22d3ee neon-cyan needle swinging across radial ticks over 420ms cubic-bezier(0.22, 1.22, 0.36, 1).",
        "cfg": {"bg": "#141526", "card": "#1d1f36", "accent": "#22d3ee", "label": "DOWNLOAD MBPS", "vals": ["124", "386", "612", "842", "948"]},
    },
    "nyt": {
        "motionSlug": "wordle-3d-tile-flip-cascade",
        "motionName": "Wordle 3D Perspective Tile Flip Cascade",
        "engine": "envelope_seal_reveal",
        "use": "Typography", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 480, "ease": {"t": "spring", "k": 300, "c": 22},
        "props": ["transform: rotateX (360deg sequential)", "background-color (Wordle green/gold)", "transition-delay (70ms)"],
        "summary": "Submitting a guess in NYT Wordle cascades letter tiles one by one through a crisp 3D X-axis perspective flip, revealing emerald correct and ochre present clues.",
        "hint": "Tap Wordle row to flip guess tiles",
        "choreography": [
            "0ms: first letter tile launches a 360° perspective X-axis rotation.",
            "70-350ms: remaining letters flip sequentially with 70ms stagger into #538d4e emerald and #b59f3b ochre.",
            "350-480ms: solved row settles cleanly on crisp newsprint white."
        ],
        "agentPrompt": "Recreate NYT Wordle's iconic tile flip reveal on #ffffff with #538d4e correct green and #b59f3b present ochre tiles: cascade 6 square letter tiles through rotateX(360deg) over 480ms cubic-bezier(0.22, 1.2, 0.36, 1) with 70ms per-tile stagger.",
        "cfg": {"bg": "#f8f8f7", "card": "#ffffff", "fg": "#121213", "accent": "#538d4e", "accent2": "#b59f3b", "tiles": ["S", "P", "R", "I", "N", "G"], "sub": "Splendid · 3 / 6"},
    },
    "readwise-reader": {
        "motionSlug": "ghostreader-highlight-stream",
        "motionName": "Ghostreader Key-Highlight Pill Cascade",
        "engine": "streaming_ai_cards",
        "use": "Typography", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "light",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["opacity", "transform: translateY + scale (highlight pills)"],
        "summary": "Triggering Ghostreader in Readwise Reader pops warm amber highlight tags above a clean editorial summary card with unhurried reading rhythm.",
        "hint": "Tap article card to replay Ghostreader",
        "choreography": [
            "0-270ms: Highlight, Flashcard, and Summary chips rise cleanly in #d97706 amber.",
            "160-400ms: distilled takeaway lines glide smoothly into view.",
            "400-460ms: warm reading caret pulses steadily."
        ],
        "agentPrompt": "Build Readwise Reader's Ghostreader summary cascade on #faf7f0 with #d97706 amber pills staggering upward by 90ms over 380ms cubic-bezier(0.22, 1.2, 0.36, 1).",
        "cfg": {"bg": "#faf7f0", "card": "#ffffff", "fg": "#1c1917", "accent": "#d97706", "sources": ["★ Highlight", "Ghostreader", "Spaced Rep"], "lines": ["3 key takeaways saved to Notion", "Review scheduled in 4 days"]},
    },
    "brilliant": {
        "motionSlug": "interactive-logic-node-graph",
        "motionName": "Interactive Logic Node Snap & Concept Highlight",
        "engine": "graph_cursor_canvas",
        "use": "Generative", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 800, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["fill (solved concept nodes)", "transform: translate (interactive pins)"],
        "summary": "Solving an interactive lesson in Brilliant lights connected geometry nodes in crisp emerald and cobalt as step markers glide cleanly across the proof graph.",
        "hint": "Tap diagram to step interactive proof",
        "choreography": [
            "0-160ms: active logic nodes illuminate in Brilliant emerald (#16a34a).",
            "80-740ms: Proof Step and QED tags glide cleanly across the SVG graph.",
            "740-800ms: solved node pair highlights sharply."
        ],
        "agentPrompt": "Build Brilliant's interactive logic-node lesson diagram on #f7f8fa with #16a34a emerald and #2563eb cobalt markers gliding across connected SVG nodes over 800ms.",
        "cfg": {"bg": "#f7f8fa", "card": "#ffffff", "fg": "#101114", "accent": "#16a34a", "accent2": "#2563eb", "tag1": "Input A", "tag2": "Q.E.D. ✓"},
    },
    "khan-academy": {
        "motionSlug": "mastery-level-stepper",
        "motionName": "Mastery Crown Skill-Level Stepper Flow",
        "engine": "stepper_progress_flow",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 450, "ease": {"t": "spring", "k": 320, "c": 21},
        "props": ["width (mastery bar)", "transform: scale (crown milestone)", "box-shadow"],
        "summary": "Leveling up a math unit in Khan Academy sweeps bright teal mastery progress cleanly through Familiar, Proficient, and Mastered stages.",
        "hint": "Tap mastery levels to advance unit",
        "choreography": [
            "0-80ms: active mastery badge pops 1.2x with #14BF96 teal glow.",
            "40-390ms: horizontal progress connector sweeps smoothly rightward.",
            "390-450ms: earned skill stages lock filled."
        ],
        "agentPrompt": "Build Khan Academy's skill mastery stepper on #f1fbf8 with #14BF96 teal progress bar and 4 interactive level nodes scaling 1.2x over 450ms cubic-bezier(0.22, 1.15, 0.36, 1).",
        "cfg": {"bg": "#f1fbf8", "card": "#ffffff", "fg": "#0f172a", "accent": "#14BF96", "steps": ["Attempt", "Familiar", "Profic.", "Mastered"]},
    },
}

out = [build_motion_entry(META[slug], spec) for slug, spec in SPECS.items()]
dest = ROOT / "data" / "packs" / "apps-ai-dev-utilities.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(out)} motions to {dest.name}")
