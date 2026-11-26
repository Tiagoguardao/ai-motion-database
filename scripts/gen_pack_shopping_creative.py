#!/usr/bin/env python3
"""Generates data/packs/apps-shopping-creative.json (25 iconic Shopping, Photo & Video Creative apps)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from app_motion_engines import build_motion_entry

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = {a["slug"]: a for a in json.loads((ROOT / ".cache/harvest_200_apps.json").read_text())["apps-shopping-creative"]}

SPECS = {
    "shop-app": {
        "motionSlug": "live-package-route-arc",
        "motionName": "Live Package Delivery Map Arc & Violet Beacon",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Fluid", "surface": "dark",
        "dur": 1150, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (violet arc)", "transform: translate (package pin)", "transform: scale (ping)"],
        "summary": "Tracking an order in Shop draws a vibrant #5A31F4 violet transit arc across a clean dark map while the parcel marker glides smoothly to your doorstep.",
        "hint": "Tap map to replay parcel tracking",
        "choreography": [
            "Continuous: destination beacon pulses softly in Shop violet.",
            "0-1150ms: route curve draws via stroke-dashoffset while package badge glides along.",
            "Top pill highlights 'Out for delivery' status."
        ],
        "agentPrompt": "Build Shop's live package tracking map on #110d1e with #5A31F4 violet SVG spline draw over 1150ms cubic-bezier(0.22, 1, 0.36, 1), moving package icon, and pulsing delivery beacon.",
        "cfg": {"bg": "#110d1e", "card": "#1b1430", "accent": "#6d4aff", "badge": "Out for delivery · 2pm", "marker": "📦"},
    },
    "amazon": {
        "motionSlug": "prime-buy-now-swipe",
        "motionName": "Prime Buy-Now Slide Rail & Instant Order Confirm",
        "engine": "swipe_rail_cta",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "light",
        "dur": 520, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateX (thumb)", "transform: scaleX (amber wash)"],
        "summary": "Amazon's one-swipe Buy Now rail glides a bright amber knob across the pill track to prevent accidental orders while delivering unmistakable checkout confirmation.",
        "hint": "Click rail to confirm Prime Buy Now",
        "choreography": [
            "0-100ms: #FF9900 circular knob glides rightward from left detent.",
            "80-440ms: full-height amber wash sweeps across behind bold white copy.",
            "440-520ms: handle snaps cleanly into ✓ Ordered."
        ],
        "agentPrompt": "Recreate Amazon's Swipe-to-Buy confirmation rail on #fdf8f0 with #f59e0b/#FF9900 wash and 40px sliding handle animating over 520ms cubic-bezier(0.22, 1.14, 0.36, 1).",
        "cfg": {"bg": "#fdf8f0", "card": "#ffffff", "fg": "#111827", "accent": "#f59e0b", "prompt": "Swipe to Buy Now · Prime", "done": "Order Placed ✓"},
    },
    "ebay": {
        "motionSlug": "auction-bid-swap-card",
        "motionName": "Live Auction Current vs. Max Bid Flip",
        "engine": "token_swap_flip",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 330, "c": 22},
        "props": ["transform: translateY (bid rows)", "transform: rotate (180deg)"],
        "summary": "Comparing live auction bids on eBay smoothly exchanges Current Bid and Your Max Bid cards vertically while rotating the central action disc 180°.",
        "hint": "Tap button to raise/toggle bid tiers",
        "choreography": [
            "0-70ms: #E53238 circular swap disc rotates 180°.",
            "40-360ms: Current Bid and Max Bid rows cross-translate vertically ±62px.",
            "360-420ms: updated bid cards settle crisply."
        ],
        "agentPrompt": "Build an eBay live auction bid comparison card on #fafafa with #E53238 crimson accent: vertically swap two 54px bid cards by ±62px while rotating the central button 180deg over 420ms.",
        "cfg": {"bg": "#fafafa", "card": "#ffffff", "fg": "#111827", "accent": "#E53238", "a1": "CURRENT", "v1": "$245.00", "a2": "YOUR BID", "v2": "$260.00"},
    },
    "depop": {
        "motionSlug": "streetwear-like-burst",
        "motionName": "Vintage Drop Heart Burst & Bold Red Pill",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 370, "c": 18},
        "props": ["transform: scale + rotate", "transform: translate (red sparks)", "color"],
        "summary": "Saving a vintage piece on Depop fires six punchy crimson sparks outward from the heart pill with high-energy streetwear spring bounce.",
        "hint": "Tap heart pill to save listing",
        "choreography": [
            "0-80ms: heart pops scale(1.3) rotate(-8deg) in #FF2300 Depop red.",
            "60-460ms: 6 radial red sparks fan outward cleanly.",
            "240-400ms: bag/likes count increments immediately."
        ],
        "agentPrompt": "Build Depop's listing heart burst on #ffffff with #FF2300 bold red accent: spring-scale the heart 1.3x and radiate 6 sparks over 480ms.",
        "cfg": {"bg": "#f7f7f8", "card": "#ffffff", "fg": "#101114", "accent": "#FF2300", "author": "@archivestudio · $88", "body": "90s Japanese Selvedge Work Jacket · Size M · Mint", "icon": "♥", "count": 134},
    },
    "vinted": {
        "motionSlug": "make-offer-price-flip",
        "motionName": "Make an Offer vs. Asking Price Card Swap",
        "engine": "token_swap_flip",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Fluid", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 310, "c": 22},
        "props": ["transform: translateY", "transform: rotate"],
        "summary": "Negotiating on Vinted smoothly flips Asking Price and Your Offer cards across a crisp turquoise action button.",
        "hint": "Tap teal arrow to toggle offer view",
        "choreography": [
            "0-70ms: #09B1BA teal button rotates 180°.",
            "40-360ms: Asking and Offer rows translate ±62px cleanly.",
            "360-420ms: price cards settle with soft shadow."
        ],
        "agentPrompt": "Build Vinted's offer/asking price swap card on #f0fafb with #09B1BA teal accent: cross-translate two 54px price rows ±62px over 420ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#f0fafb", "card": "#ffffff", "fg": "#0f172a", "accent": "#09B1BA", "a1": "ASKING", "v1": "€42.00", "a2": "OFFER", "v2": "€35.00"},
    },
    "stockx": {
        "motionSlug": "bid-ask-market-flip",
        "motionName": "Live Lowest Ask ↔ Highest Bid Market Swap",
        "engine": "token_swap_flip",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 340, "c": 23},
        "props": ["transform: translateY (Ask/Bid cards)", "transform: rotate (180deg)"],
        "summary": "Flipping between Buy Now (Lowest Ask) and Place Bid in StockX exchanges two stark market-order cards around a forest-green invert button.",
        "hint": "Tap green button to flip Ask ↔ Bid",
        "choreography": [
            "0-70ms: #006340/#16a34a central button spins 180°.",
            "40-360ms: Lowest Ask and Highest Bid rows cross-slide ±62px.",
            "360-420ms: sneaker market prices lock crisply in monospace."
        ],
        "agentPrompt": "Create StockX's Lowest Ask / Highest Bid market swap widget on #0e1210 with #16a34a StockX green: animate vertical card cross-translation and 180deg button rotation over 420ms.",
        "cfg": {"bg": "#0e1210", "card": "#171f1b", "accent": "#16a34a", "a1": "ASK", "v1": "$312", "a2": "BID", "v2": "$288"},
    },
    "goat": {
        "motionSlug": "sneaker-drop-tile-reveal",
        "motionName": "Sneaker Release Gallery 3D Tile Reveal",
        "engine": "envelope_seal_reveal",
        "use": "Typography", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "light",
        "dur": 480, "ease": {"t": "spring", "k": 300, "c": 22},
        "props": ["transform: rotateX", "background-color", "transition-delay"],
        "summary": "GOAT's monochrome gallery aesthetic flips stark architectural typography tiles in 3D perspective to announce verified sneaker drops.",
        "hint": "Tap tiles to trigger GOAT drop flip",
        "choreography": [
            "0ms: leading monochrome letter initiates 360° perspective X-flip.",
            "70-350ms: staggered architectural tiles alternate jet black and warm stone.",
            "350-480ms: crisp verified drop subline holds gallery poise."
        ],
        "agentPrompt": "Build GOAT's editorial sneaker drop tile flip on #f6f6f4 with #101114 and #52525b alternating 3D rotateX tiles staggered by 70ms over 480ms.",
        "cfg": {"bg": "#f6f6f4", "card": "#ffffff", "fg": "#101114", "accent": "#101114", "accent2": "#52525b", "tiles": ["G", "O", "A", "T", "9", "5"], "sub": "Verified Authentic · US 10"},
    },
    "nike": {
        "motionSlug": "snkrs-got-em-tile-reveal",
        "motionName": "SNKRS 'GOT EM' 3D Perspective Cascade",
        "engine": "envelope_seal_reveal",
        "use": "Typography", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 340, "c": 19},
        "props": ["transform: rotateX", "background-color", "transition-delay (70ms)"],
        "summary": "Winning a limited Nike SNKRS draw ripples bold 'GOT EM' letters in 3D perspective across stark black and infrared tiles.",
        "hint": "Tap tiles to celebrate SNKRS drop",
        "choreography": [
            "0ms: 'G' tile fires a crisp 360° perspective flip.",
            "70-350ms: remaining letters cascade across alternating ink and infrared.",
            "350-480ms: full 'GOT EM' win banner locks cleanly."
        ],
        "agentPrompt": "Build Nike SNKRS' 'GOT EM' celebration cascade on #0b0b0c with #ffffff/#ef4444 alternating 3D rotateX tiles staggered by 70ms over 480ms cubic-bezier(0.22, 1.2, 0.36, 1).",
        "cfg": {"bg": "#0b0b0c", "card": "#18181b", "accent": "#ef4444", "accent2": "#27272a", "tiles": ["G", "O", "T", "'", "E", "M"], "sub": "Air Max Pulse · Order Confirmed"},
    },
    "zara": {
        "motionSlug": "editorial-lookbook-tilt",
        "motionName": "Editorial Lookbook Card Tilt & Minimalist Veil",
        "engine": "card_freeze_tilt",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Editorial", "surface": "light",
        "dur": 480, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: rotateX + rotateY", "transform: translateX (editorial sheen)", "clip-path"],
        "summary": "ZARA's high-fashion mobile lookbook pairs razor-sharp monochrome minimalism with whisper-smooth 3D perspective tilt and frosted collection reveal.",
        "hint": "Hover to tilt or tap lookbook card",
        "choreography": [
            "Hover: pointer drives refined ±11° Y and ±8° X editorial tilt.",
            "Tap: frosted veil sweeps horizontally via clip-path over the lookbook card."
        ],
        "agentPrompt": "Create a ZARA minimalist monochrome lookbook card on #f7f6f3 with #101114 -> #3f3f46 card, subtle 3D pointer tilt, specular sweep, and clip-path frosted toggle.",
        "cfg": {"bg": "#f7f6f3", "card": "#ffffff", "fg": "#101114", "accent": "#18181b", "accent2": "#3f3f46", "brand": "Z A R A  ·  A/W", "num": "LOOK 04 · WOOL COAT", "toggle": "Quick View", "toggleAlt": "Added to Bag"},
    },
    "ikea": {
        "motionSlug": "swedish-flatpack-tile-reveal",
        "motionName": "Swedish Product Code 3D Tile Flip & Bag Pop",
        "engine": "envelope_seal_reveal",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 480, "ease": {"t": "spring", "k": 310, "c": 21},
        "props": ["transform: rotateX", "background-color (Swedish blue/gold)", "transition-delay"],
        "summary": "Adding an iconic piece in the IKEA app flips bold Swedish blue and yellow tiles in 3D perspective with crisp Nordic industrial charm.",
        "hint": "Tap tiles to flip IKEA product tag",
        "choreography": [
            "0ms: first letter starts a crisp 360° X-axis perspective rotation.",
            "70-350ms: alternating #0058A3 blue and #eab308 yellow tiles cascade smoothly.",
            "350-480ms: aisle/bin metadata holds clear legibility below."
        ],
        "agentPrompt": "Build IKEA's playful product tag 3D flip on #f5f7fa with #0058A3 blue and #eab308 yellow tiles staggered by 70ms over 480ms.",
        "cfg": {"bg": "#f5f7fa", "card": "#ffffff", "fg": "#0f172a", "accent": "#0058A3", "accent2": "#d97706", "tiles": ["K", "A", "L", "L", "A", "X"], "sub": "Aisle 14 · Bin 08 · In Stock"},
    },
    "etsy": {
        "motionSlug": "handmade-favorite-burst",
        "motionName": "Handmade Favorite Heart Burst & Terracotta Pill",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 350, "c": 19},
        "props": ["transform: scale + rotate", "transform: translate (terracotta sparks)", "background-color"],
        "summary": "Favoriting an artisan listing on Etsy blooms a warm #F1641E terracotta heart with radial craft sparks over soft linen white.",
        "hint": "Tap heart to favorite handmade piece",
        "choreography": [
            "0-80ms: heart pops 1.3x with subtle tilt in Etsy orange.",
            "60-460ms: 6 radial terracotta sparks burst cleanly outward.",
            "240-400ms: shop favorites counter ticks upward."
        ],
        "agentPrompt": "Create Etsy's handmade favorite heart burst on #faf6f2 with #F1641E orange accent: spring-scale the heart 1.3x and burst 6 dots over 480ms.",
        "cfg": {"bg": "#faf6f2", "card": "#ffffff", "fg": "#1c1917", "accent": "#F1641E", "author": "Kyoto Ceramic Studio", "body": "Wheel-thrown stoneware espresso cup · Handmade to order", "icon": "♥", "count": 628},
    },
    "asos": {
        "motionSlug": "saved-size-tile-flip",
        "motionName": "Saved Fit Size Selector 3D Tile Flip",
        "engine": "envelope_seal_reveal",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 330, "c": 22},
        "props": ["transform: rotateX", "background-color", "transition-delay"],
        "summary": "Selecting sizes in ASOS ripples crisp monochrome size tiles through a snappy 3D flip before highlighting in-stock fits.",
        "hint": "Tap size tiles to check stock flip",
        "choreography": [
            "0ms: XS tile begins 360° perspective flip.",
            "70-350ms: S–XXL tiles cascade across in bold jet black and emerald in-stock.",
            "350-460ms: settled size bar reads crisply."
        ],
        "agentPrompt": "Build ASOS's monochrome size-availability 3D tile flip on #f5f5f5 with #101114 and #16a34a tiles staggered by 70ms over 460ms.",
        "cfg": {"bg": "#f5f5f5", "card": "#ffffff", "fg": "#101114", "accent": "#101114", "accent2": "#16a34a", "tiles": ["X", "S", "M", "L", "X", "L"], "sub": "Free Express Delivery · Saved"},
    },
    "sephora": {
        "motionSlug": "beauty-insider-tier-stepper",
        "motionName": "Beauty Insider Rouge Tier Stepper Flow",
        "engine": "stepper_progress_flow",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 450, "ease": {"t": "spring", "k": 300, "c": 23},
        "props": ["width (rouge bar)", "transform: scale (tier milestone)", "box-shadow"],
        "summary": "Advancing through Sephora's Beauty Insider tiers sweeps a glossy rose-crimson bar across Insider, VIB, and Rouge milestones.",
        "hint": "Tap tier milestones to advance status",
        "choreography": [
            "0-80ms: active tier circle scales 1.2x with soft crimson glow.",
            "40-390ms: progress line sweeps smoothly to the target milestone.",
            "390-450ms: achieved beauty tiers lock solidly filled."
        ],
        "agentPrompt": "Create Sephora's Beauty Insider tier stepper on #111114 with #e11d48 rouge highlight and 4 interactive step nodes animating over 450ms cubic-bezier(0.22, 1.15, 0.36, 1).",
        "cfg": {"bg": "#111114", "card": "#1b1b20", "accent": "#e11d48", "steps": ["Join", "Insider", "VIB", "Rouge"]},
    },
    "capcut": {
        "motionSlug": "video-timeline-split-scrub",
        "motionName": "Video Cut & Grade Before/After Playhead Scrub",
        "engine": "split_before_after",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Tactile", "surface": "dark",
        "dur": 300, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset (grade preview)", "left (playhead divider)"],
        "summary": "Scrubbing CapCut's real-time filter playhead sweeps a vibrant color-graded cut across raw footage with razor-sharp vertical playhead tracking.",
        "hint": "Move pointer or tap to scrub cut",
        "choreography": [
            "0-50ms: pointer X moves the white vertical playhead smoothly.",
            "50-240ms: graded clip reveals seamlessly via clip-path: inset(0 0 0 p%).",
            "240-300ms: floating circular ↔ handle tracks in lockstep."
        ],
        "agentPrompt": "Build CapCut's real-time video color-grade playhead scrubber on #0d0e11 with #06b6d4 -> #8b5cf6 graded layer revealed via pointer-mapped clip-path: inset(0 0 0 X%).",
        "cfg": {"bg": "#0d0e11", "card": "#181a20", "accent": "#06b6d4", "accent2": "#8b5cf6", "leftLbl": "RAW 60FPS", "rightLbl": "GRADED LUT"},
    },
    "lightroom": {
        "motionSlug": "before-after-curtain-scrub",
        "motionName": "Before / After Interactive Split Curtain Drag",
        "engine": "split_before_after",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Silky", "surface": "dark",
        "dur": 300, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset (edited photo)", "left (split line)"],
        "summary": "Dragging Adobe Lightroom's Before/After curtain reveals developed RAW color grading instantaneously beneath a precision hairline divider.",
        "hint": "Move pointer or tap to compare RAW vs Edited",
        "choreography": [
            "Continuous hover: horizontal cursor tracks split curtain 12%–88% cleanly.",
            "0-240ms: edited layer updates clip-path without layout reflow.",
            "Center circular ↔ handle glides smoothly along the vertical seam."
        ],
        "agentPrompt": "Recreate Adobe Lightroom's Before/After split-curtain comparison on #11151c with #31A8FF -> #1d4ed8 developed layer clipped via clip-path: inset(0 0 0 X%) and synchronized vertical divider.",
        "cfg": {"bg": "#11151c", "card": "#19202b", "accent": "#31A8FF", "accent2": "#1d4ed8", "leftLbl": "ORIGINAL DNG", "rightLbl": "DEVELOPED"},
    },
    "snapseed": {
        "motionSlug": "tune-image-split-wipe",
        "motionName": "Tune Image Ambiance Split Wipe Preview",
        "engine": "split_before_after",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Tactile", "surface": "dark",
        "dur": 300, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset", "left"],
        "summary": "Holding and scrubbing Snapseed's preview curtain compares flat original tones against tuned leaf-green HDR ambiance instantaneously.",
        "hint": "Hover or tap to compare Tune Image",
        "choreography": [
            "Hover/Click: vertical divider glides smoothly across the viewfinder.",
            "Clipped edited frame reveals Snapseed's tuned contrast in real time."
        ],
        "agentPrompt": "Build Snapseed's Before/After Tune Image wipe on #121412 with #34A853 -> #15803d edited layer controlled by pointer-driven clip-path: inset(0 0 0 X%).",
        "cfg": {"bg": "#121412", "card": "#1b1f1b", "accent": "#34A853", "accent2": "#15803d", "leftLbl": "BEFORE", "rightLbl": "AMBIANCE +45"},
    },
    "halide": {
        "motionSlug": "manual-focus-knurled-dial",
        "motionName": "Tactile Knurled Manual-Focus & Aperture Dial",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 340, "c": 23},
        "props": ["transform: rotate (gold exposure needle)", "textContent (f-stop)"],
        "summary": "Halide's pro camera interface rotates a luminous yellow focus-peaking needle across precision Leica-style radial detents with crisp mechanical spring.",
        "hint": "Tap dial to step manual shutter / focus",
        "choreography": [
            "0-70ms: dial tap snaps to the next manual exposure detent.",
            "40-360ms: #FACC15 glowing indicator rotates smoothly around the 128px knurled ring.",
            "360-420ms: monospace shutter/aperture readout locks crisply."
        ],
        "agentPrompt": "Recreate Halide's manual camera rotary dial on #0a0a0c with #FACC15 viewfinder-yellow indicator rotating across 13 radial ticks over 420ms cubic-bezier(0.22, 1.22, 0.36, 1).",
        "cfg": {"bg": "#0a0a0c", "card": "#16161a", "accent": "#FACC15", "label": "PROCESS ZERO", "vals": ["1/60s", "1/125s", "1/250s", "1/500s", "1/1000s"]},
    },
    "kino": {
        "motionSlug": "cinema-lut-wipe-preview",
        "motionName": "Instant Grade Cinema LUT Split Wipe",
        "engine": "split_before_after",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Cinematic", "surface": "dark",
        "dur": 300, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset (LUT preview)", "left (curtain seam)"],
        "summary": "Swiping Kino's Instant Grade preview wipes warm Kodak-inspired cinema LUT color smoothly over flat Apple Log video.",
        "hint": "Hover or tap to compare Apple Log vs LUT",
        "choreography": [
            "Continuous hover: curtain scrubs smoothly between Apple Log and Instant Grade.",
            "Warm #FF4D2D cinema LUT layer tracks divider with zero frame lag."
        ],
        "agentPrompt": "Build Kino's Apple Log vs Cinema LUT split curtain on #0d0b0b with #FF4D2D -> #d97706 graded layer scrubbed via clip-path: inset(0 0 0 X%).",
        "cfg": {"bg": "#0d0b0b", "card": "#1a1616", "accent": "#FF4D2D", "accent2": "#d97706", "leftLbl": "APPLE LOG", "rightLbl": "KINO LUT 24P"},
    },
    "darkroom": {
        "motionSlug": "tone-curve-split-preview",
        "motionName": "Tone Curve Split-Compare Wipe & Violet Grade",
        "engine": "split_before_after",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Silky", "surface": "dark",
        "dur": 300, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset", "left"],
        "summary": "Darkroom's precision compare curtain slides smoothly across high-contrast photo grades so editors can verify shadows and highlights instantly.",
        "hint": "Move pointer or tap to compare tone curve",
        "choreography": [
            "Hover/Click: hairline divider glides cleanly across the frame.",
            "Clipped #8B5CF6 graded layer follows with silky cubic-bezier easing."
        ],
        "agentPrompt": "Create Darkroom's photo grade comparison curtain on #0f0d16 with #8B5CF6 -> #ec4899 developed layer scrubbed via clip-path: inset(0 0 0 X%).",
        "cfg": {"bg": "#0f0d16", "card": "#1b1726", "accent": "#8B5CF6", "accent2": "#ec4899", "leftLbl": "FLAT", "rightLbl": "CURVE + LUT"},
    },
    "procreate-pocket": {
        "motionSlug": "brush-size-opacity-scrub",
        "motionName": "Canvas Layer Compare & Brush Blend Wipe",
        "engine": "split_before_after",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Organic", "surface": "dark",
        "dur": 300, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset", "left"],
        "summary": "Comparing sketch linework against painted Gouache layers in Procreate Pocket wipes smoothly across a crisp dark studio frame.",
        "hint": "Hover or tap to compare Sketch vs Painted",
        "choreography": [
            "Hover/Click: divider glides across the illustration viewport.",
            "Crimson-magenta painted layer reveals seamlessly over monochrome linework."
        ],
        "agentPrompt": "Build Procreate Pocket's Sketch vs Painted layer wipe on #131116 with #E11D48 -> #f97316 painted canvas layer controlled by pointer clip-path.",
        "cfg": {"bg": "#131116", "card": "#1e1a22", "accent": "#E11D48", "accent2": "#f97316", "leftLbl": "6B SKETCH", "rightLbl": "GOUACHE"},
    },
    "canva": {
        "motionSlug": "magic-align-cursor-guides",
        "motionName": "Smart Alignment Guides & Collaborator Cursor Snap",
        "engine": "graph_cursor_canvas",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 800, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: translate (designer cursors)", "fill (snapped canvas nodes)"],
        "summary": "Collaborating on a Canva deck glides vibrant cyan and purple teammate cursors smoothly across snapped layout anchors on a crisp white artboard.",
        "hint": "Tap artboard to snap layout elements",
        "choreography": [
            "0-160ms: snapped anchor handles illuminate in #00C4CC Canva cyan.",
            "80-740ms: cyan and violet designer tags glide smoothly across the canvas.",
            "740-800ms: elements lock onto grid lines cleanly."
        ],
        "agentPrompt": "Build Canva's multiplayer artboard alignment preview on #f4fbfb with #00C4CC cyan and #8b5cf6 purple collaborator cursors gliding across SVG anchor nodes over 800ms.",
        "cfg": {"bg": "#f4fbfb", "card": "#ffffff", "fg": "#0f172a", "accent": "#00C4CC", "accent2": "#8b5cf6", "tag1": "Nina", "tag2": "Magic Resize"},
    },
    "unfold": {
        "motionSlug": "story-template-tile-flip",
        "motionName": "Minimalist Story Frame 3D Flip Cascade",
        "engine": "envelope_seal_reveal",
        "use": "Transitions", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "light",
        "dur": 480, "ease": {"t": "spring", "k": 290, "c": 22},
        "props": ["transform: rotateX", "background-color", "transition-delay"],
        "summary": "Previewing editorial Story templates in Unfold flips gallery-grade monochrome frame cards in crisp 3D perspective over warm cream paper.",
        "hint": "Tap frames to flip Story layout",
        "choreography": [
            "0ms: first frame tile initiates smooth 360° perspective rotation.",
            "70-350ms: staggered editorial tiles flip cleanly into matte charcoal.",
            "350-480ms: clean template subtitle anchors the composition."
        ],
        "agentPrompt": "Create Unfold's minimalist story-template 3D tile flip on #f7f5f0 with #18181b and #71717a matte tiles staggered by 70ms over 480ms.",
        "cfg": {"bg": "#f7f5f0", "card": "#ffffff", "fg": "#18181b", "accent": "#18181b", "accent2": "#71717a", "tiles": ["F", "I", "L", "M", "0", "4"], "sub": "CS Series · Editorial Frame"},
    },
    "dazz-cam": {
        "motionSlug": "retro-film-frame-flip",
        "motionName": "Retro Analog Film-Roll Frame Advance Flip",
        "engine": "envelope_seal_reveal",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 320, "c": 21},
        "props": ["transform: rotateX", "background-color (warm film amber)", "transition-delay"],
        "summary": "Advancing a 35mm roll in Dazz Cam clicks warm amber film-counter tiles through a tactile 3D flip over dark camera-body metal.",
        "hint": "Tap counter to wind next 35mm frame",
        "choreography": [
            "0ms: first frame-counter tile clicks through 360° X-rotation.",
            "70-350ms: warm #F59E0B amber and vermilion film frames cascade across.",
            "350-460ms: mechanical exposure counter settles crisply."
        ],
        "agentPrompt": "Build Dazz Cam's 35mm film-counter 3D flip on #12110f with #F59E0B amber and #ea580c tiles rotating around X-axis with 70ms stagger over 460ms.",
        "cfg": {"bg": "#12110f", "card": "#1e1c18", "accent": "#F59E0B", "accent2": "#ea580c", "tiles": ["C", "P", "M", "3", "5", "M"], "sub": "Exp 24 / 36 · ISO 400"},
    },
    "lapse": {
        "motionSlug": "darkroom-develop-flip",
        "motionName": "Darkroom Film Developing 3D Reveal",
        "engine": "envelope_seal_reveal",
        "use": "Transitions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 480, "ease": {"t": "spring", "k": 300, "c": 21},
        "props": ["transform: rotateX", "background-color", "transition-delay"],
        "summary": "Developing fresh snaps in Lapse's darkroom flips warm safelight-orange tiles in 3D perspective as your disposable roll finishes processing.",
        "hint": "Tap darkroom tiles to develop snaps",
        "choreography": [
            "0ms: first tile flips into glowing darkroom orange (#F97316).",
            "70-350ms: remaining tiles cascade smoothly across the strip.",
            "350-480ms: developed snap badge settles warmly."
        ],
        "agentPrompt": "Build Lapse's darkroom developing flip reveal on #140f0c with #F97316 safelight-orange and #db2777 tiles staggered by 70ms over 480ms.",
        "cfg": {"bg": "#140f0c", "card": "#221914", "accent": "#F97316", "accent2": "#db2777", "tiles": ["D", "E", "V", "E", "L", "P"], "sub": "3 snaps developed · Tap to view"},
    },
    "photomator": {
        "motionSlug": "ml-auto-enhance-wipe",
        "motionName": "ML Auto-Enhance Split Curtain Shimmer Wipe",
        "engine": "split_before_after",
        "use": "Transitions", "stack": "CSS", "trigger": "Hover", "feel": "Silky", "surface": "dark",
        "dur": 300, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset (ML enhanced)", "left (split line)"],
        "summary": "Photomator's ML Super Resolution & Auto-Enhance wipes vibrant pink-violet color fidelity smoothly across raw highlights as you scrub.",
        "hint": "Hover or tap to compare ML Enhance",
        "choreography": [
            "Hover/Click: precision split line scrubs smoothly across the image.",
            "Enhanced #EC4899 -> #8b5cf6 color layer tracks clip-path cleanly."
        ],
        "agentPrompt": "Create Photomator's ML Auto-Enhance comparison wipe on #130f16 with #EC4899 -> #8b5cf6 enhanced layer revealed via pointer-mapped clip-path: inset(0 0 0 X%).",
        "cfg": {"bg": "#130f16", "card": "#1e1724", "accent": "#EC4899", "accent2": "#8b5cf6", "leftLbl": "ORIGINAL", "rightLbl": "ML ENHANCE"},
    },
}

out = [build_motion_entry(META[slug], spec) for slug, spec in SPECS.items()]
dest = ROOT / "data" / "packs" / "apps-shopping-creative.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(out)} motions to {dest.name}")
