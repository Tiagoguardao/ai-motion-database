#!/usr/bin/env python3
"""Generates data/packs/apps-social.json (25 iconic Social & Messaging apps)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from app_motion_engines import build_motion_entry

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = {a["slug"]: a for a in json.loads((ROOT / ".cache/harvest_200_apps.json").read_text())["apps-social"]}

SPECS = {
    "whatsapp": {
        "motionSlug": "voice-note-waveform-scrub",
        "motionName": "Voice Note Waveform Scrub & Emerald Play",
        "engine": "waveform_audio",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 260, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["background-color (played bars)", "transform: scaleY (active bar peak)", "textContent (timestamp)"],
        "summary": "Playing or scrubbing a WhatsApp voice message lights each vertical bar emerald green sequentially while giving the active playback bar a subtle vertical pop.",
        "hint": "Tap Play or click any bar to scrub",
        "choreography": [
            "0-60ms: circular #25D366 play button compresses on press and toggles to pause bars.",
            "Continuous: playback index steps through 18 bars, tinting played bars emerald and pulsing the active bar scaleY(1.22).",
            "Click scrub: tapping anywhere on the waveform jumps playback position instantaneously."
        ],
        "agentPrompt": "Build WhatsApp's voice-note pill on #0b141a with #1f2c34 bubble and #25D366 accent: place a 38px circular play/pause button beside 18 variable-height rounded bars; animate played bars to #25D366, pop the current bar to scaleY(1.22), and allow direct click-to-scrub.",
        "cfg": {"bg": "#0b141a", "card": "#1f2c34", "accent": "#25D366", "accent2": "#53f08a", "track": "Voice message · 1.5×", "bars": [25, 58, 82, 42, 74, 94, 60, 35, 86, 70, 48, 92, 65, 38, 76, 52, 64, 30]},
    },
    "snapchat": {
        "motionSlug": "snap-streak-tile-reveal",
        "motionName": "Snap Streak 3D Tile Flip & Yellow Flash",
        "engine": "envelope_seal_reveal",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 320, "c": 19},
        "props": ["transform: rotateX (360deg cascade)", "background-color", "transition-delay (70ms)"],
        "summary": "Opening a Snap streak badge cascades 3D perspective tiles across Snap Yellow and ink black with playful 70ms per-letter stagger.",
        "hint": "Tap tiles to trigger Snap streak flip",
        "choreography": [
            "0ms: first tile launches a 360° X-axis perspective flip.",
            "70-350ms: remaining letters ripple across with 70ms stagger, alternating bold accent fills.",
            "350-480ms: tiles settle cleanly with crisp high-contrast legibility."
        ],
        "agentPrompt": "Create a Snapchat streak reveal cascade on #111114 with #facc15 yellow and #ec4899 snap-red tiles: flip 6 rounded tiles around rotateX(360deg) over 480ms cubic-bezier(0.22, 1.2, 0.36, 1) with 70ms stagger delays.",
        "cfg": {"bg": "#111114", "card": "#1e1e24", "accent": "#eab308", "accent2": "#ec4899", "tiles": ["S", "N", "A", "P", "🔥", "42"], "sub": "42-day streak active"},
    },
    "x-twitter": {
        "motionSlug": "heart-particle-bookmark",
        "motionName": "Heart Radial Particle Burst & Counter Roll",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 380, "c": 18},
        "props": ["transform: scale + rotate (heart)", "transform: translate (6 radial sparks)", "color"],
        "summary": "Liking a post on X explodes six radial rose sparks outward from the heart icon while tilting it into a crisp spring overshoot and incrementing the counter.",
        "hint": "Tap heart pill to trigger burst",
        "choreography": [
            "0-80ms: heart pops scale(1.3) rotate(-8deg) while pill tints translucent #f91880.",
            "60-480ms: 6 micro-particles burst 16-24px radially and shrink to 0 opacity.",
            "260-420ms: tabular count locks in the incremented total."
        ],
        "agentPrompt": "Build X's heart-burst reaction pill on #000000 with #f91880 rose accent: on click, scale the heart icon to 1.3 with -8deg tilt over 380ms cubic-bezier(0.22, 1.4, 0.36, 1), tint the pill rgba(249,24,128,0.12), and spawn 6 radial particle dots fading out over 480ms.",
        "cfg": {"bg": "#000000", "card": "#121417", "accent": "#f91880", "author": "@designeng", "body": "Micro-physics > heavy page transitions every single time.", "icon": "♥", "count": 842},
    },
    "bluesky": {
        "motionSlug": "butterfly-repost-burst",
        "motionName": "Butterfly Like Burst & Sky Pill Glow",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 350, "c": 19},
        "props": ["transform: scale", "transform: translate (sky sparks)", "background-color"],
        "summary": "Tapping like on Bluesky pops a bright sky-blue burst around the action pill with light, airy spring responsiveness.",
        "hint": "Tap sky pill to trigger burst",
        "choreography": [
            "0-90ms: icon scales up 1.3x with subtle counter-clockwise lift.",
            "60-460ms: 6 #1185FE sparks radiate outward from the icon center.",
            "220-420ms: pill tint and incremented count settle smoothly."
        ],
        "agentPrompt": "Build Bluesky's airy post reaction burst on #f4f9ff with #1185FE sky blue: on toggle, scale the icon 1.3x on spring(350, 19), tint the pill border and background, and emit 6 radial sky-blue particles over 460ms.",
        "cfg": {"bg": "#f3f8ff", "card": "#ffffff", "fg": "#0f172a", "accent": "#1185FE", "author": "bsky.app · @motion", "body": "Open protocols + 60fps mobile feed choreography.", "icon": "🦋", "count": 319},
    },
    "mastodon": {
        "motionSlug": "boost-star-pop",
        "motionName": "Toot Boost Pop & Periwinkle Spark Burst",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 340, "c": 20},
        "props": ["transform: scale + rotate", "transform: translate (sparks)", "color"],
        "summary": "Boosting a Mastodon post launches a crisp periwinkle spark burst around the pill while shifting border and text accents into federated purple.",
        "hint": "Tap boost pill to animate",
        "choreography": [
            "0-90ms: boost icon rotates and scales 1.3x.",
            "60-460ms: 6 #6364FF dots radiate outward and fade cleanly.",
            "240-400ms: counter increments in place."
        ],
        "agentPrompt": "Implement Mastodon's boost button burst on #171923 with #6364FF periwinkle: scale and rotate the boost icon on toggle while radiating 6 dots over 480ms cubic-bezier(0.16, 1, 0.3, 1).",
        "cfg": {"bg": "#151722", "card": "#202332", "accent": "#6364FF", "author": "@fediverse@mastodon.social", "body": "Federated timelines with snappy client-side spring interactions.", "icon": "↻", "count": 94},
    },
    "signal": {
        "motionSlug": "encrypted-stream-reveal",
        "motionName": "Disappearing Message Verification Cascade",
        "engine": "streaming_ai_cards",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "dark",
        "dur": 480, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["opacity", "transform: translateY + scale (safety pills)"],
        "summary": "Signal's private chat thread cascades end-to-end encryption verification chips and message lines upward with calm, dependable blue timing.",
        "hint": "Tap card to replay verification cascade",
        "choreography": [
            "0-270ms: E2EE, Safety Number, and Timer pills rise sequentially with 90ms stagger.",
            "140-420ms: encrypted message preview lines fade upward smoothly.",
            "420-480ms: subtle typing cursor pulses cleanly in Signal blue."
        ],
        "agentPrompt": "Create a Signal private thread verification card on #12151c with #3A76F0 chips: stagger 3 pill badges upward (translateY 6px -> 0, scale 0.92 -> 1) by 90ms each over 380ms cubic-bezier(0.22, 1.2, 0.36, 1), followed by smooth message lines.",
        "cfg": {"bg": "#12151c", "card": "#1b202b", "accent": "#3A76F0", "sources": ["E2E Encrypted", "Timer: 5m", "Verified"], "lines": ["Safety number verified with Maya", "Meeting link stays local only"]},
    },
    "messenger": {
        "motionSlug": "theme-bubble-stream",
        "motionName": "Gradient Chat Theme Bubble Cascade",
        "engine": "streaming_ai_cards",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 320, "c": 22},
        "props": ["opacity", "transform: translateY + scale", "background-color"],
        "summary": "Messenger's expressive chat thread pops reaction chips and fresh message bubbles upward in a bouncy, staggered rhythm.",
        "hint": "Tap thread to replay message arrival",
        "choreography": [
            "0-260ms: quick-reply chips spring upward in #0084FF tint with 90ms spacing.",
            "150-400ms: incoming chat lines glide in smoothly with zero jump.",
            "400-460ms: live typing indicator pulses steadily."
        ],
        "agentPrompt": "Build a Messenger incoming bubble & quick-reply cascade on #0f1218 with #0084FF accents: stagger pill chips upward over 380ms cubic-bezier(0.22, 1.2, 0.36, 1) and reveal two chat lines with a blinking cursor.",
        "cfg": {"bg": "#0f1218", "card": "#191f2a", "accent": "#0084FF", "sources": ["👋 Wave", "📍 Share", "👍 Sounds good"], "lines": ["Just landed at SFO!", "Grabbing coffee near Gate B"]},
    },
    "linkedin": {
        "motionSlug": "celebrate-reaction-pop",
        "motionName": "Celebrate Reaction Pill Spring & Sparkles",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 340, "c": 20},
        "props": ["transform: scale + rotate", "transform: translate (sparks)", "background-color"],
        "summary": "Tapping Celebrate on a LinkedIn update pops the clapping badge with crisp corporate blue overshoot and subtle celebratory particles.",
        "hint": "Tap Celebrate pill on update card",
        "choreography": [
            "0-80ms: Celebrate icon pops 1.3x with slight tilt as pill tints #0A66C2.",
            "60-460ms: 6 radial blue dots fan outward cleanly.",
            "240-400ms: reaction count increments immediately."
        ],
        "agentPrompt": "Recreate LinkedIn's Celebrate reaction pill on #f3f2ef with #0A66C2 tint: scale the icon 1.3x on spring(340, 20), highlight the pill border/fill, and burst 6 radial micro-dots over 480ms.",
        "cfg": {"bg": "#f3f2ef", "card": "#ffffff", "fg": "#111827", "accent": "#0A66C2", "author": "Maya Chen · Staff Designer", "body": "Excited to share our new motion token system for iOS & Web!", "icon": "👏", "count": 512},
    },
    "substack": {
        "motionSlug": "notes-restack-pop",
        "motionName": "Notes Restack Pop & Persimmon Spark Burst",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 330, "c": 21},
        "props": ["transform: scale + rotate", "transform: translate (sparks)", "color"],
        "summary": "Restacking a Substack Note delivers an editorial persimmon-orange spring pop and delicate burst of sparks over warm paper white.",
        "hint": "Tap Restack pill to animate",
        "choreography": [
            "0-90ms: icon pops 1.3x into #FF6719 persimmon orange.",
            "60-460ms: 6 radial orange dots expand outward and vanish.",
            "260-420ms: tabular restack counter updates smoothly."
        ],
        "agentPrompt": "Design Substack Notes' Restack interaction on #faf8f5 with #FF6719 persimmon accent: animate the pill icon scale(1.3) rotate(-8deg) over 380ms cubic-bezier(0.22, 1.4, 0.36, 1) with a 6-dot radial burst.",
        "cfg": {"bg": "#faf8f5", "card": "#ffffff", "fg": "#18181b", "accent": "#FF6719", "author": "The Motion Dispatch", "body": "Why great software feels like an instrument rather than a spreadsheet.", "icon": "↻", "count": 176},
    },
    "bereal": {
        "motionSlug": "dual-cam-split-reveal",
        "motionName": "Front ↔ Back Dual-Camera Split Scrub",
        "engine": "split_before_after",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Tactile", "surface": "dark",
        "dur": 320, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset (camera wipe)", "left (divider handle)"],
        "summary": "Comparing BeReal's simultaneous Front and Back camera captures wipes cleanly across a stark black viewfinder with a crisp floating split handle.",
        "hint": "Move pointer or tap to wipe Front/Back",
        "choreography": [
            "0-60ms: horizontal scrub coordinate updates the vertical divider position.",
            "60-240ms: rear-camera layer reveals smoothly via clip-path: inset(0 0 0 p%).",
            "240-320ms: floating circular ↔ handle glides smoothly along the seam."
        ],
        "agentPrompt": "Build a BeReal Front/Back camera comparison wipe on #000000: layer two 146px viewfinder cards and scrub the upper layer's clip-path: inset(0 0 0 X%) synchronously with a white 2px divider and 24px circular drag badge.",
        "cfg": {"bg": "#000000", "card": "#111114", "accent": "#27272a", "accent2": "#3f3f46", "leftLbl": "FRONT CAM", "rightLbl": "BACK CAM"},
    },
    "locket": {
        "motionSlug": "widget-photo-flip",
        "motionName": "Home-Screen Locket 3D Photo Flip Reveal",
        "engine": "envelope_seal_reveal",
        "use": "Transitions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 310, "c": 20},
        "props": ["transform: rotateX", "background-color", "transition-delay"],
        "summary": "A fresh photo arriving on Locket Widget flips glossy warm-gold tiles in 3D perspective to announce a new moment from a close friend.",
        "hint": "Tap tiles to flip Locket update",
        "choreography": [
            "0ms: leading tile begins a 360° perspective X-flip.",
            "70-350ms: amber-gold tiles ripple sequentially across the row.",
            "350-480ms: settled widget strip holds crisp warm contrast."
        ],
        "agentPrompt": "Build a Locket Widget 3D flip notification on #12100d with #FFB800 gold accent: cascade 6 square rounded tiles through rotateX(360deg) over 480ms cubic-bezier(0.22, 1.2, 0.36, 1) with 70ms stagger.",
        "cfg": {"bg": "#12100d", "card": "#211d17", "accent": "#FFB800", "accent2": "#f97316", "tiles": ["L", "O", "C", "K", "E", "T"], "sub": "New snap from Sam · 1m"},
    },
    "partiful": {
        "motionSlug": "rsvp-going-confetti",
        "motionName": "RSVP Going Pill Pop & Party Sparks",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 360, "c": 17},
        "props": ["transform: scale + rotate", "transform: translate (party sparks)", "background-color"],
        "summary": "Tapping 'Going' on a Partiful invite pops a playful ultraviolet badge with radial confetti sparks and increments the guest count immediately.",
        "hint": "Tap Going pill to RSVP",
        "choreography": [
            "0-80ms: party emoji pops 1.3x with jaunty -8deg tilt.",
            "60-480ms: 6 electric violet sparks burst outward from the pill.",
            "240-400ms: guest count ticks up cleanly."
        ],
        "agentPrompt": "Build Partiful's playful RSVP Going button on #120d1f with #8B5CF6 ultraviolet highlight: spring-scale the emoji icon 1.3x on toggle and burst 6 radial confetti dots over 480ms.",
        "cfg": {"bg": "#120d1f", "card": "#1d1533", "accent": "#8B5CF6", "author": "Rooftop Vinyl Night", "body": "Saturday 8 PM · Mission Loft · BYO records", "icon": "🎉", "count": 48},
    },
    "retro-photo": {
        "motionSlug": "weekly-journal-tile-flip",
        "motionName": "Weekly Photo Strip 3D Flip Reveal",
        "engine": "envelope_seal_reveal",
        "use": "Transitions", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "light",
        "dur": 480, "ease": {"t": "spring", "k": 290, "c": 22},
        "props": ["transform: rotateX", "background-color", "transition-delay"],
        "summary": "Flipping open a weekly journal strip in Retro cascades tactile analog-orange day tiles in crisp 3D perspective.",
        "hint": "Tap week tiles to flip journal",
        "choreography": [
            "0ms: Monday tile initiates perspective rotateX(360deg).",
            "70-420ms: Mon–Sat tiles ripple across in warm #FF5C35 and slate tones.",
            "420-480ms: full week strip locks cleanly into editorial grid."
        ],
        "agentPrompt": "Create a Retro photo journal weekly flip animation on #faf7f2 with #FF5C35 vermilion accent: flip 6 day tiles (M-S) around rotateX(360deg) over 480ms cubic-bezier(0.22, 1.2, 0.36, 1) staggered by 70ms.",
        "cfg": {"bg": "#faf7f2", "card": "#ffffff", "fg": "#18181b", "accent": "#FF5C35", "accent2": "#18181b", "tiles": ["M", "T", "W", "T", "F", "S"], "sub": "Week 47 · 14 photos"},
    },
    "vsco": {
        "motionSlug": "film-preset-dial-scrub",
        "motionName": "Film Preset Intensity Rotary Dial",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 24},
        "props": ["transform: rotate (indicator needle)", "textContent (preset strength)"],
        "summary": "Adjusting a VSCO film preset rotates a minimalist monochrome dial across precision tick marks with spring detent snaps from A4 +2 to +12.",
        "hint": "Tap dial to step film intensity",
        "choreography": [
            "0-70ms: dial tap advances to the next preset strength detent.",
            "40-360ms: crisp indicator pill rotates smoothly around the 128px ring with slight overshoot.",
            "360-420ms: center monospace strength readout locks cleanly."
        ],
        "agentPrompt": "Build a minimalist VSCO film-preset rotary dial on #0d0d0e with monochrome #e4e4e7 needle: surround a 128px circle with radial tick marks at 20deg intervals and rotate the indicator over 420ms cubic-bezier(0.22, 1.22, 0.36, 1) across preset strengths.",
        "cfg": {"bg": "#0d0d0e", "card": "#18181b", "accent": "#e4e4e7", "label": "PRESET A6", "vals": ["+2.0", "+4.5", "+7.0", "+9.5", "+12"]},
    },
    "tumblr": {
        "motionSlug": "reblog-rainbow-burst",
        "motionName": "Reblog Pill Spring & Cyan Spark Burst",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 350, "c": 19},
        "props": ["transform: scale + rotate", "transform: translate (sparks)", "color"],
        "summary": "Reblogging a post on Tumblr snaps the reblog arrows into bright cyan with a crisp burst of particles over classic deep navy.",
        "hint": "Tap Reblog pill to trigger burst",
        "choreography": [
            "0-90ms: reblog icon pops 1.3x and tilts -8deg into #00cf35/#00b8ff glow.",
            "60-460ms: 6 radial micro-sparks fan outward cleanly.",
            "240-400ms: notes counter updates smoothly."
        ],
        "agentPrompt": "Recreate Tumblr's Reblog burst on #001935 deep navy with #00cf35 emerald highlight: spring-scale the reblog glyph 1.3x on toggle while radiating 6 dots over 480ms.",
        "cfg": {"bg": "#001935", "card": "#0b2747", "accent": "#00cf35", "author": "kinetic-archive", "body": "Saved this kinetic typography loop for midnight inspiration.", "icon": "⇄", "count": 264},
    },
    "wechat": {
        "motionSlug": "red-packet-seal-flip",
        "motionName": "Hongbao Red-Packet Gold Seal 3D Flip",
        "engine": "envelope_seal_reveal",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 310, "c": 20},
        "props": ["transform: rotateX (3D coin flip)", "background-color", "transition-delay"],
        "summary": "Opening a WeChat Red Packet flips crimson and imperial gold tiles in 3D perspective before revealing the lucky reward amount.",
        "hint": "Tap tiles to open Red Packet",
        "choreography": [
            "0ms: first crimson tile spins 360° in 3D perspective.",
            "70-360ms: alternating crimson (#d93829) and gold (#f5c26b) tiles cascade across.",
            "360-480ms: opened packet state holds warm festive contrast."
        ],
        "agentPrompt": "Build a WeChat Red Packet 3D flip reveal on #1a0d0d with #d93829 crimson and #eab308 gold tiles: stagger 6 tiles through rotateX(360deg) over 480ms cubic-bezier(0.22, 1.2, 0.36, 1) with 70ms delays.",
        "cfg": {"bg": "#1a0c0c", "card": "#2b1414", "accent": "#dc2626", "accent2": "#d97706", "tiles": ["福", "¥", "8", "8", ".", "8"], "sub": "Best wishes · Tap to open"},
    },
    "line": {
        "motionSlug": "sticker-bubble-cascade",
        "motionName": "Expressive Chat Sticker & Chip Cascade",
        "engine": "streaming_ai_cards",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 330, "c": 20},
        "props": ["opacity", "transform: translateY + scale"],
        "summary": "LINE's chat bar cascades bright emerald sticker suggestions and crisp message bubbles upward with snappy Japanese messaging polish.",
        "hint": "Tap chat card to replay sticker cascade",
        "choreography": [
            "0-260ms: sticker suggestion chips spring up sequentially in #06C755 green.",
            "160-400ms: chat text lines glide smoothly into view.",
            "400-460ms: blinking compose cursor holds clean rhythm."
        ],
        "agentPrompt": "Build LINE's quick-sticker chat cascade on #eefaf2 with #06C755 green badges: stagger 3 sticker pills upward (translateY 6px -> 0, scale 0.92 -> 1) by 90ms each over 380ms cubic-bezier(0.22, 1.2, 0.36, 1).",
        "cfg": {"bg": "#eefaf2", "card": "#ffffff", "fg": "#0f172a", "accent": "#06C755", "sources": ["🐻 Yay!", "🐰 On my way", "✨ Thanks"], "lines": ["Meet at Shibuya exit 8?", "Sending animated sticker now"]},
    },
    "viber": {
        "motionSlug": "violet-message-stream",
        "motionName": "Encrypted Chat Pill & Pulse Reveal",
        "engine": "streaming_ai_cards",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Fluid", "surface": "dark",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["opacity", "transform: translateY + scale"],
        "summary": "Viber's rich chat screen pairs purple quick-reaction pills rising on a crisp stagger with live message status updates.",
        "hint": "Tap thread to replay reveal",
        "choreography": [
            "0-260ms: violet status pills rise cleanly with 90ms stagger.",
            "160-400ms: message lines slide into focus.",
            "400-460ms: cursor blinks softly in #7360F2."
        ],
        "agentPrompt": "Create a Viber purple chat pill cascade on #141120 with #7360F2 accent: animate 3 rounded chips upward over 380ms cubic-bezier(0.22, 1.2, 0.36, 1) with 90ms spacing above staggered chat lines.",
        "cfg": {"bg": "#141120", "card": "#1f1a31", "accent": "#7360F2", "sources": ["HD Voice", "Pinned", "Seen ✓✓"], "lines": ["Voice room starting in 5 mins", "Tap to join HD audio"]},
    },
    "clubhouse": {
        "motionSlug": "speaker-audio-waveform",
        "motionName": "Live Audio Room Speaker Waveform",
        "engine": "waveform_audio",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Organic", "surface": "light",
        "dur": 260, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["background-color (active bars)", "transform: scaleY (voice peak)"],
        "summary": "Clubhouse's warm parchment stage drives a responsive multi-bar voice indicator that pulses warmly as speakers take the mic.",
        "hint": "Tap Play or bars to scrub audio room",
        "choreography": [
            "Continuous: 18 rounded bars animate left-to-right in warm amber-terracotta as speech progresses.",
            "Active bar scales vertically 1.22x to emphasize vocal cadence.",
            "Tap Play to mute/resume live room playback immediately."
        ],
        "agentPrompt": "Build Clubhouse's warm parchment voice-room waveform on #F2EFE4 with #d97706 speaker highlight: pair a 38px circular audio toggle with 18 variable-height bars where the active bar pulses scaleY(1.22).",
        "cfg": {"bg": "#f2efe4", "card": "#ffffff", "fg": "#1c1917", "accent": "#d97706", "accent2": "#b45309", "track": "Design Systems Room · Live", "bars": [34, 62, 84, 48, 92, 68, 52, 88, 74, 40, 80, 96, 60, 44, 72, 86, 54, 36]},
    },
    "hinge": {
        "motionSlug": "prompt-card-rose-swipe",
        "motionName": "Prompt Card Rose Send & Spring Dismiss",
        "engine": "card_swipe_deck",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 290, "c": 22},
        "props": ["transform: translate + rotate (card exit)", "opacity (stamp & next card promote)"],
        "summary": "Sending a Rose or skipping a Hinge prompt glides the top profile card diagonally out of the deck with a subtle tilt while the stacked card rises smoothly forward.",
        "hint": "Tap Rose/Skip or card to advance deck",
        "choreography": [
            "0-80ms: ROSE or SKIP stamp fades cleanly onto the corner of the active card.",
            "40-360ms: front card translates ±86px with ±14deg rotation while fading out.",
            "360-420ms: underlying card scales smoothly from 0.92 -> 1.0 into primary focus."
        ],
        "agentPrompt": "Build a Hinge editorial prompt card deck on #f6f4f1 with #7c2d52 plum-rose accent: stack two rounded cards where clicking Yes/No translates the front card ±86px with ±14deg tilt over 420ms cubic-bezier(0.22, 1.2, 0.36, 1) and promotes the next prompt smoothly.",
        "cfg": {"bg": "#f6f4f1", "card": "#ffffff", "fg": "#18181b", "accent": "#7c2d52", "accent2": "#be185d", "stampR": "ROSE 🌹", "stampL": "SKIP", "cards": [("Elena, 27", "Simple pleasure: morning espresso"), ("Liam, 30", "Green flag: makes playlists"), ("Nora, 26", "Two truths & a lie")]},
    },
    "bumble": {
        "motionSlug": "match-sheet-detent",
        "motionName": "24h Match Timer Sheet & Golden Prompt Chips",
        "engine": "sheet_detent_drawer",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 480, "ease": {"t": "spring", "k": 310, "c": 22},
        "props": ["transform: translateY (sheet rise)", "background-color (icebreaker chip)"],
        "summary": "Matching on Bumble springs up a warm golden icebreaker sheet with quick-tap opening moves that highlight instantaneously.",
        "hint": "Tap sheet or opening-move chips",
        "choreography": [
            "0-380ms: rounded bottom sheet glides upward from translateY(56px) -> 0 on spring(310, 22).",
            "160-480ms: tapping any opening move chip snaps it into bold Bumble gold (#FFC629)."
        ],
        "agentPrompt": "Create a Bumble match icebreaker bottom sheet on #fffbeb with #f59e0b/#FFC629 gold: spring-translate a rounded sheet from 56px to 0 over 480ms cubic-bezier(0.22, 1.18, 0.36, 1) containing selectable opening-move chips.",
        "cfg": {"bg": "#fffbeb", "card": "#ffffff", "fg": "#18181b", "accent": "#f59e0b", "sheetTitle": "It's a Match · 23h left", "chips": ["☕ Coffee?", "🎵 Fav song?", "✈️ Next trip?"], "cta": "Send Opening Move"},
    },
    "tinder": {
        "motionSlug": "card-swipe-stamp-tilt",
        "motionName": "Spring Card Swipe & LIKE/NOPE Stamp Tilt",
        "engine": "card_swipe_deck",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 20},
        "props": ["transform: translate + rotate", "opacity (LIKE/NOPE stamp)", "transform: scale (next card)"],
        "summary": "Tinder's iconic card stack tilts ±14° as it launches off-screen with a bold emerald LIKE or rose NOPE stamp while the underlying profile springs into focus.",
        "hint": "Tap ♥ / ✕ or card to swipe",
        "choreography": [
            "0-70ms: angled LIKE (#4ade80) or NOPE (#fb7185) stamp flashes onto the card corner.",
            "30-360ms: top card accelerates diagonally (±86px, -12px) rotating ±14° while fading out.",
            "360-420ms: next card scales up from 0.92 -> 1.0 to take the foreground."
        ],
        "agentPrompt": "Recreate Tinder's swipe card deck on #111318 with #FE3C72 -> #ff7854 gradient cards: on swipe left/right, reveal angled LIKE/NOPE stamps, translate the top card ±86px with ±14deg rotation over 420ms cubic-bezier(0.22, 1.2, 0.36, 1), and spring-promote the back card from scale(0.92) to 1.",
        "cfg": {"bg": "#111318", "card": "#1d2029", "accent": "#FE3C72", "accent2": "#ff7854", "stampR": "LIKE", "stampL": "NOPE", "cards": [("Chloe, 25", "2 miles away · Photographer"), ("Marcus, 28", "4 miles away · Chef"), ("Zoe, 24", "1 mile away · Illustrator")]},
    },
    "nextdoor": {
        "motionSlug": "neighborhood-sheet-pop",
        "motionName": "Local Alert Sheet & Neighborhood Pill Select",
        "engine": "sheet_detent_drawer",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 300, "c": 23},
        "props": ["transform: translateY", "background-color"],
        "summary": "Opening a local category filter in Nextdoor springs up a crisp white bottom drawer with leaf-green neighborhood radius chips.",
        "hint": "Tap sheet or distance chips",
        "choreography": [
            "0-380ms: bottom sheet rises from 56px peek to full detent smoothly.",
            "180-460ms: selected radius chip snaps into vibrant Nextdoor green (#16a34a)."
        ],
        "agentPrompt": "Build a Nextdoor neighborhood filter sheet on #f2faf0 with #16a34a green pills: animate the sheet translateY(56px -> 0) over 460ms cubic-bezier(0.22, 1.18, 0.36, 1) with interactive radius chips.",
        "cfg": {"bg": "#f2faf0", "card": "#ffffff", "fg": "#111827", "accent": "#16a34a", "sheetTitle": "Nearby Posts", "chips": ["0.5 mi", "2 mi", "5 mi"], "cta": "Apply Radius"},
    },
    "meetup": {
        "motionSlug": "event-rsvp-sheet",
        "motionName": "Event Seat RSVP Sheet & Slot Highlight",
        "engine": "sheet_detent_drawer",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 310, "c": 22},
        "props": ["transform: translateY", "background-color"],
        "summary": "Reserving a spot at a local Meetup slides up a high-contrast RSVP sheet where selecting session times lights up crimson pill chips.",
        "hint": "Tap sheet or pick a session time",
        "choreography": [
            "0-380ms: RSVP sheet rises cleanly into full detent.",
            "160-480ms: tapped session slot snaps to #F64060 coral fill."
        ],
        "agentPrompt": "Build a Meetup RSVP bottom sheet on #141218 with #F64060 coral accent: rise the drawer from translateY(56px) to 0 over 480ms cubic-bezier(0.22, 1.18, 0.36, 1) with 3 selectable session chips.",
        "cfg": {"bg": "#141218", "card": "#1f1c26", "accent": "#F64060", "sheetTitle": "Design & Motion Meetup", "chips": ["Thu 6pm", "Thu 7pm", "Sat 11am"], "cta": "Claim Free Seat"},
    },
    "twitch": {
        "motionSlug": "hype-train-follow-burst",
        "motionName": "Purple Follow Heart Burst & Hype Counter",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 380, "c": 17},
        "props": ["transform: scale + rotate", "transform: translate (purple sparks)", "background-color"],
        "summary": "Hitting Follow on a live Twitch channel fires six electric purple sparks outward while popping the heart icon and ticking up the live follower counter.",
        "hint": "Tap Follow pill to fire hype burst",
        "choreography": [
            "0-80ms: heart pops scale(1.3) rotate(-8deg) in #9146FF Twitch purple.",
            "60-460ms: 6 neon-violet sparks radiate outward and dissipate.",
            "240-400ms: live viewer/follower count increments cleanly."
        ],
        "agentPrompt": "Create Twitch's Follow heart burst on #0e0e10 with #9146FF purple highlight: spring-scale the heart 1.3x with -8deg tilt over 380ms cubic-bezier(0.22, 1.4, 0.36, 1) and launch 6 radial particles.",
        "cfg": {"bg": "#0e0e10", "card": "#18181b", "accent": "#9146FF", "author": "LIVE · shader_studio", "body": "Building 60fps GLSL transitions from scratch · Hype Train Lvl 4", "icon": "♥", "count": 4290},
    },
}

out = [build_motion_entry(META[slug], spec) for slug, spec in SPECS.items()]
dest = ROOT / "data" / "packs" / "apps-social.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(out)} motions to {dest.name}")
