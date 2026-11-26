#!/usr/bin/env python3
"""Generates data/packs/apps-health-lifestyle.json (25 iconic Health, Fitness & Mindfulness apps)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from app_motion_engines import build_motion_entry

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = {a["slug"]: a for a in json.loads((ROOT / ".cache/harvest_200_apps.json").read_text())["apps-health-lifestyle"]}

SPECS = {
    "oura": {
        "motionSlug": "readiness-crown-ring-sweep",
        "motionName": "Nocturnal Readiness Dual-Ring Sweep & Crown Glow",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Calm", "surface": "dark",
        "dur": 720, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (Readiness & Sleep rings)", "filter: drop-shadow", "textContent"],
        "summary": "Opening Oura sweeps luminous ice-blue and champagne rings smoothly around your morning Readiness score with calm Nordic serenity.",
        "hint": "Tap ring to cycle Readiness / Sleep / Activity",
        "choreography": [
            "0-180ms: dark obsidian ring tracks prime from 12-o'clock.",
            "180-660ms: outer Readiness arc and inner Sleep arc sweep simultaneously via stroke-dashoffset.",
            "660-720ms: center score and 'Optimal ♛' tag settle gently."
        ],
        "agentPrompt": "Build Oura's nocturnal Readiness dual-ring gauge on #0b0d12 with #93c5fd ice-blue and #fbbf24 crown-gold concentric SVG arcs animating stroke-dashoffset over 720ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#0b0d12", "card": "#151924", "accent": "#93c5fd", "accent2": "#fbbf24", "label": "Readiness", "unit": "", "scores": [91, 86, 94, 79], "tag": "♛ Optimal"},
    },
    "whoop": {
        "motionSlug": "recovery-strain-ring-dial",
        "motionName": "Tactical Recovery & Day Strain Concentric Dial",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 700, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (Recovery green & Strain blue)", "filter: drop-shadow"],
        "summary": "WHOOP's dark tactical dashboard sweeps an electric green Recovery ring around a bright cyan Day Strain inner arc with razor-sharp monospace telemetry.",
        "hint": "Tap dial to cycle Recovery profiles",
        "choreography": [
            "0-160ms: high-contrast black ring container primes.",
            "160-640ms: #16ec06 Recovery arc and #38bdf8 Strain arc sweep crisply via stroke-dashoffset.",
            "640-700ms: center recovery percentage locks cleanly."
        ],
        "agentPrompt": "Recreate WHOOP's Recovery & Strain concentric ring gauge on #090b0d with #16ec06 neon green outer arc and #38bdf8 inner arc animated over 700ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#090b0d", "card": "#14171c", "accent": "#16ec06", "accent2": "#38bdf8", "label": "Recovery", "unit": "%", "scores": [84, 92, 61, 77], "tag": "Peak Ready"},
    },
    "nike-run-club": {
        "motionSlug": "volt-pace-split-bars",
        "motionName": "Volt Run Pace Zones & Split Cascade",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 600, "ease": {"t": "spring", "k": 320, "c": 22},
        "props": ["width (volt split bars)", "transition-delay (90ms)"],
        "summary": "Nike Run Club's post-run summary shoots bold neon-volt split bars across pace zones with athletic 90ms stagger.",
        "hint": "Tap card to replay split bars",
        "choreography": [
            "0ms: 5K Pace bar fires rightward in signature Nike Volt (#CCFF00).",
            "90-180ms: Cadence and Negative Split bars cascade with crisp spring settle.",
            "480-600ms: tabular metrics lock cleanly."
        ],
        "agentPrompt": "Build Nike Run Club's volt split-bar cascade on #0d0e0f with #CCFF00 -> #84cc16 bars animating width over 600ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#0d0e0f", "card": "#181a1c", "accent": "#CCFF00", "accent2": "#84cc16", "rows": [("1K Split", 94), ("Cadence", 86), ("Zone 4", 72)]},
    },
    "peloton": {
        "motionSlug": "leaderboard-output-bars",
        "motionName": "Live Ride Output & Leaderboard Surge Bars",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Rhythmic", "surface": "dark",
        "dur": 620, "ease": {"t": "spring", "k": 310, "c": 21},
        "props": ["width (crimson output bars)", "transition-delay"],
        "summary": "Peloton's live ride telemetry drives punchy crimson output, cadence, and resistance bars upward as you push toward a new PR.",
        "hint": "Tap telemetry card to surge output",
        "choreography": [
            "0ms: Output bar surges rightward in #DF1C2F Peloton crimson.",
            "90-180ms: Cadence and Resistance bars stagger in smoothly.",
            "500-620ms: live percentage readouts settle cleanly."
        ],
        "agentPrompt": "Build Peloton's live ride metric bar card on #101114 with #DF1C2F -> #fb7185 bars animating width over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#101114", "card": "#1b1d22", "accent": "#DF1C2F", "accent2": "#fb7185", "rows": [("Output", 92), ("Cadence", 84), ("Resist", 68)]},
    },
    "myfitnesspal": {
        "motionSlug": "macro-calorie-bars",
        "motionName": "Daily Macro Breakdown Staggered Bars",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 620, "ease": {"t": "bezier", "p": [0.22, 1.16, 0.36, 1]},
        "props": ["width (macro bars)", "transition-delay (90ms)"],
        "summary": "Logging a meal in MyFitnessPal smoothly cascades Protein, Carbs, and Fat bars across crisp royal blue progress tracks.",
        "hint": "Tap card to log meal & fill macros",
        "choreography": [
            "0ms: Protein bar advances cleanly in #0066EE blue.",
            "90-180ms: Carbs and Fat tracks stagger into updated daily totals.",
            "500-620ms: tabular macro percentages align crisply."
        ],
        "agentPrompt": "Build MyFitnessPal's daily macro bars on #f3f7fd with #0066EE -> #38bdf8 tracks expanding over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#f3f7fd", "card": "#ffffff", "fg": "#0f172a", "accent": "#0066EE", "accent2": "#38bdf8", "rows": [("Protein", 88), ("Carbs", 74), ("Fats", 58)]},
    },
    "macrofactor": {
        "motionSlug": "expenditure-trend-scrub",
        "motionName": "Adaptive TDEE Expenditure Sparkline Scrub",
        "engine": "sparkline_scrub",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Hover", "feel": "Silky", "surface": "dark",
        "dur": 240, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["cx/cy (dot)", "x1/x2 (guide)", "textContent (kcal)"],
        "summary": "Scrubbing MacroFactor's expenditure curve slides a crisp glowing node along your adaptive calorie trend with zero visual noise.",
        "hint": "Hover or tap chart to scrub TDEE",
        "choreography": [
            "0-50ms: horizontal scrub maps cleanly to daily expenditure estimates.",
            "50-190ms: indigo marker and dashed vertical crosshair glide smoothly.",
            "190-240ms: monospace kcal figure updates in real time."
        ],
        "agentPrompt": "Build MacroFactor's adaptive expenditure sparkline scrubber on #0f1218 with #818cf8 curve and pointer-tracked reticle gliding over 160ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#0f1218", "card": "#181d26", "accent": "#818cf8", "label": "Expenditure", "unit": "", "delta": "2,640 kcal avg", "points": [44, 42, 39, 41, 36, 33, 30, 27, 24, 20], "values": ["2,510", "2,530", "2,555", "2,540", "2,580", "2,605", "2,620", "2,645", "2,665", "2,690"]},
    },
    "gentler-streak": {
        "motionSlug": "activity-path-ring-glow",
        "motionName": "Organic Activity Path Ring & Gentle Zone",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Organic", "surface": "light",
        "dur": 740, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (organic arcs)", "textContent"],
        "summary": "Gentler Streak replaces harsh fitness rings with warm leaf-green and sunny-amber arcs that sweep smoothly to keep training inside your healthy zone.",
        "hint": "Tap ring to preview healthy zone states",
        "choreography": [
            "0-180ms: warm cream dial primes smoothly.",
            "180-680ms: #78C850 green and #fbbf24 sun arcs glide via stroke-dashoffset.",
            "680-740ms: friendly 'In the Zone' badge anchors below."
        ],
        "agentPrompt": "Create Gentler Streak's warm organic ring gauge on #f6faf2 with #78C850 and #fbbf24 concentric SVG arcs sweeping over 740ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#f6faf2", "card": "#ffffff", "fg": "#1c2419", "accent": "#65a30d", "accent2": "#f59e0b", "label": "Activity", "unit": "%", "scores": [76, 84, 68, 90], "tag": "In the Zone"},
    },
    "hevy": {
        "motionSlug": "set-complete-swipe-timer",
        "motionName": "Completed Set Row Swipe & Rest Timer Toast",
        "engine": "list_swipe_action",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 400, "ease": {"t": "spring", "k": 340, "c": 22},
        "props": ["transform: translateX (set row)", "background-color (check)", "transform: translateY (rest toast)"],
        "summary": "Checking off a heavy gym set in Hevy flashes the set row cleanly across vibrant electric blue while popping the automatic rest-timer bar underneath.",
        "hint": "Tap set row to log & start rest timer",
        "choreography": [
            "0-80ms: circular checkbox fills #1E88E5 immediately.",
            "40-340ms: set card translates +92px over the logged backing.",
            "160-400ms: bottom rest-timer pill springs up smoothly."
        ],
        "agentPrompt": "Build Hevy's set-completion row interaction on #0e1116 with #1E88E5 action backing: slide the workout row +92px over 400ms cubic-bezier(0.22, 1.14, 0.36, 1) and float a rest-timer toast.",
        "cfg": {"bg": "#0e1116", "card": "#171d26", "accent": "#1E88E5", "rowTitle": "Bench Press · 85 kg × 8", "rowSub": "Set 3 of 4 · RPE 8", "actionLbl": "Logged"},
    },
    "strong": {
        "motionSlug": "pr-set-check-swipe",
        "motionName": "New PR Set Check Swipe & Rest Bar Pop",
        "engine": "list_swipe_action",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 400, "ease": {"t": "spring", "k": 330, "c": 23},
        "props": ["transform: translateX", "transform: translateY"],
        "summary": "Completing a Personal Record set in Strong locks the exercise row cleanly across crisp sky-blue feedback with an instant Undo/Rest snackbar.",
        "hint": "Tap workout set to log PR",
        "choreography": [
            "0-80ms: check circle fills #38BDF8 sky blue.",
            "40-340ms: row slides +92px revealing PR confirmation.",
            "160-400ms: toast rises smoothly beneath."
        ],
        "agentPrompt": "Create Strong's set-log swipe card on #10141a with #38BDF8 sky-blue reveal and bottom toast springing upward over 400ms.",
        "cfg": {"bg": "#10141a", "card": "#1a212b", "accent": "#0ea5e9", "rowTitle": "Deadlift · 140 kg × 5", "rowSub": "🏆 New 5RM Personal Record", "actionLbl": "PR Saved"},
    },
    "ladder": {
        "motionSlug": "strength-interval-bars",
        "motionName": "Volt Strength Block Progress Cascade",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 600, "ease": {"t": "spring", "k": 330, "c": 22},
        "props": ["width (volt workout bars)", "transition-delay"],
        "summary": "Ladder's athletic workout tracker snaps bold volt-yellow block progress bars across Warmup, Strength, and Finisher sets.",
        "hint": "Tap card to advance workout block",
        "choreography": [
            "0ms: Warmup bar snaps full in #CCFF00 volt.",
            "90-180ms: Strength and Conditioning bars stagger cleanly.",
            "480-600ms: completion percentages align crisply."
        ],
        "agentPrompt": "Build Ladder's volt strength block progress bars on #0d0e0f with #CCFF00 -> #a3e635 gradients cascading over 600ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#0d0e0f", "card": "#181a1d", "accent": "#CCFF00", "accent2": "#a3e635", "rows": [("Warmup", 100), ("Strength", 78), ("Finisher", 45)]},
    },
    "fitbit": {
        "motionSlug": "step-goal-ring-sweep",
        "motionName": "10,000 Steps Teal Ring Completion Sweep",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 720, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (step & active zone rings)", "filter: drop-shadow"],
        "summary": "Fitbit's daily goal dial sweeps radiant teal and mint arcs smoothly around your step progress until the 10K milestone locks in.",
        "hint": "Tap ring to advance daily steps",
        "choreography": [
            "0-180ms: concentric teal tracks prime smoothly.",
            "180-660ms: outer Steps ring and inner Active Zone ring fill via stroke-dashoffset.",
            "660-720ms: center percentage and milestone pill lock cleanly."
        ],
        "agentPrompt": "Create Fitbit's dual-ring step tracker on #0d1517 with #00B0B9 teal and #34d399 mint SVG arcs sweeping over 720ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#0d1517", "card": "#152326", "accent": "#00B0B9", "accent2": "#34d399", "label": "Step Goal", "unit": "%", "scores": [82, 95, 100, 64], "tag": "10,000 target"},
    },
    "garmin-connect": {
        "motionSlug": "body-battery-scrub",
        "motionName": "Body Battery Charge/Drain Interactive Curve",
        "engine": "sparkline_scrub",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Hover", "feel": "Crisp", "surface": "dark",
        "dur": 240, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["cx/cy (dot)", "x1/x2 (guide)", "textContent (battery score)"],
        "summary": "Scrubbing Garmin Connect's Body Battery timeline glides a bright cyan telemetry marker across hourly energy charge and drain samples.",
        "hint": "Hover or tap curve to inspect Body Battery",
        "choreography": [
            "0-50ms: pointer X resolves to hourly Body Battery telemetry.",
            "50-190ms: #007CC3/#38bdf8 dot and vertical hairline track cleanly.",
            "190-240ms: numeric score updates without flicker."
        ],
        "agentPrompt": "Build Garmin Connect's Body Battery SVG scrubber on #0b1118 with #0ea5e9 stroke and vertical gradient fill, tracking pointer X over 160ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#0b1118", "card": "#131d29", "accent": "#0ea5e9", "label": "Body Battery", "unit": "", "delta": "+48 overnight", "points": [14, 18, 24, 31, 36, 42, 48, 52, 44, 30], "values": ["94 / 100", "90 / 100", "84 / 100", "77 / 100", "72 / 100", "65 / 100", "58 / 100", "53 / 100", "62 / 100", "78 / 100"]},
    },
    "flo": {
        "motionSlug": "cycle-wheel-orbital-dial",
        "motionName": "Cycle Phase Wheel Rotary Day Dial",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "light",
        "dur": 440, "ease": {"t": "spring", "k": 280, "c": 22},
        "props": ["transform: rotate (phase indicator)", "textContent (cycle day)"],
        "summary": "Stepping through Flo's soft coral cycle wheel rotates a delicate glowing day marker cleanly across radial day ticks.",
        "hint": "Tap wheel to step cycle days",
        "choreography": [
            "0-70ms: tap advances the cycle wheel to the next phase milestone.",
            "40-380ms: #FF5C8D coral marker orbits smoothly around the 128px dial.",
            "380-440ms: centered day label locks cleanly."
        ],
        "agentPrompt": "Build Flo's pastel cycle-phase rotary wheel on #fff5f8 with #FF5C8D coral indicator rotating around radial day ticks over 440ms cubic-bezier(0.22, 1.22, 0.36, 1).",
        "cfg": {"bg": "#fff5f8", "card": "#ffffff", "fg": "#1f1720", "accent": "#FF5C8D", "label": "CYCLE DAY", "vals": ["Day 4", "Day 10", "Day 14", "Day 21", "Day 27"]},
    },
    "clue": {
        "motionSlug": "concentric-cycle-dial",
        "motionName": "Concentric Cycle Tracker Precision Dial",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: rotate (coral pointer)", "textContent"],
        "summary": "Clue's scientific cycle wheel pairs crisp Swiss-grid typography with a bright coral radial pointer snapping accurately across cycle milestones.",
        "hint": "Tap dial to step cycle predictions",
        "choreography": [
            "0-70ms: tap advances dial to next prediction marker.",
            "40-360ms: #FF5252 pointer rotates smoothly across calibrated ticks.",
            "360-420ms: monospace cycle status updates cleanly."
        ],
        "agentPrompt": "Create Clue's Swiss-style rotary cycle dial on #fafafa with #FF5252 coral pointer rotating across 13 radial ticks over 420ms cubic-bezier(0.22, 1.22, 0.36, 1).",
        "cfg": {"bg": "#f9f9fb", "card": "#ffffff", "fg": "#111827", "accent": "#FF5252", "label": "PHASE", "vals": ["Day 1", "Day 7", "Ovulat.", "Day 20", "Day 28"]},
    },
    "sleep-cycle": {
        "motionSlug": "dawn-alarm-sunrise-orb",
        "motionName": "Smart Dawn Alarm Sunrise Glow Orb",
        "engine": "orb_voice_aura",
        "use": "Backgrounds", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale + border-radius (sunrise orb)", "transform: scale + opacity (dawn ripples)"],
        "summary": "Sleep Cycle's smart wake window pulses a warm amber sunrise orb with slow, tranquil ripple halos as you transition from deep to light sleep.",
        "hint": "Tap dawn orb to cycle sleep stages",
        "choreography": [
            "Continuous: warm amber dawn halos expand smoothly every 2.6s.",
            "Tap: glowing #F59E0B sun orb morphs organically between Deep, REM, and Smart Wake."
        ],
        "agentPrompt": "Build Sleep Cycle's warm dawn orb on #0d1018 with #F59E0B -> #ea580c radial sun gradient, organic border-radius morphs, and 2.6s expanding sunrise rings.",
        "cfg": {"bg": "#0d1018", "card": "#171c28", "accent": "#F59E0B", "accent2": "#ea580c", "states": ["Deep Sleep · 2:14", "REM Cycle · 5:40", "Smart Wake · 6:52"]},
    },
    "endel": {
        "motionSlug": "generative-focus-soundscape-orb",
        "motionName": "Generative Focus Soundscape Harmonic Orb",
        "engine": "orb_voice_aura",
        "use": "Generative", "stack": "CSS", "trigger": "Loop", "feel": "Organic", "surface": "dark",
        "dur": 540, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale + border-radius (harmonic blob)", "transform: scale + opacity (sound ripples)"],
        "summary": "Endel's adaptive audio engine breathes a monochrome liquid-silver orb framed by minimalist concentric acoustic rings synced to your circadian mode.",
        "hint": "Tap orb to switch Focus / Relax / Sleep",
        "choreography": [
            "Continuous: twin hairline acoustic rings expand outward over 2.6s.",
            "Mode tap: liquid silver orb softly reshapes its organic silhouette across Focus, Relax, and Sleep."
        ],
        "agentPrompt": "Build Endel's minimalist adaptive soundscape orb on #09090b with silver-white radial sphere, organic border-radius morphing over 520ms, and twin 2.6s expanding hairline rings.",
        "cfg": {"bg": "#09090b", "card": "#18181b", "accent": "#e4e4e7", "accent2": "#52525b", "states": ["Focus · 108 BPM", "Relax · Deep Alpha", "Sleep · Pink Noise"]},
    },
    "waking-up": {
        "motionSlug": "mindfulness-bell-ripple",
        "motionName": "Terracotta Mindfulness Bell Ripple Orb",
        "engine": "orb_voice_aura",
        "use": "Backgrounds", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (bell resonance rings)", "border-radius (breathing sphere)"],
        "summary": "Beginning a session in Waking Up resonates calm terracotta bell ripples outward from a warm matte clay sphere.",
        "hint": "Tap sphere to shift meditation cue",
        "choreography": [
            "Continuous: delicate #E06D3B resonance rings expand gently over 2.6s.",
            "Tap: warm terracotta sphere gently shifts cadence between Notice, Breathe, and Rest."
        ],
        "agentPrompt": "Build Waking Up's contemplative terracotta orb on #141110 with #E06D3B -> #9a3412 sphere and slow 2.6s concentric bell ripples.",
        "cfg": {"bg": "#141110", "card": "#211c19", "accent": "#E06D3B", "accent2": "#9a3412", "states": ["Begin · 10:00", "Notice Breath", "Open Awareness"]},
    },
    "finch": {
        "motionSlug": "self-care-pet-heart-pop",
        "motionName": "Self-Care Pet Goal Check & Rainbow Heart Burst",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 360, "c": 17},
        "props": ["transform: scale + rotate (heart)", "transform: translate (sparkles)", "background-color"],
        "summary": "Completing a daily self-care goal in Finch pops a joyful pastel-emerald sparkle burst and cheers your companion pet forward.",
        "hint": "Tap goal pill to energize Finch",
        "choreography": [
            "0-80ms: heart pops 1.3x with playful tilt into #62C370 Finch green.",
            "60-460ms: 6 joyful sparkles radiate outward cleanly.",
            "240-400ms: pet energy counter increments."
        ],
        "agentPrompt": "Build Finch's playful self-care goal reward pill on #f2fbf4 with #22c55e/#62C370 accent: spring-scale the heart 1.3x and burst 6 radial sparkles over 480ms.",
        "cfg": {"bg": "#f2fbf4", "card": "#ffffff", "fg": "#14532d", "accent": "#22c55e", "author": "Pip the Finch · Adventure", "body": "Drink water & stretch for 2 minutes (+5 Energy!)", "icon": "💚", "count": 45},
    },
    "waterllama": {
        "motionSlug": "hydration-sloshing-bottle",
        "motionName": "Sloshing Hydration Wave Bottle Fill",
        "engine": "liquid_fill_vessel",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 680, "ease": {"t": "spring", "k": 250, "c": 18},
        "props": ["height (water level)", "transform: translateX + rotate (sloshing wave)"],
        "summary": "Logging a glass of water in Waterllama surges bright sky-blue liquid upward inside the rounded hydration bottle with a cheerful sloshing surface wave.",
        "hint": "Tap bottle to log +250ml water",
        "choreography": [
            "Continuous: glossy aqua wave sways smoothly side-to-side every 2.4s.",
            "0-580ms on tap: water level jumps upward with buoyant spring overshoot.",
            "580-680ms: updated hydration total centers cleanly."
        ],
        "agentPrompt": "Recreate Waterllama's sloshing bottle fill on #eff9ff with #38BDF8 -> #0284c7 liquid gradient: transition fill height over 680ms cubic-bezier(0.22, 1.18, 0.36, 1) with an oscillating wave crest.",
        "cfg": {"bg": "#eff9ff", "card": "#ffffff", "fg": "#0c4a6e", "accent": "#38BDF8", "accent2": "#0284c7", "label": "Hydration", "vals": ["750 ml", "1.25 L", "1.75 L", "2.00 L"]},
    },
    "streaks": {
        "motionSlug": "habit-ring-completion",
        "motionName": "Bold Tactile Habit Ring Fill & Orange Glow",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 680, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (habit ring)", "filter: drop-shadow", "textContent"],
        "summary": "Holding or tapping a Streaks habit ring sweeps bold vermilion-orange ink around the circular dial until the daily streak snaps complete.",
        "hint": "Tap ring to complete habit streak",
        "choreography": [
            "0-160ms: matte charcoal ring primes cleanly.",
            "160-620ms: #FF6B35 and #fbbf24 arcs sweep around to completion.",
            "620-680ms: streak day count locks firmly in place."
        ],
        "agentPrompt": "Build Streaks' Apple Design Award habit ring on #171210 with #FF6B35 orange and #fbbf24 concentric SVG arcs sweeping over 680ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#171210", "card": "#261c17", "accent": "#FF6B35", "accent2": "#fbbf24", "label": "Read 20m", "unit": "d", "scores": [12, 24, 38, 45], "tag": "Daily Streak"},
    },
    "lifesum": {
        "motionSlug": "life-score-ring-sweep",
        "motionName": "Fresh Green Life Score Ring & Vitality Gauge",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Fluid", "surface": "light",
        "dur": 720, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (Life Score arc)", "textContent"],
        "summary": "Lifesum's Life Score sweeps bright leaf-green and mint arcs around a clean white wellness gauge to highlight nutrition balance.",
        "hint": "Tap gauge to cycle Life Score",
        "choreography": [
            "0-160ms: crisp white wellness card primes.",
            "160-660ms: emerald and mint concentric rings fill via stroke-dashoffset.",
            "660-720ms: center Life Score settles crisply."
        ],
        "agentPrompt": "Build Lifesum's Life Score ring gauge on #f2fbf5 with #22c55e and #86efac SVG arcs animating over 720ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#f2fbf5", "card": "#ffffff", "fg": "#14532d", "accent": "#22c55e", "accent2": "#86efac", "label": "Life Score", "unit": "", "scores": [84, 91, 72, 88], "tag": "Balanced"},
    },
    "noom": {
        "motionSlug": "color-density-bars",
        "motionName": "Calorie Density Color-Zone Bars Cascade",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 620, "ease": {"t": "bezier", "p": [0.22, 1.16, 0.36, 1]},
        "props": ["width (density bars)", "transition-delay (90ms)"],
        "summary": "Noom's food-color budget smoothly cascades Green, Yellow, and Orange density bars to give calm, intuitive portion clarity.",
        "hint": "Tap card to animate color zones",
        "choreography": [
            "0ms: Green Foods bar glides across warm cream card.",
            "90-180ms: Yellow and Orange bars follow in 90ms stagger.",
            "500-620ms: percentages settle cleanly."
        ],
        "agentPrompt": "Create Noom's color-density progress card on #fdf8f6 with #F25C54 -> #fb923c bars expanding over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#fdf8f6", "card": "#ffffff", "fg": "#1c1917", "accent": "#22c55e", "accent2": "#F25C54", "rows": [("Green", 86), ("Yellow", 62), ("Orange", 34)]},
    },
    "runna": {
        "motionSlug": "interval-pace-zone-bars",
        "motionName": "Interval Split Target Bars & Pace Shift",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 600, "ease": {"t": "spring", "k": 320, "c": 22},
        "props": ["width (interval bars)", "transition-delay"],
        "summary": "Runna's structured training plan cascades bold rose-coral interval bars across Tempo, Threshold, and Recovery splits.",
        "hint": "Tap card to step training intervals",
        "choreography": [
            "0ms: Tempo split bar launches rightward in #FF3B5C.",
            "90-180ms: Threshold and Recovery bars cascade cleanly.",
            "480-600ms: split targets lock sharply."
        ],
        "agentPrompt": "Build Runna's interval training progress bars on #121014 with #FF3B5C -> #fb7185 gradients animating over 600ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#121014", "card": "#1d1921", "accent": "#FF3B5C", "accent2": "#fb7185", "rows": [("Tempo", 92), ("Thresh", 84), ("Easy", 60)]},
    },
    "eight-sleep": {
        "motionSlug": "thermal-pod-dial-scrub",
        "motionName": "Dual-Zone Thermal Pod Dial (-4° Cool ↔ +4° Warm)",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 290, "c": 23},
        "props": ["transform: rotate (thermal indicator)", "textContent (temperature)"],
        "summary": "Dialing your Eight Sleep Pod temperature rotates a crisp ice-blue indicator across calibrated radial detents from -4° deep cool to +3° gentle wake warmth.",
        "hint": "Tap dial to adjust Pod temperature",
        "choreography": [
            "0-70ms: tap steps thermal target to the next sleep phase setting.",
            "40-360ms: glowing #3B82F6 needle glides smoothly across the dark dial.",
            "360-420ms: center degree readout settles cleanly."
        ],
        "agentPrompt": "Recreate Eight Sleep's thermal control dial on #0a0e17 with #3B82F6 glowing indicator needle rotating across radial ticks over 420ms cubic-bezier(0.22, 1.22, 0.36, 1).",
        "cfg": {"bg": "#0a0e17", "card": "#131b2b", "accent": "#3B82F6", "label": "POD TEMP", "vals": ["-4°", "-2°", "0°", "+2°", "+4°"]},
    },
    "cronometer": {
        "motionSlug": "micronutrient-target-bars",
        "motionName": "Micronutrient Target Cascade Bars",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 620, "ease": {"t": "bezier", "p": [0.22, 1.16, 0.36, 1]},
        "props": ["width (nutrient target bars)", "transition-delay (90ms)"],
        "summary": "Cronometer's precision nutrition dashboard cascades vibrant tangerine bars across Vitamin D, Magnesium, and Omega-3 daily targets.",
        "hint": "Tap card to animate nutrient targets",
        "choreography": [
            "0ms: Vitamin D bar glides across dark slate track in #FF702A.",
            "90-180ms: Magnesium and Omega-3 bars stagger smoothly into place.",
            "500-620ms: tabular RDA percentages lock cleanly."
        ],
        "agentPrompt": "Build Cronometer's micronutrient progress bars on #141210 with #FF702A -> #fbbf24 gradients animating width over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#141210", "card": "#201c19", "accent": "#FF702A", "accent2": "#fbbf24", "rows": [("Vit D", 96), ("Magnes.", 82), ("Omega-3", 74)]},
    },
}

out = [build_motion_entry(META[slug], spec) for slug, spec in SPECS.items()]
dest = ROOT / "data" / "packs" / "apps-health-lifestyle.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(out)} motions to {dest.name}")
