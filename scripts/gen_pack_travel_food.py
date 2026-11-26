#!/usr/bin/env python3
"""Generates data/packs/apps-travel-food.json (25 iconic Travel, Maps & Food apps)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from app_motion_engines import build_motion_entry

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = {a["slug"]: a for a in json.loads((ROOT / ".cache/harvest_200_apps.json").read_text())["apps-travel-food"]}

SPECS = {
    "uber": {
        "motionSlug": "pickup-radar-route-glide",
        "motionName": "Pickup Radar Pulse & Driver Route Spline",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Fluid", "surface": "dark",
        "dur": 1200, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (route spline)", "transform: translate (car pin)", "transform: scale (radar ping)"],
        "summary": "Matching with an Uber driver draws the curved pickup path across a stark monochrome map while a pulsing radar ring locks onto your curb and the driver glides in.",
        "hint": "Tap map to replay pickup approach",
        "choreography": [
            "Continuous: pickup pin radiates soft concentric radar pings every 1.8s.",
            "0-1150ms: black-and-white SVG route spline draws via stroke-dashoffset while driver marker tracks forward.",
            "900-1200ms: high-contrast '3 min away' ETA pill anchors the corner."
        ],
        "agentPrompt": "Build Uber's live driver pickup map on #0b0b0d with crisp white route spline: animate stroke-dashoffset from 260 -> 0 over 1200ms cubic-bezier(0.22, 1, 0.36, 1), glide the driver marker smoothly along the path, and pulse a concentric pickup radar ring.",
        "cfg": {"bg": "#0b0b0d", "card": "#16171b", "accent": "#ffffff", "badge": "UberX · 3 min", "marker": "🚗"},
    },
    "lyft": {
        "motionSlug": "magenta-route-spline-glide",
        "motionName": "Magenta Route Spline Draw & Arrival Ping",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 1150, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (magenta route)", "transform: translate (pin)", "transform: scale (ping)"],
        "summary": "Lyft traces a bright magenta pickup curve across dark slate streets while the driver marker glides toward a pulsing arrival halo.",
        "hint": "Tap map to replay Lyft route draw",
        "choreography": [
            "Continuous: destination halo pulses outward in #FF00BF.",
            "0-1150ms: curved SVG path draws smoothly while driver marker travels from origin to pickup.",
            "Top badge holds crisp ETA contrast."
        ],
        "agentPrompt": "Create a Lyft live route tracker on #120d16 with #FF00BF magenta spline draw over 1150ms cubic-bezier(0.22, 1, 0.36, 1), moving marker, and pulsing pickup ring.",
        "cfg": {"bg": "#120d16", "card": "#1d1524", "accent": "#FF00BF", "badge": "Lyft · 4 min", "marker": "🚘"},
    },
    "google-maps": {
        "motionSlug": "blue-dot-navigation-spline",
        "motionName": "Live Blue Navigation Spline & ETA Tracker",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 1150, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (Google Blue route)", "transform: translate", "transform: scale (radar)"],
        "summary": "Starting turn-by-turn navigation in Google Maps traces a vibrant #4285F4 route line across crisp map tiles while pulsing your live destination beacon.",
        "hint": "Tap map to replay navigation trace",
        "choreography": [
            "Continuous: destination marker pulses a soft blue beacon.",
            "0-1150ms: #4285F4 route path sweeps from start to destination while directional puck glides along.",
            "ETA chip displays live arrival duration cleanly."
        ],
        "agentPrompt": "Build a Google Maps route trace animation on #edf3fb with #4285F4 blue spline: animate stroke-dashoffset over 1150ms cubic-bezier(0.22, 1, 0.36, 1), translate the blue arrow puck along the curve, and pulse the target pin.",
        "cfg": {"bg": "#edf3fb", "card": "#ffffff", "fg": "#111827", "accent": "#4285F4", "badge": "14 min · Fastest", "marker": "➤"},
    },
    "waze": {
        "motionSlug": "live-hazard-route-radar",
        "motionName": "Live Traffic Route Draw & Sky Hazard Ping",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 1100, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (cyan route)", "transform: translate (car)", "transform: scale (alert ring)"],
        "summary": "Waze's night-mode navigation draws a neon sky-blue route around congestion while pulsing live community alert pings ahead.",
        "hint": "Tap map to replay Waze reroute",
        "choreography": [
            "Continuous: ahead alert pin radiates #33CCFF rings.",
            "0-1100ms: smooth spline traces the alternate route as the car marker advances.",
            "Top pill announces live time saved."
        ],
        "agentPrompt": "Create a Waze night-mode navigation reroute on #0f1722 with #33CCFF sky route stroke, moving car badge, and pulsing hazard ring.",
        "cfg": {"bg": "#0f1722", "card": "#172333", "accent": "#33CCFF", "badge": "-6 min reroute", "marker": "⚡"},
    },
    "citymapper": {
        "motionSlug": "multimodal-transit-sheet",
        "motionName": "Live Transit Departure Sheet & Route Chips",
        "engine": "sheet_detent_drawer",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 320, "c": 22},
        "props": ["transform: translateY (transit sheet)", "background-color (mode pill)"],
        "summary": "Opening a Citymapper trip springs up a friendly emerald route card where switching between Metro, Bus, and Bike snaps crisp departure chips.",
        "hint": "Tap sheet or switch transit mode",
        "choreography": [
            "0-380ms: rounded transit sheet springs upward from 56px peek to full height.",
            "160-460ms: tapping any mode chip highlights it in #2DC937 Citymapper green."
        ],
        "agentPrompt": "Build a Citymapper transit mode bottom sheet on #effaf0 with #2DC937 emerald chips: animate translateY(56px -> 0) over 460ms cubic-bezier(0.22, 1.18, 0.36, 1) with selectable Metro/Bus/Bike pills.",
        "cfg": {"bg": "#effaf0", "card": "#ffffff", "fg": "#111827", "accent": "#22c55e", "sheetTitle": "Next Departures", "chips": ["🚇 2m", "🚌 5m", "🚲 9m"], "cta": "GO · Live Route"},
    },
    "booking-com": {
        "motionSlug": "genius-stay-date-sheet",
        "motionName": "Genius Deal Date Sheet & Navy Confirm Snap",
        "engine": "sheet_detent_drawer",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateY", "background-color"],
        "summary": "Selecting stay dates in Booking.com lifts a structured deep-navy reservation drawer with snappy night-count pills and Genius savings CTA.",
        "hint": "Tap sheet or choose stay length",
        "choreography": [
            "0-380ms: reservation sheet glides up cleanly on spring(310, 23).",
            "160-460ms: selected night option snaps into #003580 Booking navy."
        ],
        "agentPrompt": "Create Booking.com's stay-length reservation drawer on #eef3fa with #003580 navy accents: spring-raise the sheet over 460ms cubic-bezier(0.22, 1.18, 0.36, 1) with 3 selectable stay chips.",
        "cfg": {"bg": "#eef3fa", "card": "#ffffff", "fg": "#0f172a", "accent": "#003580", "sheetTitle": "Genius Level 3 · -15%", "chips": ["2 Nights", "3 Nights", "5 Nights"], "cta": "Reserve Room"},
    },
    "expedia": {
        "motionSlug": "onekey-trip-picker-sheet",
        "motionName": "Trip Bundle Picker Sheet & Gold Highlight",
        "engine": "sheet_detent_drawer",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Fluid", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 310, "c": 22},
        "props": ["transform: translateY", "background-color"],
        "summary": "Bundling flights and stays in Expedia raises a navy-and-gold booking drawer with instant pill selection for package tiers.",
        "hint": "Tap sheet or choose bundle chip",
        "choreography": [
            "0-380ms: trip drawer rises smoothly into full view.",
            "160-460ms: tapped bundle tier switches to bright Expedia gold."
        ],
        "agentPrompt": "Build Expedia's bundle picker bottom sheet on #0b132b with #eab308 gold accents: raise the drawer from translateY(56px) to 0 over 460ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#0b132b", "card": "#152042", "accent": "#eab308", "sheetTitle": "OneKey Bundle", "chips": ["Flight", "Hotel", "+ Car"], "cta": "Unlock $180 Off"},
    },
    "hopper": {
        "motionSlug": "price-freeze-sheet-pop",
        "motionName": "Price Freeze Coral Drawer & Prediction Chips",
        "engine": "sheet_detent_drawer",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 480, "ease": {"t": "spring", "k": 330, "c": 21},
        "props": ["transform: translateY", "background-color"],
        "summary": "Freezing a flight fare in Hopper springs up a warm coral Price Freeze sheet where choosing hold durations lights up snappy pills.",
        "hint": "Tap sheet or pick freeze window",
        "choreography": [
            "0-380ms: rounded coral-accented drawer bounces smoothly into full detent.",
            "160-480ms: selected freeze window snaps into #FA6866 coral."
        ],
        "agentPrompt": "Build Hopper's Price Freeze bottom sheet on #fff4f4 with #FA6866 coral chips: spring-lift the sheet over 480ms cubic-bezier(0.22, 1.18, 0.36, 1) with selectable hold-duration pills.",
        "cfg": {"bg": "#fff4f4", "card": "#ffffff", "fg": "#18181b", "accent": "#FA6866", "sheetTitle": "Price Freeze · $384", "chips": ["3 Days", "7 Days", "14 Days"], "cta": "Freeze This Price"},
    },
    "tripit": {
        "motionSlug": "itinerary-timeline-stepper",
        "motionName": "Trip Itinerary Stage Connector & Gate Progress",
        "engine": "stepper_progress_flow",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 450, "ease": {"t": "spring", "k": 300, "c": 23},
        "props": ["width (itinerary bar)", "transform: scale (active leg)", "box-shadow"],
        "summary": "TripIt advances an airline-blue itinerary connector cleanly across Flight, Hotel, Transfer, and Return legs as your trip unfolds.",
        "hint": "Tap any trip leg to highlight stage",
        "choreography": [
            "0-80ms: active leg circle pops 1.2x with crisp #0066CC halo.",
            "40-390ms: horizontal progress bar sweeps cleanly across stages.",
            "390-450ms: completed legs lock filled."
        ],
        "agentPrompt": "Build TripIt's itinerary leg stepper on #f2f7fd with #0066CC blue progress fill: animate a 4px connector bar and 4 step nodes scaling 1.2x over 450ms cubic-bezier(0.22, 1.15, 0.36, 1).",
        "cfg": {"bg": "#f2f7fd", "card": "#ffffff", "fg": "#0f172a", "accent": "#0066CC", "steps": ["Check-in", "Flight", "Hotel", "Return"]},
    },
    "delta": {
        "motionSlug": "boarding-pass-card-tilt",
        "motionName": "SkyMiles Boarding Pass 3D Tilt & Crimson Sheen",
        "engine": "card_freeze_tilt",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Hover", "feel": "Silky", "surface": "dark",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: rotateX + rotateY", "transform: translateX (foil sheen)", "clip-path"],
        "summary": "Delta's SkyMiles boarding pass gleams with a subtle metallic sweep across deep navy-crimson as you tilt it, with one-tap gate-pass lock.",
        "hint": "Hover to tilt or tap pass to lock",
        "choreography": [
            "Hover: pointer coordinates tilt the boarding pass ±11° Y and ±8° X.",
            "Tap: diagonal gloss sweeps across the #C8102E -> #1d2951 gradient while boarding status toggles."
        ],
        "agentPrompt": "Create a Delta SkyMiles boarding pass tilt card on #0d1221 with #C8102E -> #1e3a8a gradient: add perspective(680px) pointer tilt, diagonal light sheen, and clip-path boarding lock toggle.",
        "cfg": {"bg": "#0d1221", "card": "#182138", "accent": "#C8102E", "accent2": "#1e3a8a", "brand": "DELTA · DL 412", "num": "GATE B14 · 12A", "toggle": "Boarded lock", "toggleAlt": "Checked in ✓"},
    },
    "united": {
        "motionSlug": "gate-boarding-stepper",
        "motionName": "Flight Boarding Group Stepper & Live Progress",
        "engine": "stepper_progress_flow",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 450, "ease": {"t": "spring", "k": 310, "c": 24},
        "props": ["width (boarding bar)", "transform: scale (group node)"],
        "summary": "United's live flight tracker advances an aviation-blue bar through Bags, Security, Boarding, and Takeoff with crisp active-stage focus.",
        "hint": "Tap any flight stage to step forward",
        "choreography": [
            "0-80ms: active flight milestone scales 1.2x with #005DAA blue halo.",
            "40-390ms: progress connector expands smoothly to the active milestone.",
            "390-450ms: prior steps lock into solid completed state."
        ],
        "agentPrompt": "Build United Airlines' live flight milestone bar on #0b1320 with #0ea5e9/#005DAA accent: animate a 4px connector bar and 4 interactive nodes over 450ms cubic-bezier(0.22, 1.15, 0.36, 1).",
        "cfg": {"bg": "#0b1320", "card": "#142033", "accent": "#0284c7", "steps": ["Bags", "Gate", "Boarding", "In Air"]},
    },
    "alltrails": {
        "motionSlug": "topographic-trail-trace",
        "motionName": "Topographic Trail Route Trace & Summit Ping",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Organic", "surface": "light",
        "dur": 1200, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (trail line)", "transform: translate (hiker pin)", "transform: scale (summit ping)"],
        "summary": "Previewing a hike on AllTrails draws a crisp forest-green trail line across dotted terrain while pulsing the summit marker.",
        "hint": "Tap map to trace trail route",
        "choreography": [
            "Continuous: summit pin radiates soft emerald beacon rings.",
            "0-1200ms: #2C5601/#15803d trail spline draws cleanly as the hiker marker climbs along it."
        ],
        "agentPrompt": "Build AllTrails' trail route preview on #f2f7f0 with #15803d forest-green SVG stroke-dashoffset animation over 1200ms cubic-bezier(0.22, 1, 0.36, 1) and pulsing summit marker.",
        "cfg": {"bg": "#f2f7f0", "card": "#ffffff", "fg": "#14532d", "accent": "#15803d", "badge": "5.4 mi · +1,120 ft", "marker": "🥾"},
    },
    "komoot": {
        "motionSlug": "cycling-waypoint-route-draw",
        "motionName": "Cycling Waypoint Spline Draw & Live Distance",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Fluid", "surface": "dark",
        "dur": 1150, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (route)", "transform: translate (cyclist marker)", "transform: scale"],
        "summary": "Komoot's outdoor planner traces a vibrant olive-green cycling line through waypoints with smooth GPS progression across dark topo dots.",
        "hint": "Tap map to replay cycling route",
        "choreography": [
            "Continuous: waypoint beacon pulses cleanly in #6AA127.",
            "0-1150ms: route curve draws seamlessly while bike marker glides forward."
        ],
        "agentPrompt": "Build Komoot's waypoint route draw on #121710 with #6AA127 olive-green SVG spline animation over 1150ms cubic-bezier(0.22, 1, 0.36, 1) and moving bike badge.",
        "cfg": {"bg": "#121710", "card": "#1b2418", "accent": "#6AA127", "badge": "28.4 km · Gravel", "marker": "🚴"},
    },
    "lime": {
        "motionSlug": "scooter-unlock-slide-rail",
        "motionName": "Electric Scooter Slide-to-Unlock Rail",
        "engine": "swipe_rail_cta",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 520, "ease": {"t": "spring", "k": 310, "c": 22},
        "props": ["transform: translateX (electric knob)", "transform: scaleX (lime wash)"],
        "summary": "Unlocking a Lime scooter sweeps neon electric-green across the tactile pill rail before snapping into an active unlocked ride state.",
        "hint": "Click rail to unlock scooter",
        "choreography": [
            "0-100ms: circular #00DD00 thumb launches rightward.",
            "80-440ms: full-width neon lime wash fills cleanly behind white text.",
            "440-520ms: handle snaps into ✓ Unlocked."
        ],
        "agentPrompt": "Build Lime's scooter unlock rail on #0c140e with #00c800 neon-green track wash and 40px circular thumb translating across the rail over 520ms cubic-bezier(0.22, 1.14, 0.36, 1).",
        "cfg": {"bg": "#0c140e", "card": "#162419", "accent": "#00c800", "prompt": "Slide to Unlock · 84%", "done": "Unlocked — Ride Safe ✓"},
    },
    "bolt": {
        "motionSlug": "emerald-driver-eta-glide",
        "motionName": "Driver Approach Spline & Emerald ETA Ping",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 1150, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (emerald curve)", "transform: translate (car)", "transform: scale (ping)"],
        "summary": "Bolt tracks an arriving driver along a bright #34D186 emerald route spline into a gently pulsing pickup beacon.",
        "hint": "Tap map to replay driver arrival",
        "choreography": [
            "Continuous: pickup pin radiates emerald arrival rings.",
            "0-1150ms: route curve draws cleanly while car marker approaches."
        ],
        "agentPrompt": "Create Bolt's driver arrival tracker on #0d1512 with #34D186 emerald route stroke-dashoffset draw over 1150ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#0d1512", "card": "#16241f", "accent": "#34D186", "badge": "Bolt · 2 min · €6.40", "marker": "🚕"},
    },
    "doordash": {
        "motionSlug": "delivery-stage-bounce",
        "motionName": "Live Order Delivery Stage Progress Stepper",
        "engine": "stepper_progress_flow",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 450, "ease": {"t": "spring", "k": 320, "c": 21},
        "props": ["width (red delivery bar)", "transform: scale (stage badge)", "box-shadow"],
        "summary": "DoorDash's live order tracker sweeps bold vermilion progress across Confirmed, Kitchen, Dasher, and Doorstep with a buoyant active-stage pop.",
        "hint": "Tap stages to advance food delivery",
        "choreography": [
            "0-80ms: active delivery icon scales 1.2x with #FF3008 coral halo.",
            "40-390ms: red progress bar glides cleanly to the active step.",
            "390-450ms: completed stages lock solid crimson."
        ],
        "agentPrompt": "Build DoorDash's live delivery stage tracker on #fff5f3 with #FF3008 vermilion progress connector and 4 interactive nodes scaling 1.2x over 450ms cubic-bezier(0.22, 1.15, 0.36, 1).",
        "cfg": {"bg": "#fff5f3", "card": "#ffffff", "fg": "#18181b", "accent": "#FF3008", "steps": ["Placed", "Kitchen", "Dasher", "Door"]},
    },
    "uber-eats": {
        "motionSlug": "cart-sheet-quick-add",
        "motionName": "Quick-Add Dish Sheet & Emerald Cart Confirm",
        "engine": "sheet_detent_drawer",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 320, "c": 22},
        "props": ["transform: translateY (modifier sheet)", "background-color (size chip)"],
        "summary": "Customizing an Uber Eats dish glides up a sleek dark modifier sheet with snappy emerald portion chips and an instant Add-to-Cart CTA.",
        "hint": "Tap sheet or pick dish size",
        "choreography": [
            "0-380ms: modifier sheet rises cleanly on spring(320, 22).",
            "160-460ms: selected portion chip illuminates in #06C167 Uber Eats green."
        ],
        "agentPrompt": "Build Uber Eats' dish customizer bottom sheet on #0e1110 with #06C167 emerald accents: lift the drawer from translateY(56px) to 0 over 460ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#0e1110", "card": "#181d1b", "accent": "#06C167", "sheetTitle": "Spicy Salmon Bowl", "chips": ["Regular", "Large", "+ Avocado"], "cta": "Add to Cart · $16.50"},
    },
    "deliveroo": {
        "motionSlug": "teal-rider-map-tracker",
        "motionName": "Teal Rider Map Glide & Live Minute Ping",
        "engine": "radar_map_tracker",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 1150, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (teal path)", "transform: translate (rider pin)", "transform: scale (ping)"],
        "summary": "Deliveroo animates a crisp #00CCBC turquoise route curve as your rider glides smoothly across the neighborhood map toward your pulsing doorstep pin.",
        "hint": "Tap map to replay rider approach",
        "choreography": [
            "Continuous: home pin pulses soft teal rings.",
            "0-1150ms: turquoise route draws smoothly while scooter pin travels along."
        ],
        "agentPrompt": "Build Deliveroo's rider tracker map on #eefcfb with #00CCBC turquoise SVG route draw over 1150ms cubic-bezier(0.22, 1, 0.36, 1), animated rider pin, and pulsing destination beacon.",
        "cfg": {"bg": "#eefcfb", "card": "#ffffff", "fg": "#0f172a", "accent": "#00CCBC", "badge": "Arriving in 7 min", "marker": "🛵"},
    },
    "instacart": {
        "motionSlug": "grocery-stepper-drawer",
        "motionName": "Grocery Delivery Window Sheet & Green Chips",
        "engine": "sheet_detent_drawer",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateY", "background-color"],
        "summary": "Choosing an Instacart grocery delivery window slides up a clean white sheet with bright produce-green slot pills for Priority, 2-Hour, and Scheduled delivery.",
        "hint": "Tap sheet or pick delivery window",
        "choreography": [
            "0-380ms: delivery window drawer glides up smoothly.",
            "160-460ms: chosen speed chip lights up in #43B02A Instacart green."
        ],
        "agentPrompt": "Build Instacart's delivery slot bottom sheet on #f2faf0 with #43B02A green pills: spring-lift the drawer over 460ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#f2faf0", "card": "#ffffff", "fg": "#111827", "accent": "#43B02A", "sheetTitle": "Delivery Window", "chips": ["Priority 35m", "2-Hour", "5–7 PM"], "cta": "Checkout Cart (8)"},
    },
    "opentable": {
        "motionSlug": "reservation-slot-drawer",
        "motionName": "Dining Time-Slot Sheet & Crimson Table Confirm",
        "engine": "sheet_detent_drawer",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 310, "c": 22},
        "props": ["transform: translateY (table sheet)", "background-color (crimson slot)"],
        "summary": "Booking a table on OpenTable lifts a clean reservation sheet with signature crimson time-slot pills that snap immediately on tap.",
        "hint": "Tap sheet or select dinner time",
        "choreography": [
            "0-380ms: reservation drawer rises smoothly to full detent.",
            "160-460ms: tapped seating time highlights in #DA3743 crimson."
        ],
        "agentPrompt": "Build OpenTable's table reservation bottom sheet on #fdf4f5 with #DA3743 crimson time-slot pills rising over 460ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#fdf4f5", "card": "#ffffff", "fg": "#18181b", "accent": "#DA3743", "sheetTitle": "Table for 2 · Tonight", "chips": ["6:45 PM", "7:30 PM", "8:15 PM"], "cta": "Complete Reservation"},
    },
    "resy": {
        "motionSlug": "notify-seating-sheet",
        "motionName": "Editorial Seating Sheet & Terracotta Slot Highlight",
        "engine": "sheet_detent_drawer",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 300, "c": 23},
        "props": ["transform: translateY", "background-color"],
        "summary": "Resy's dark hospitality sheet lifts dining room, patio, and bar seating pills with refined terracotta accent highlights.",
        "hint": "Tap sheet or pick seating area",
        "choreography": [
            "0-380ms: dark hospitality drawer glides smoothly upward.",
            "160-460ms: selected seating option lights up in #D3452A terracotta."
        ],
        "agentPrompt": "Create Resy's dark seating selector bottom sheet on #141212 with #D3452A terracotta pills rising over 460ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#141212", "card": "#1f1c1c", "accent": "#D3452A", "sheetTitle": "Via Carota · Notify", "chips": ["Bar 7:00", "Patio 7:45", "Indoor 8:30"], "cta": "Book Seat"},
    },
    "beli": {
        "motionSlug": "head-to-head-restaurant-rank",
        "motionName": "Head-to-Head Restaurant Rank Swipe Deck",
        "engine": "card_swipe_deck",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 21},
        "props": ["transform: translate + rotate", "opacity (LOVED/MEH stamp)", "transform: scale"],
        "summary": "Ranking a restaurant in Beli swings the venue card out with a crisp LOVED or SKIP stamp while promoting the next head-to-head spot in your list.",
        "hint": "Tap ♥ / ✕ to rank restaurant",
        "choreography": [
            "0-70ms: LOVED or PASS badge flashes cleanly across the dining card.",
            "40-360ms: card exits ±86px at ±14° tilt.",
            "360-420ms: next restaurant card pops forward from scale(0.92) -> 1."
        ],
        "agentPrompt": "Build Beli's restaurant ranking swipe deck on #f0f7f8 with #0B5D69 deep-teal cards, LOVED/PASS stamps, and 420ms cubic-bezier(0.22, 1.2, 0.36, 1) card promotion.",
        "cfg": {"bg": "#f0f7f8", "card": "#ffffff", "fg": "#0f172a", "accent": "#0B5D69", "accent2": "#0e7490", "stampR": "9.4 ★", "stampL": "PASS", "cards": [("Prado · Lisbon", "Modern Portuguese · $$"), ("Lilia · Brooklyn", "Handmade Pasta · $$$"), ("Barrafina · Soho", "Tapas Counter · $$")]},
    },
    "starbucks": {
        "motionSlug": "gold-star-cup-fill",
        "motionName": "Rewards Cup Liquid Fill & Star Tier Surge",
        "engine": "liquid_fill_vessel",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 680, "ease": {"t": "spring", "k": 250, "c": 20},
        "props": ["height (emerald liquid)", "transform: translateX (wave surface)"],
        "summary": "Earning Stars in Starbucks raises a rich Siren-green liquid column inside the rewards tumbler with a gentle oscillating wave crest.",
        "hint": "Tap cup to add +50 Bonus Stars",
        "choreography": [
            "0-100ms: tap triggers upward surge inside the rounded rewards cup.",
            "100-580ms: #00704A liquid wave rises with soft overshoot toward 200 Stars.",
            "580-680ms: centered star count updates crisply."
        ],
        "agentPrompt": "Create Starbucks' Rewards liquid cup fill on #f0f8f4 with #00704A -> #059669 wave gradient rising over 680ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#f0f8f4", "card": "#ffffff", "fg": "#064e3b", "accent": "#00704A", "accent2": "#047857", "label": "Bonus Stars", "vals": ["75 ★", "125 ★", "175 ★", "200 ★"]},
    },
    "too-good-to-go": {
        "motionSlug": "surprise-bag-reserve-rail",
        "motionName": "Surprise Bag Slide-to-Reserve Emerald Rail",
        "engine": "swipe_rail_cta",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "light",
        "dur": 520, "ease": {"t": "spring", "k": 300, "c": 23},
        "props": ["transform: translateX (thumb)", "transform: scaleX (teal fill)"],
        "summary": "Reserving a Surprise Bag in Too Good To Go sweeps deep pine teal across the confirmation rail to prevent accidental pickups while feeling super rewarding.",
        "hint": "Click rail to reserve Surprise Bag",
        "choreography": [
            "0-100ms: circular #00635B handle launches rightward across the pill rail.",
            "80-440ms: full-height pine-teal wash expands behind crisp confirmation copy.",
            "440-520ms: handle settles at right edge with ✓ badge."
        ],
        "agentPrompt": "Build Too Good To Go's Surprise Bag slide-to-reserve rail on #eef7f6 with #00635B pine-teal scaleX fill and sliding 40px knob over 520ms cubic-bezier(0.22, 1.14, 0.36, 1).",
        "cfg": {"bg": "#eef7f6", "card": "#ffffff", "fg": "#0f172a", "accent": "#00635B", "prompt": "Slide to Reserve · €3.99", "done": "Bag Reserved ✓"},
    },
    "yuka": {
        "motionSlug": "barcode-health-score-scan",
        "motionName": "Barcode Laser Scan → Instant Health Score Pop",
        "engine": "barcode_laser_scan",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Loop", "feel": "Crisp", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 340, "c": 20},
        "props": ["transform: translateY (green laser)", "transform: scale (score badge)", "opacity"],
        "summary": "Scanning a product barcode in Yuka sweeps an emerald laser across vertical bars before popping the iconic '86/100 · Excellent' rating badge.",
        "hint": "Tap barcode viewfinder to score item",
        "choreography": [
            "Continuous: glowing #22c55e laser sweeps smoothly top-to-bottom across barcode stripes.",
            "0-360ms on scan hit: Excellent score pill springs from scale(0.9) to 1.04.",
            "360-420ms: verified score stays sharp and scannable."
        ],
        "agentPrompt": "Recreate Yuka's barcode scanner & instant health rating pop on #f3faf5 with #22c55e glowing scan beam and spring-scaled '86/100 Excellent' pill.",
        "cfg": {"bg": "#f3faf5", "card": "#ffffff", "fg": "#111827", "accent": "#16a34a", "scanTitle": "Excellent", "score": "86 / 100"},
    },
}

out = [build_motion_entry(META[slug], spec) for slug, spec in SPECS.items()]
dest = ROOT / "data" / "packs" / "apps-travel-food.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(out)} motions to {dest.name}")
