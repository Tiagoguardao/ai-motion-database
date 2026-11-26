#!/usr/bin/env python3
"""Generates data/packs/apps-finance.json (25 iconic Finance & Crypto apps)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from app_motion_engines import build_motion_entry

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = {a["slug"]: a for a in json.loads((ROOT / ".cache/harvest_200_apps.json").read_text())["apps-finance"]}

SPECS = {
    "cash-app": {
        "motionSlug": "numpad-amount-spring",
        "motionName": "Numpad Amount Spring & Green Pay Bounce",
        "engine": "numpad_spring",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 340, "ease": {"t": "spring", "k": 380, "c": 20},
        "props": ["transform: scale (amount pop)", "background-color (send confirmation)", "opacity"],
        "summary": "Entering digits on Cash App's signature green home screen scales the oversized dollar figure with snappy spring overshoot while the rounded Pay pill confirms instantaneously.",
        "hint": "Tap digits or Pay to trigger bounce",
        "choreography": [
            "0-45ms: pressed keypad cell compresses to scale(0.9) for crisp tactile contact.",
            "45-240ms: hero currency figure scales 0.84 -> 1.12 -> 1.0 on spring(380, 20) as new digits append.",
            "240-340ms: Pay pill blooms into emerald confirmation state with soft shadow lift."
        ],
        "agentPrompt": "Build Cash App's numpad payment screen on #00D632 or deep obsidian #09130b with #00D632 accents: render an oversized tabular currency readout that springs scale(0.84 -> 1.12 -> 1) over 340ms cubic-bezier(0.22, 1.45, 0.36, 1) on every digit tap, paired with tactile keypad buttons and a rounded pill Pay CTA that confirms in place.",
        "cfg": {"bg": "#08140b", "card": "#122417", "accent": "#00D632", "accent2": "#00B82B", "currency": "$", "amounts": ["25", "45", "120", "85"], "cta": "Pay", "sub": "Cash Balance · Instant"},
    },
    "venmo": {
        "motionSlug": "social-payment-pulse",
        "motionName": "Emoji Payment Send & Social Feed Pop",
        "engine": "numpad_spring",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 360, "ease": {"t": "spring", "k": 340, "c": 21},
        "props": ["transform: scale", "background-color", "box-shadow"],
        "summary": "Venmo's peer-to-peer pay sheet pairs crisp blue amount bounces with playful instant confirmation feedback designed for casual split payments.",
        "hint": "Tap keypad digits or Pay pill",
        "choreography": [
            "0-50ms: digit tap depresses keycap 10% and shifts numeric readout.",
            "50-260ms: currency total springs upward with buoyant overshoot in Venmo cobalt (#008CFF).",
            "260-360ms: Pay CTA pulses into verified sent pill with subtle shadow bloom."
        ],
        "agentPrompt": "Implement a Venmo-style P2P payment keypad on a clean #f5f9ff surface with #008CFF primary buttons: animate the dollar figure on every input using spring(340, 21) scale(0.84 -> 1.12 -> 1) and transition the Pay pill cleanly into a confirmed state.",
        "cfg": {"bg": "#f2f7ff", "card": "#ffffff", "fg": "#0f172a", "accent": "#008CFF", "accent2": "#0070d6", "currency": "$", "amounts": ["18", "32", "64", "24"], "cta": "Pay @alex", "sub": "🍕 Dinner split · Friends"},
    },
    "robinhood": {
        "motionSlug": "sparkline-haptic-scrub",
        "motionName": "Live Sparkline Scrub & Price Odometer",
        "engine": "sparkline_scrub",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Hover", "feel": "Crisp", "surface": "dark",
        "dur": 240, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["cx/cy (SVG scrub dot)", "x1/x2 (vertical crosshair)", "textContent (live ticker)"],
        "summary": "Dragging across Robinhood's portfolio chart slides a crisp vertical hairline and glowing green node along the price spline while updating the live dollar valuation in lockstep.",
        "hint": "Move pointer or click chart to scrub",
        "choreography": [
            "0-60ms: pointer horizontal position maps to nearest tick sample along the SVG polyline.",
            "60-180ms: glowing #00C805 reticle and dashed vertical crosshair glide smoothly via cubic-bezier(0.22, 1, 0.36, 1).",
            "180-240ms: tabular price readout snaps to the exact timestamp value without layout shift."
        ],
        "agentPrompt": "Create a Robinhood interactive SVG sparkline on #0b0e11: draw a 2.2px #00C805 polyline over a translucent vertical gradient fill, track pointer X to glide a 4.5px dot and dashed vertical crosshair with 160ms cubic-bezier(0.22, 1, 0.36, 1), and update a monospace price header synchronously.",
        "cfg": {"bg": "#0b0e11", "card": "#13171d", "accent": "#00C805", "label": "Investing", "unit": "$", "delta": "+$412.80 (+2.71%)", "points": [50, 44, 47, 36, 40, 26, 30, 19, 23, 11], "values": ["14,820.10", "14,940.50", "14,880.00", "15,120.40", "15,060.20", "15,310.80", "15,240.00", "15,490.60", "15,410.15", "15,632.90"]},
    },
    "coinbase": {
        "motionSlug": "crypto-swap-flip",
        "motionName": "Instant Crypto Convert Flip & Rate Lock",
        "engine": "token_swap_flip",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Fluid", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 310, "c": 22},
        "props": ["transform: translateY (asset card swap)", "transform: rotate (180deg swap button)"],
        "summary": "Tapping Coinbase's central convert arrow rotates the cobalt button 180° while the source and destination asset cards cross-slide seamlessly into each other's slots.",
        "hint": "Tap swap arrow to invert pair",
        "choreography": [
            "0-80ms: circular #0052FF swap button depresses and begins a 180° rotation.",
            "40-340ms: BTC and USD cards translate vertically across each other by ±62px on spring(310, 22).",
            "340-420ms: swapped cards settle cleanly with zero overlap flicker."
        ],
        "agentPrompt": "Build a Coinbase crypto convert widget on #0a0b0d with #0052FF accent: stack two 54px asset cards separated by an 8px gap and overlay a centered 34px circular swap button; on toggle, rotate the button 180deg while translating the top card +62px and bottom card -62px over 420ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#0a0b0d", "card": "#14161c", "accent": "#0052FF", "a1": "BTC", "v1": "0.1840", "a2": "USD", "v2": "16,842.00"},
    },
    "paypal": {
        "motionSlug": "express-pay-confirm",
        "motionName": "Express Checkout Slide & Verified Blue Check",
        "engine": "swipe_rail_cta",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "light",
        "dur": 520, "ease": {"t": "spring", "k": 290, "c": 24},
        "props": ["transform: translateX (thumb)", "transform: scaleX (progress wash)", "color"],
        "summary": "PayPal's express payment rail glides a deep navy thumb across the pill track, sweeping a solid confirmation fill behind it before morphing the arrow into a checkmark.",
        "hint": "Click rail to confirm PayPal transfer",
        "choreography": [
            "0-120ms: circular #003087 thumb accelerates rightward across the 48px track.",
            "80-420ms: scaleX confirmation wash sweeps left-to-right while prompt text shifts from muted slate to white.",
            "420-520ms: thumb settles at the right cap with subtle spring overshoot and switches icon to ✓."
        ],
        "agentPrompt": "Recreate PayPal's slide-to-pay confirmation rail on #f5f7fa: use a 48px rounded track with a left-anchored scaleX(0->1) #003087 fill layer and a 40px circular handle that translates to the far edge over 520ms cubic-bezier(0.22, 1.14, 0.36, 1) while inverting colors into a verified checkmark.",
        "cfg": {"bg": "#eef2f9", "card": "#ffffff", "fg": "#0f172a", "accent": "#003087", "prompt": "Slide to Pay $68.00", "done": "Paid with PayPal ✓"},
    },
    "monzo": {
        "motionSlug": "hot-coral-card-freeze",
        "motionName": "Hot Coral Card Freeze Frost Wipe & 3D Tilt",
        "engine": "card_freeze_tilt",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 480, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["clip-path: inset (frost wipe)", "transform: rotateX + rotateY", "filter: saturate"],
        "summary": "Toggling Freeze on Monzo's iconic Hot Coral debit card wipes a frosted ice sheen across the surface via clip-path while desaturating and tilting the card in 3D perspective.",
        "hint": "Hover to tilt or tap Freeze card",
        "choreography": [
            "0-120ms: card tilts slightly backward in perspective(680px) as desaturation begins.",
            "80-420ms: translucent frosted glass overlay sweeps left-to-right via clip-path: inset(0 100% 0 0 -> 0 0 0 0).",
            "420-480ms: button label switches to 'Frozen ❄' while pointer tilt remains live."
        ],
        "agentPrompt": "Design Monzo's Hot Coral card freeze interaction on #111827: render a 222x126px #FF4F40 card inside perspective(680px) with pointer-driven rotateX/rotateY tilt and a diagonal sheen; on Freeze toggle, animate a frosted backdrop-filter: blur(5px) overlay with clip-path: inset(0 100% 0 0 -> 0) over 480ms cubic-bezier(0.22, 1, 0.36, 1) and filter: saturate(0.35).",
        "cfg": {"bg": "#111827", "card": "#1f2937", "accent": "#FF4F40", "accent2": "#e0382a", "brand": "monzo", "num": "•••• 8914", "toggle": "Freeze card", "toggleAlt": "Unfreeze ❄"},
    },
    "n26": {
        "motionSlug": "spaces-pill-switcher",
        "motionName": "Spaces Sub-Account Segmented Glide",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Crisp", "surface": "light",
        "dur": 380, "ease": {"t": "spring", "k": 330, "c": 24},
        "props": ["transform: translateX (shared thumb)", "color", "textContent"],
        "summary": "Switching between N26's Main Account, Travel Space, and Tax Vault glides a teal pill indicator cleanly beneath the labels with crisp German neo-bank restraint.",
        "hint": "Click tabs to switch N26 Spaces",
        "choreography": [
            "0-60ms: tapped segment highlights immediately while the shared indicator launches.",
            "60-320ms: #36A18B indicator slides across columns via translateX(i * 100%) on spring(330, 24).",
            "320-380ms: balance readout card updates to the selected Space's total."
        ],
        "agentPrompt": "Build an N26 Spaces segmented switcher on #f4f7f6 with #36A18B indicator: use a 3-column CSS grid with an absolutely positioned active thumb translating by translateX(index * 100%) over 380ms cubic-bezier(0.22, 1.18, 0.36, 1) above a minimalist balance summary card.",
        "cfg": {"bg": "#f3f7f6", "card": "#ffffff", "fg": "#111827", "accent": "#36A18B", "tabs": ["Main", "Travel", "Vault"], "tabVals": ["€4,280", "€1,150", "€9,400"]},
    },
    "nubank": {
        "motionSlug": "ultravioleta-card-tilt",
        "motionName": "Ultravioleta Metallic Card Sheen & Privacy Lock",
        "engine": "card_freeze_tilt",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Hover", "feel": "Silky", "surface": "dark",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: rotateX + rotateY", "transform: translateX (specular sheen)", "clip-path"],
        "summary": "Nubank's signature violet card catches a sweeping metallic highlight across its gradient face as you move the pointer, with a crisp one-tap privacy shield wipe.",
        "hint": "Move pointer or tap to lock card",
        "choreography": [
            "Continuous hover: pointer offsets drive subtle ±11° Y and ±8° X 3D tilt.",
            "0-460ms on click: specular gloss sweeps across the #820AD1 surface while privacy frost wipes over card digits.",
            "Release: card glides smoothly back to flat neutral plane."
        ],
        "agentPrompt": "Build Nubank's Ultravioleta 3D tilt card on #140821 using linear-gradient(135deg, #820AD1, #4c0680): add pointer-tracked rotateX/rotateY perspective tilt, a 115deg white specular sheen sweep, and a clip-path privacy frost toggle over 460ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#12071d", "card": "#231036", "accent": "#820AD1", "accent2": "#4f0582", "brand": "nu", "num": "•••• 3091", "toggle": "Hide details", "toggleAlt": "Hidden ••••"},
    },
    "klarna": {
        "motionSlug": "pay-in-4-stepper",
        "motionName": "Pay-in-4 Installment Step Progress Bar",
        "engine": "stepper_progress_flow",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 450, "ease": {"t": "spring", "k": 300, "c": 23},
        "props": ["width (connector fill)", "transform: scale (active milestone)", "box-shadow"],
        "summary": "Klarna's installment timeline animates a pink-and-ink progress connector across four scheduled bi-weekly payments, popping the active milestone ring with a soft halo.",
        "hint": "Tap any installment step",
        "choreography": [
            "0-80ms: selected payment milestone pops to scale(1.2) with a soft coral halo ring.",
            "40-380ms: horizontal progress track glides smoothly to the target step percentage.",
            "380-450ms: preceding nodes lock into filled completed state."
        ],
        "agentPrompt": "Build Klarna's Pay-in-4 installment stepper on #fff5f8 with #101114 ink and #f472b6 highlight: connect 4 circular step buttons over a 4px track whose fill width transitions over 450ms cubic-bezier(0.22, 1.15, 0.36, 1) while the current node scales 1.2x with a 5px translucent ring.",
        "cfg": {"bg": "#fff5f8", "card": "#ffffff", "fg": "#101114", "accent": "#e11d74", "steps": ["Today", "2 wks", "4 wks", "6 wks"]},
    },
    "ramp": {
        "motionSlug": "receipt-laser-auto-match",
        "motionName": "Receipt Laser Scan & Instant Expense Match",
        "engine": "barcode_laser_scan",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Loop", "feel": "Crisp", "surface": "dark",
        "dur": 420, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: translateY (volt laser beam)", "transform: scale (match pill)", "opacity"],
        "summary": "Ramp's automated receipt capture sweeps a luminous lime-yellow scan beam across receipt lines before snapping an instant policy-matched badge into focus.",
        "hint": "Tap scanner to trigger receipt match",
        "choreography": [
            "Continuous: 2.5px #d4e815 scan beam oscillates vertically across the receipt field with soft glow.",
            "0-360ms on hit: match pill springs from scale(0.9) opacity 0.65 to scale(1.04) full clarity.",
            "360-420ms: matched transaction total locks cleanly in monospace."
        ],
        "agentPrompt": "Create Ramp's receipt auto-match scanner on #111312 with #d4e815 electric-volt accent: animate a glowing horizontal laser line oscillating vertically across stylized receipt bars, paired with a bottom pill badge that springs to scale(1.04) when a receipt matches.",
        "cfg": {"bg": "#111312", "card": "#191c1a", "accent": "#cde016", "scanTitle": "Auto-Matched", "score": "$142.50"},
    },
    "mercury": {
        "motionSlug": "wire-approval-slide",
        "motionName": "Treasury Wire Slide-to-Approve Rail",
        "engine": "swipe_rail_cta",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 520, "ease": {"t": "spring", "k": 280, "c": 24},
        "props": ["transform: translateX (handle)", "transform: scaleX (indigo fill)", "color"],
        "summary": "Approving a high-value startup wire in Mercury uses a calm, deliberate slide-to-send rail that sweeps cool indigo across the track and flips into a verified confirmation.",
        "hint": "Click rail to approve wire transfer",
        "choreography": [
            "0-100ms: circular indigo thumb glides out of its left detent.",
            "80-440ms: full-height #5E6AD2 wash fills left-to-right behind crisp monospace text.",
            "440-520ms: handle snaps to the right cap and flips arrow to ✓."
        ],
        "agentPrompt": "Design Mercury's wire-transfer approval rail on #0e1017 with #5E6AD2 indigo: build a 48px pill track containing a scaleX(0->1) fill layer and a 40px circular thumb that translates to the right edge over 520ms cubic-bezier(0.22, 1.14, 0.36, 1) to confirm a $25,000 wire.",
        "cfg": {"bg": "#0e1017", "card": "#171a24", "accent": "#5E6AD2", "prompt": "Slide to send $25,000", "done": "Wire Sent ✓"},
    },
    "brex": {
        "motionSlug": "spend-limit-tabs",
        "motionName": "Corporate Spend Budget Segmented Morph",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Crisp", "surface": "dark",
        "dur": 380, "ease": {"t": "spring", "k": 340, "c": 25},
        "props": ["transform: translateX (active pill)", "color", "textContent"],
        "summary": "Toggling between Brex's Travel, Software, and Events spend limits glides a sharp orange indicator across the control bar while updating remaining monthly budgets.",
        "hint": "Click budget categories",
        "choreography": [
            "0-60ms: tapped category takes crisp white contrast immediately.",
            "60-320ms: #F46A25 sliding pill translates cleanly into the target column.",
            "320-380ms: bottom budget panel reflects the live remaining spend cap."
        ],
        "agentPrompt": "Build a Brex spend-limit segmented control on #121214 with #F46A25 accent: slide a rounded pill indicator across 3 equal columns using translateX(i * 100%) over 380ms cubic-bezier(0.22, 1.18, 0.36, 1) synchronized with a remaining-budget card.",
        "cfg": {"bg": "#121214", "card": "#1c1d21", "accent": "#F46A25", "tabs": ["Travel", "SaaS", "Events"], "tabVals": ["$12,400", "$48,900", "$6,250"]},
    },
    "wealthfront": {
        "motionSlug": "apy-cash-vessel",
        "motionName": "Cash Account APY Liquid Compound Fill",
        "engine": "liquid_fill_vessel",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "dark",
        "dur": 680, "ease": {"t": "spring", "k": 240, "c": 20},
        "props": ["height (liquid level)", "transform: translateX + rotate (wave crest)", "textContent"],
        "summary": "Wealthfront's automated savings goal fills a softly rounded indigo vessel with a gently undulating wave crest as monthly deposits compound toward the target.",
        "hint": "Tap vessel to add deposit step",
        "choreography": [
            "Continuous: dual-toned indigo wave crest sways gently left-to-right every 2.4s.",
            "0-560ms on click: liquid column rises smoothly with elastic overshoot to the next goal milestone.",
            "560-680ms: center tabular APY/progress readout updates cleanly over the fill."
        ],
        "agentPrompt": "Build a Wealthfront savings goal liquid vessel on #131126 with #4840BB/#6d63e8 fill: animate a rounded container's bottom-anchored fill height over 680ms cubic-bezier(0.22, 1.18, 0.36, 1) topped by a swaying curved wave crest.",
        "cfg": {"bg": "#121024", "card": "#1d1a38", "accent": "#635bff", "accent2": "#4840BB", "label": "4.50% APY", "vals": ["$12K", "$24K", "$38K", "$50K"]},
    },
    "betterment": {
        "motionSlug": "retirement-goal-ring",
        "motionName": "Retirement Goal Dual-Ring Progress Sweep",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Calm", "surface": "light",
        "dur": 720, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (outer & inner arcs)", "textContent"],
        "summary": "Betterment's goal tracker sweeps concentric blue and sky arcs around the projected target percentage to make long-term investment progress immediately legible.",
        "hint": "Tap ring to cycle projection scenarios",
        "choreography": [
            "0-180ms: concentric SVG tracks initialize from top 12-o'clock anchor.",
            "180-680ms: outer cobalt arc and inner sky arc sweep smoothly via stroke-dashoffset.",
            "680-720ms: center percentage and 'On track' pill settle cleanly."
        ],
        "agentPrompt": "Build a Betterment dual-ring SVG goal gauge on #f3f7fc with #1D6AE5 and #60a5fa strokes: animate two concentric circles rotated -90deg via stroke-dashoffset over 720ms cubic-bezier(0.22, 1, 0.36, 1) with a centered monospace percentage readout.",
        "cfg": {"bg": "#f3f7fc", "card": "#ffffff", "fg": "#0f172a", "accent": "#1D6AE5", "accent2": "#60a5fa", "label": "Goal Track", "unit": "%", "scores": [78, 86, 94, 68], "tag": "On track"},
    },
    "chime": {
        "motionSlug": "spotme-boost-fill",
        "motionName": "SpotMe Boost Liquid Reserve Meter",
        "engine": "liquid_fill_vessel",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 640, "ease": {"t": "spring", "k": 260, "c": 20},
        "props": ["height (mint fill)", "transform: translateX (wave surface)"],
        "summary": "Receiving a SpotMe boost in Chime raises a vibrant mint-green wave column inside the limit capsule with bouncy, friendly spring ease.",
        "hint": "Tap capsule to add +$5 SpotMe boost",
        "choreography": [
            "0-100ms: boost triggers upward surge in the mint liquid container.",
            "100-540ms: fluid level rises to the next SpotMe tier with gentle wave slosh.",
            "540-640ms: updated boost allowance locks in the center."
        ],
        "agentPrompt": "Build a Chime SpotMe liquid reserve meter on #eefbf4 with #1EC677 mint gradient: animate the rising fill height over 640ms cubic-bezier(0.22, 1.18, 0.36, 1) with an oscillating rounded top wave crest.",
        "cfg": {"bg": "#eefbf4", "card": "#ffffff", "fg": "#064e3b", "accent": "#1EC677", "accent2": "#10b981", "label": "SpotMe Limit", "vals": ["$40", "$80", "$140", "$200"]},
    },
    "sofi": {
        "motionSlug": "vault-allocation-switch",
        "motionName": "Savings Vault Tab Glide & APY Counter",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Fluid", "surface": "dark",
        "dur": 380, "ease": {"t": "spring", "k": 320, "c": 24},
        "props": ["transform: translateX (cyan pill)", "color", "textContent"],
        "summary": "Browsing SoFi's Checking, Vaults, and Invest buckets glides a bright cyan pill across the header while surfacing live balance and APY badges.",
        "hint": "Switch between SoFi buckets",
        "choreography": [
            "0-60ms: active tab text switches to high-contrast white.",
            "60-320ms: #00A2C7 pill glides horizontally with subtle spring overshoot.",
            "320-380ms: summary tile updates balance cleanly."
        ],
        "agentPrompt": "Implement SoFi's account bucket switcher on #0b141a with #00A2C7 cyan highlight: slide a shared-layout pill across Checking/Vaults/Invest over 380ms cubic-bezier(0.22, 1.18, 0.36, 1) paired with a live monospace summary row.",
        "cfg": {"bg": "#0b141a", "card": "#14222b", "accent": "#00A2C7", "tabs": ["Checking", "Vaults", "Invest"], "tabVals": ["$3,940", "$18,200", "$42,610"]},
    },
    "splitwise": {
        "motionSlug": "group-split-balance-flip",
        "motionName": "Group Split Balance Pair Swap",
        "engine": "token_swap_flip",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 22},
        "props": ["transform: translateY (payer/payee cards)", "transform: rotate (180deg swap)"],
        "summary": "Flipping payer and recipient in Splitwise rotates the teal swap button 180° while smoothly exchanging the two expense share cards vertically.",
        "hint": "Tap swap button to flip payer",
        "choreography": [
            "0-80ms: central #1CC29F circle rotates 180deg with spring kick.",
            "40-360ms: 'You paid' and 'Alex owes' rows exchange vertical slots seamlessly.",
            "360-420ms: settled cards align cleanly with crisp border contrast."
        ],
        "agentPrompt": "Build a Splitwise payer/payee swap card on #f2fbf9 with #1CC29F accent: vertically cross-translate two 54px balance rows by ±62px while rotating the central 34px swap button 180deg over 420ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#f2fbf9", "card": "#ffffff", "fg": "#0f172a", "accent": "#1CC29F", "a1": "YOU PAID", "v1": "$128.40", "a2": "SPLIT / 2", "v2": "$64.20"},
    },
    "copilot-money": {
        "motionSlug": "monthly-budget-ring",
        "motionName": "Monthly Budget Spend Ring & Pace Glow",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 720, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (budget & pace rings)", "filter: drop-shadow"],
        "summary": "Copilot Money's dark-mode budget card sweeps glowing cobalt and mint rings around remaining spend to show instantly whether you are under monthly pace.",
        "hint": "Tap ring to cycle budget categories",
        "choreography": [
            "0-160ms: dark OLED ring tracks prime with subtle radial glow.",
            "160-660ms: outer cobalt spend arc and inner pace ring animate simultaneously via stroke-dashoffset.",
            "660-720ms: center budget percentage and '$420 left' pill settle smoothly."
        ],
        "agentPrompt": "Create Copilot Money's OLED dark-mode budget ring on #0b0d14 with #4F6BFF and #34d399 strokes: animate two concentric SVG arcs over 720ms cubic-bezier(0.22, 1, 0.36, 1) with soft drop-shadow glow and a crisp pill status tag.",
        "cfg": {"bg": "#0b0d14", "card": "#151926", "accent": "#4F6BFF", "accent2": "#34d399", "label": "Monthly Cap", "unit": "%", "scores": [64, 78, 52, 89], "tag": "$420 under pace"},
    },
    "monarch-money": {
        "motionSlug": "net-worth-scrub-curve",
        "motionName": "Net Worth Interactive Area Scrub",
        "engine": "sparkline_scrub",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Hover", "feel": "Fluid", "surface": "dark",
        "dur": 240, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["cx/cy (dot)", "x1/x2 (hairline)", "textContent (net worth)"],
        "summary": "Scrubbing Monarch Money's warm-coral net worth spline glides the hairline marker across months while displaying exact historical net worth snapshots.",
        "hint": "Hover or tap chart to scrub net worth",
        "choreography": [
            "0-50ms: pointer X maps cleanly to monthly net-worth sample points.",
            "50-190ms: #FF6B35 marker dot and dashed vertical guide track with silk ease.",
            "190-240ms: tabular dollar total updates instantaneously."
        ],
        "agentPrompt": "Build Monarch Money's net worth scrub chart on #131110 with #FF6B35 stroke and vertical area gradient: track pointer X across the SVG path to glide the indicator dot and dashed vertical line over 160ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#131110", "card": "#1d1a18", "accent": "#FF6B35", "label": "Net Worth", "unit": "$", "delta": "+$18,420 (6M)", "points": [54, 48, 45, 41, 36, 33, 27, 24, 18, 13], "values": ["124,100", "126,800", "128,450", "130,900", "133,200", "135,600", "138,100", "139,850", "141,200", "142,520"]},
    },
    "phantom": {
        "motionSlug": "solana-token-swap-spin",
        "motionName": "Solana Token Swap Flip & Violet Pulse",
        "engine": "token_swap_flip",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 340, "c": 20},
        "props": ["transform: translateY (SOL/USDC cards)", "transform: rotate (180deg)"],
        "summary": "Swapping tokens in Phantom flips the signature lavender button 180° with spring overshoot while the SOL and USDC balance rows exchange places smoothly.",
        "hint": "Tap swap arrow to flip SOL ↔ USDC",
        "choreography": [
            "0-70ms: centered #AB9FF2 swap disc springs into a 180° rotation.",
            "40-360ms: SOL and USDC cards translate vertically past each other on spring(340, 20).",
            "360-420ms: swapped cards land with clean violet token badges."
        ],
        "agentPrompt": "Recreate Phantom wallet's token swap card on #1c1b22 with #AB9FF2 lavender accent: stack two 54px token cards with an overlapping 34px swap button; on click, rotate the button 180deg and cross-translate both cards ±62px over 420ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#18171e", "card": "#23222b", "accent": "#AB9FF2", "a1": "SOL", "v1": "18.40", "a2": "USDC", "v2": "3,412.80"},
    },
    "metamask": {
        "motionSlug": "eth-swap-network-flip",
        "motionName": "ETH Token Swap Flip & Fox-Orange Accent",
        "engine": "token_swap_flip",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 22},
        "props": ["transform: translateY", "transform: rotate"],
        "summary": "MetaMask's mobile swap sheet pairs a bold fox-orange central invert button with smooth vertical cross-translation of Ethereum token amounts.",
        "hint": "Tap orange arrow to swap ETH ↔ ARB",
        "choreography": [
            "0-70ms: #F6851B central circle spins 180° on tap.",
            "40-350ms: ETH and ARB balance cards glide vertically past each other.",
            "350-420ms: cards settle with crisp dark-slate borders."
        ],
        "agentPrompt": "Build MetaMask's token swap interaction on #121417 with #F6851B accent: animate two stacked asset cards translating ±62px vertically while the overlapping circular button rotates 180deg over 420ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#121417", "card": "#1b1f24", "accent": "#F6851B", "a1": "ETH", "v1": "1.250", "a2": "ARB", "v2": "4,190"},
    },
    "rainbow-wallet": {
        "motionSlug": "holo-wallet-card-tilt",
        "motionName": "Iridescent Holographic Wallet Card Tilt",
        "engine": "card_freeze_tilt",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Hover", "feel": "Playful", "surface": "dark",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: rotateX + rotateY", "transform: translateX (holographic sheen)", "clip-path"],
        "summary": "Rainbow's expressive wallet card responds to pointer tilt in 3D perspective with a prism gloss sweep and a playful one-tap vault privacy veil.",
        "hint": "Hover to tilt or tap to toggle privacy",
        "choreography": [
            "Hover: cursor position drives ±11° rotateY and ±8° rotateX with metallic sheen sweep.",
            "Tap: frosted veil wipes smoothly over ENS address and card sheen.",
            "Leave: card glides back to calm resting angle."
        ],
        "agentPrompt": "Create a Rainbow-style holographic crypto wallet card on #0a0f1f using a vibrant #3b82f6 -> #ec4899 gradient: add pointer-mapped 3D perspective tilt, diagonal specular sheen translation, and a smooth clip-path privacy frost toggle.",
        "cfg": {"bg": "#0a0f1f", "card": "#151d36", "accent": "#3b82f6", "accent2": "#ec4899", "brand": "rainbow.eth", "num": "0x71C…9a4E", "toggle": "Privacy blur", "toggleAlt": "Revealed 🌈"},
    },
    "ynab": {
        "motionSlug": "budget-envelope-bars",
        "motionName": "Zero-Based Envelope Category Fill Cascade",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 620, "ease": {"t": "spring", "k": 280, "c": 22},
        "props": ["width (staggered envelope bars)", "transition-delay (90ms stagger)"],
        "summary": "Assigning ready-to-assign dollars in YNAB cascades crisp indigo progress bars across Rent, Groceries, and Fun Money with a 90ms stagger.",
        "hint": "Tap card to fund budget envelopes",
        "choreography": [
            "0ms: first budget envelope bar begins expanding toward its monthly target.",
            "90-180ms: subsequent envelope bars stagger in cleanly with cubic-bezier(0.22, 1.16, 0.36, 1).",
            "480-620ms: funded percentages settle cleanly with tabular alignment."
        ],
        "agentPrompt": "Build YNAB's staggered envelope budget progress list on #f4f6fc with #3B5EDA -> #60a5fa bars: transition each 8px rounded bar's width over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with a 90ms per-row stagger delay.",
        "cfg": {"bg": "#f4f6fc", "card": "#ffffff", "fg": "#0f172a", "accent": "#3B5EDA", "accent2": "#60a5fa", "rows": [("Rent", 100), ("Groceries", 82), ("Travel", 64)]},
    },
    "acorns": {
        "motionSlug": "roundup-jar-fill",
        "motionName": "Spare Change Round-Up Liquid Jar Fill",
        "engine": "liquid_fill_vessel",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 660, "ease": {"t": "spring", "k": 260, "c": 20},
        "props": ["height (green fill level)", "transform: translateX (wave crest)"],
        "summary": "Each spare-change round-up in Acorns raises the vibrant leaf-green liquid level inside the rounded investment jar with a gentle wave motion.",
        "hint": "Tap jar to invest next round-up",
        "choreography": [
            "0-100ms: round-up click pushes liquid level upward smoothly.",
            "100-560ms: oscillating #74C947 wave surface settles at the next round-up milestone.",
            "560-660ms: updated round-up total centers clearly inside the jar."
        ],
        "agentPrompt": "Build an Acorns round-up jar animation on #f4fbf0 with #74C947 -> #4ea82a liquid fill: transition the container fill height over 660ms cubic-bezier(0.22, 1.18, 0.36, 1) topped by an oscillating wave crest.",
        "cfg": {"bg": "#f4fbf0", "card": "#ffffff", "fg": "#14532d", "accent": "#74C947", "accent2": "#4ea82a", "label": "Round-Ups", "vals": ["$1.45", "$3.20", "$4.85", "$5.00"]},
    },
    "trading-212": {
        "motionSlug": "pie-live-chart-scrub",
        "motionName": "AutoInvest Pie Live Return Scrub",
        "engine": "sparkline_scrub",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Hover", "feel": "Crisp", "surface": "dark",
        "dur": 240, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["cx/cy (dot)", "x1/x2 (guide)", "textContent"],
        "summary": "Scrubbing across a Trading 212 AutoInvest Pie chart smoothly tracks the glowing cyan marker and crosshair to preview exact historical return points.",
        "hint": "Hover or tap chart to scrub Pie value",
        "choreography": [
            "0-50ms: horizontal pointer coordinate resolves to discrete return samples.",
            "50-190ms: #00A7E1 dot and vertical dashed guide glide across the SVG curve.",
            "190-240ms: live Pie valuation updates cleanly in tabular monospace."
        ],
        "agentPrompt": "Create a Trading 212 AutoInvest Pie sparkline scrubber on #0c1118 with #00A7E1 cyan stroke and area fade: map pointer X to sample points and transition the indicator circle and vertical guide over 160ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#0c1118", "card": "#141c26", "accent": "#00A7E1", "label": "Tech Pie", "unit": "€", "delta": "+14.2% all time", "points": [52, 47, 41, 44, 35, 29, 32, 22, 17, 10], "values": ["8,120", "8,290", "8,490", "8,410", "8,760", "8,990", "8,880", "9,240", "9,410", "9,680"]},
    },
}

out = [build_motion_entry(META[slug], spec) for slug, spec in SPECS.items()]
dest = ROOT / "data" / "packs" / "apps-finance.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(out)} motions to {dest.name}")
