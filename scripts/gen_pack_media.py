#!/usr/bin/env python3
"""Generates data/packs/apps-media.json (25 iconic Music, Video, Podcasts & Reading apps)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from app_motion_engines import build_motion_entry

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = {a["slug"]: a for a in json.loads((ROOT / ".cache/harvest_200_apps.json").read_text())["apps-media"]}

SPECS = {
    "apple-music": {
        "motionSlug": "ambient-lyrics-spotlight",
        "motionName": "Blurred Album Glow & Spatial Now-Playing Bar",
        "engine": "cinema_hero_spotlight",
        "use": "Backgrounds", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (album ambient glow)", "width (scrubber progress)", "opacity"],
        "summary": "Apple Music's Now Playing canvas breathes a warm crimson radial bloom behind crisp Spatial Audio metadata as the translucent progress bar glides forward.",
        "hint": "Tap stage to skip +10s & pulse bloom",
        "choreography": [
            "0-140ms: skip tap blooms the #FA243C ambient backdrop glow outward by 18%.",
            "60-520ms: translucent white-and-crimson scrubber glides smoothly forward.",
            "120-560ms: floating +10s indicator expands and fades cleanly."
        ],
        "agentPrompt": "Build Apple Music's ambient Now Playing card on #0d090b with a soft #FA243C radial glow behind Spatial Audio metadata: pulse the ambient backdrop scale(1.18) and advance the 4px scrubber bar over 550ms cubic-bezier(0.22, 1, 0.36, 1) on tap.",
        "cfg": {"bg": "#0d090b", "card": "#1b1015", "accent": "#FA243C", "showTitle": "Midnight City (Spatial)", "showMeta": "Lossless · Dolby Atmos"},
    },
    "youtube": {
        "motionSlug": "double-tap-seek-ripple",
        "motionName": "Ambient Cinema Glow & Double-Tap +10s Ripple",
        "engine": "cinema_hero_spotlight",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 620, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (seek ripple)", "width (red scrubber)", "opacity"],
        "summary": "Tapping YouTube's dark video player pops a translucent +10s seek ripple while advancing the iconic red progress bar under a subtle ambient mode glow.",
        "hint": "Tap player to jump +10s",
        "choreography": [
            "0-200ms: circular +10s badge expands scale(0.5 -> 1.12) over the right side of the frame.",
            "40-540ms: #FF0000 scrubber glides smoothly to the new timestamp.",
            "200-620ms: ripple fades cleanly to 0 while ambient backlight settles."
        ],
        "agentPrompt": "Recreate YouTube's +10s seek ripple & red scrubber on #0f0f0f: animate a circular translucent +10s badge scaling 0.5 -> 1.12 -> 1.4 while fading out over 620ms, synced with a 4px #FF0000 timeline bar.",
        "cfg": {"bg": "#0f0f0f", "card": "#1a1a1d", "accent": "#FF0000", "showTitle": "How Spring Physics Work", "showMeta": "4K 60fps · Ambient Mode"},
    },
    "youtube-music": {
        "motionSlug": "song-video-pill-morph",
        "motionName": "Song ↔ Video Top Segmented Pill Morph",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Crisp", "surface": "dark",
        "dur": 380, "ease": {"t": "spring", "k": 340, "c": 24},
        "props": ["transform: translateX (active pill)", "color", "textContent"],
        "summary": "Switching between Song, Video, and Lyrics in YouTube Music glides a vivid crimson pill across the compact dark header.",
        "hint": "Tap tabs to switch playback mode",
        "choreography": [
            "0-60ms: chosen mode takes crisp white contrast.",
            "60-320ms: #FF0000 thumb slides cleanly across columns.",
            "320-380ms: playback mode badge updates underneath."
        ],
        "agentPrompt": "Build YouTube Music's Song/Video/Lyrics top segmented control on #0c0c0e with #FF0000 active thumb translating over 380ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#0c0c0e", "card": "#19191d", "accent": "#FF0000", "tabs": ["Song", "Video", "Lyrics"], "tabVals": ["Audio · 256k", "1080p MV", "Synced · 128bpm"]},
    },
    "netflix": {
        "motionSlug": "cinema-ribbon-spotlight",
        "motionName": "Cinema Red Backlight & Episode Progress Glide",
        "engine": "cinema_hero_spotlight",
        "use": "Transitions", "stack": "CSS", "trigger": "Click", "feel": "Cinematic", "surface": "dark",
        "dur": 600, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (crimson glow)", "width (red playback bar)", "opacity"],
        "summary": "Netflix's dark hero player washes a moody crimson backlight across the frame while advancing the crisp red continue-watching bar and +10s seek pulse.",
        "hint": "Tap stage to skip ahead +10s",
        "choreography": [
            "0-180ms: #E50914 backlight swells softly across the dark theater viewport.",
            "60-540ms: crimson episode scrubber advances smoothly.",
            "180-600ms: floating +10s ripple expands and dissipates."
        ],
        "agentPrompt": "Build a Netflix theater spotlight preview on #0a0a0c with #E50914 radial glow, crisp white title hierarchy, a +10s ripple burst, and a 4px crimson progress bar.",
        "cfg": {"bg": "#0a0a0c", "card": "#171113", "accent": "#E50914", "showTitle": "S2 · E04 — The Signal", "showMeta": "Ultra HD 4K · Spatial Audio"},
    },
    "disney-plus": {
        "motionSlug": "starry-cobalt-spotlight",
        "motionName": "Cobalt Starlight Arc Glow & Continue Bar",
        "engine": "cinema_hero_spotlight",
        "use": "Backgrounds", "stack": "CSS", "trigger": "Click", "feel": "Cinematic", "surface": "dark",
        "dur": 600, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (sapphire glow)", "width (progress bar)", "opacity"],
        "summary": "Disney+'s deep sapphire theater card blooms a luminous cobalt aurora behind IMAX metadata as the crisp blue playback scrubber glides ahead.",
        "hint": "Tap player to trigger sapphire bloom",
        "choreography": [
            "0-180ms: deep #113CCF sapphire glow swells behind the hero card.",
            "60-540ms: blue progress bar sweeps smoothly rightward.",
            "200-600ms: seek ripple fades cleanly."
        ],
        "agentPrompt": "Create a Disney+ sapphire hero player card on #070c1b with #1d4ed8 radial aura, +10s skip ripple, and 4px animated playback scrubber.",
        "cfg": {"bg": "#070c1b", "card": "#0f1936", "accent": "#2563eb", "showTitle": "Andor · Season 2", "showMeta": "IMAX Enhanced · Dolby Vision"},
    },
    "hbo-max": {
        "motionSlug": "cobalt-beam-spotlight",
        "motionName": "Deep Cobalt Spotlight Beam & Episode Seek",
        "engine": "cinema_hero_spotlight",
        "use": "Backgrounds", "stack": "CSS", "trigger": "Click", "feel": "Cinematic", "surface": "dark",
        "dur": 600, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (cobalt spotlight)", "width (scrubber)", "opacity"],
        "summary": "Max's prestige dark-stage player sweeps an intense electric-blue spotlight across episode artwork paired with a sharp +10s skip pulse.",
        "hint": "Tap screen to pulse spotlight & seek",
        "choreography": [
            "0-180ms: electric #002BE7 beam swells cleanly across the top-right corner.",
            "60-540ms: episode timeline advances seamlessly.",
            "200-600ms: skip badge dissolves without visual clutter."
        ],
        "agentPrompt": "Design a Max prestige streaming spotlight card on #060919 with #002BE7 electric-cobalt backlight, +10s seek pulse, and smooth progress scrub bar.",
        "cfg": {"bg": "#060919", "card": "#0e1538", "accent": "#1d4ed8", "showTitle": "The Last of Us · E01", "showMeta": "4K UHD · HBO Original"},
    },
    "prime-video": {
        "motionSlug": "xray-cyan-spotlight",
        "motionName": "X-Ray Cyan Glow & Instant Seek Scrubber",
        "engine": "cinema_hero_spotlight",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 580, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (cyan glow)", "width (progress bar)", "opacity"],
        "summary": "Prime Video's X-Ray playback canvas pairs crisp cyan ambient bloom with responsive +10s skip feedback and fluid bar progression.",
        "hint": "Tap screen to trigger X-Ray seek",
        "choreography": [
            "0-160ms: #00A8E1 cyan glow expands softly across the frame.",
            "60-520ms: cyan scrubber bar advances cleanly.",
            "180-580ms: +10s ripple blooms and fades."
        ],
        "agentPrompt": "Build a Prime Video X-Ray playback stage on #0b1118 with #00A8E1 cyan radial glow, +10s ripple burst, and 4px scrubber animation.",
        "cfg": {"bg": "#0b1118", "card": "#131e2a", "accent": "#00A8E1", "showTitle": "Fallout · X-Ray Active", "showMeta": "HDR10+ · Cast & Trivia"},
    },
    "soundcloud": {
        "motionSlug": "orange-waveform-scrubber",
        "motionName": "Interactive Orange Waveform Bar Scrubber",
        "engine": "waveform_audio",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Rhythmic", "surface": "dark",
        "dur": 260, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["background-color (SoundCloud orange)", "transform: scaleY (beat peak)", "textContent"],
        "summary": "SoundCloud's iconic dense bar waveform paints played bars bright orange (#FF5500) in real time and responds immediately to click-to-scrub anywhere on the track.",
        "hint": "Tap Play or click waveform to scrub",
        "choreography": [
            "Continuous: playback index illuminates bars sequentially in #FF5500.",
            "Current bar pops vertically scaleY(1.22) in warm amber highlight.",
            "Click scrub: clicking any bar jumps timestamp immediately."
        ],
        "agentPrompt": "Recreate SoundCloud's interactive orange waveform on #121214 with #FF5500 played bars: place a 38px circular orange play button next to 18 variable-height bars with direct click scrubbing and active-bar scaleY(1.22) pulse.",
        "cfg": {"bg": "#121214", "card": "#1c1c20", "accent": "#FF5500", "accent2": "#ff8833", "track": "Midnight Tape (Demo)", "bars": [30, 66, 92, 54, 80, 98, 72, 46, 86, 64, 42, 94, 78, 50, 84, 62, 70, 38]},
    },
    "bandcamp": {
        "motionSlug": "album-stream-spotlight",
        "motionName": "Independent Album Spotlight & Teal Track Bar",
        "engine": "cinema_hero_spotlight",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (teal glow)", "width (track bar)", "opacity"],
        "summary": "Streaming an indie release on Bandcamp pairs calm slate-teal backlight glow with a clean minimalist track scrubber.",
        "hint": "Tap cover stage to advance track",
        "choreography": [
            "0-160ms: #1DA0C3 teal wash pulses softly behind track typography.",
            "60-500ms: progress line slides cleanly to next section.",
            "180-560ms: +10s badge fades smoothly."
        ],
        "agentPrompt": "Create a Bandcamp album player card on #101417 with #1DA0C3 teal glow, crisp editorial track metadata, and an animated 4px scrubber bar.",
        "cfg": {"bg": "#101417", "card": "#182126", "accent": "#1DA0C3", "showTitle": "Analog Tape Vol. 3", "showMeta": "FLAC · Support the artist"},
    },
    "tidal": {
        "motionSlug": "hires-max-spotlight",
        "motionName": "HiRes MAX Gold Glow & Lossless Track Bar",
        "engine": "cinema_hero_spotlight",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (gold glow)", "width (scrubber)", "opacity"],
        "summary": "TIDAL's audiophile player pairs stark jet-black minimalism with a refined champagne-gold MAX ambient bloom and razor-thin track progression.",
        "hint": "Tap stage to skip & pulse MAX glow",
        "choreography": [
            "0-160ms: warm #eab308 MAX glow swells softly behind crisp white typography.",
            "60-500ms: gold progress bar advances smoothly.",
            "180-560ms: subtle +10s ripple dissipates."
        ],
        "agentPrompt": "Build TIDAL's HiRes MAX player stage on #09090b with champagne-gold #eab308 radial glow, stark typography, and 4px animated scrubber.",
        "cfg": {"bg": "#09090b", "card": "#151518", "accent": "#eab308", "showTitle": "MAX · 24-bit / 192 kHz", "showMeta": "FLAC Master · Studio Direct"},
    },
    "pocket-casts": {
        "motionSlug": "trim-silence-skip-dial",
        "motionName": "Playback Speed & Trim-Silence Rotary Dial",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 330, "c": 22},
        "props": ["transform: rotate (speed needle)", "textContent (speed multiplier)"],
        "summary": "Dialing Pocket Casts' playback speed snaps a crisp red indicator cleanly across radial tick marks from 1.0× to 2.2× with spring precision.",
        "hint": "Tap dial to cycle playback speed",
        "choreography": [
            "0-70ms: tap advances playback multiplier to the next speed notch.",
            "40-360ms: #F43E37 glowing needle rotates smoothly around the 128px dial.",
            "360-420ms: center speed readout locks cleanly."
        ],
        "agentPrompt": "Build Pocket Casts' playback speed rotary dial on #121216 with #F43E37 coral-red indicator needle rotating across radial tick marks over 420ms cubic-bezier(0.22, 1.22, 0.36, 1).",
        "cfg": {"bg": "#121216", "card": "#1d1d24", "accent": "#F43E37", "label": "TRIM SPEED", "vals": ["1.0×", "1.3×", "1.6×", "1.9×", "2.2×"]},
    },
    "overcast": {
        "motionSlug": "smart-speed-waveform",
        "motionName": "Smart Speed Voice Waveform & Orange Play",
        "engine": "waveform_audio",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 260, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["background-color (orange bars)", "transform: scaleY (voice boost)"],
        "summary": "Overcast's Smart Speed waveform sweeps warm orange bars across podcast speech while highlighting vocal peaks cleanly.",
        "hint": "Tap Play or scrub podcast bars",
        "choreography": [
            "Continuous: 18 crisp bars illuminate sequentially in #FC7E0F orange.",
            "Active bar pops vertically scaleY(1.22) for Voice Boost feedback.",
            "Click scrub: tap any bar to jump immediately."
        ],
        "agentPrompt": "Create Overcast's Smart Speed podcast player pill on #121214 with #FC7E0F orange accents: combine a 38px circular play button with 18 interactive scrubbing bars.",
        "cfg": {"bg": "#121214", "card": "#1c1c20", "accent": "#FC7E0F", "accent2": "#fbbf24", "track": "Smart Speed · +14m saved", "bars": [28, 52, 74, 44, 88, 66, 95, 58, 40, 82, 92, 54, 36, 70, 86, 48, 62, 34]},
    },
    "audible": {
        "motionSlug": "sleep-timer-dial",
        "motionName": "Audiobook Sleep Timer Rotary Dial",
        "engine": "dial_knob_scrub",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 300, "c": 23},
        "props": ["transform: rotate (amber pointer)", "textContent (minutes)"],
        "summary": "Setting Audible's bedside sleep timer rotates a warm amber needle across soothing dark dial ticks from 10m through End of Chapter.",
        "hint": "Tap dial to set sleep timer",
        "choreography": [
            "0-70ms: tap steps to the next bedtime duration preset.",
            "40-360ms: #F8991D indicator sweeps smoothly across radial ticks.",
            "360-420ms: center timer readout settles cleanly."
        ],
        "agentPrompt": "Build Audible's sleep timer rotary dial on #12100d with #F8991D amber needle rotating smoothly across 13 radial ticks over 420ms cubic-bezier(0.22, 1.22, 0.36, 1).",
        "cfg": {"bg": "#12100d", "card": "#1d1914", "accent": "#F8991D", "label": "SLEEP TIMER", "vals": ["10m", "15m", "30m", "45m", "Ch. End"]},
    },
    "kindle": {
        "motionSlug": "reading-progress-bars",
        "motionName": "Chapter Progress & Sepia Highlight Sweep",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "light",
        "dur": 620, "ease": {"t": "bezier", "p": [0.22, 1.16, 0.36, 1]},
        "props": ["width (reading bars)", "transition-delay (90ms)"],
        "summary": "Kindle's warm paper reading insights cascade chapter completion, daily streak, and highlights bars smoothly with gentle bookish restraint.",
        "hint": "Tap card to animate reading progress",
        "choreography": [
            "0ms: Book progress bar glides smoothly across warm sepia paper.",
            "90-180ms: Chapter and Daily Goal bars follow in 90ms stagger.",
            "480-620ms: tabular percentages settle cleanly."
        ],
        "agentPrompt": "Build Kindle's warm sepia reading progress card on #f8f3e8 with #1A73E8 -> #60a5fa bars cascading over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#f8f3e8", "card": "#fffdf8", "fg": "#292524", "accent": "#1A73E8", "accent2": "#60a5fa", "rows": [("Book", 76), ("Chapter", 92), ("Daily", 84)]},
    },
    "letterboxd": {
        "motionSlug": "five-star-emerald-pop",
        "motionName": "Watched Film Star Burst & Emerald Pill",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 460, "ease": {"t": "spring", "k": 360, "c": 18},
        "props": ["transform: scale + rotate (star)", "transform: translate (emerald sparks)", "color"],
        "summary": "Logging a 5-star review on Letterboxd pops the iconic emerald star with a crisp burst of green sparks over dark charcoal cinema slate.",
        "hint": "Tap star pill to log review",
        "choreography": [
            "0-80ms: star pops 1.3x with playful tilt into #00E054 Letterboxd green.",
            "60-460ms: 6 radial emerald dots burst cleanly outward.",
            "240-400ms: review log count updates in place."
        ],
        "agentPrompt": "Recreate Letterboxd's log/star reaction burst on #14181c with #00E054 emerald highlight: spring-scale the star 1.3x and emit 6 radial dots over 480ms.",
        "cfg": {"bg": "#14181c", "card": "#1f252c", "accent": "#00E054", "author": "Dune: Part Two (2024)", "body": "★★★★★ Watched in 70mm IMAX — monumental sound & motion.", "icon": "★", "count": 4820},
    },
    "goodreads": {
        "motionSlug": "want-to-read-shelf-pop",
        "motionName": "Want-to-Read Shelf Pop & Warm Book Sparks",
        "engine": "reaction_burst_social",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 320, "c": 21},
        "props": ["transform: scale", "transform: translate (sparks)", "background-color"],
        "summary": "Shelving a book as 'Want to Read' on Goodreads pops a warm sage-green badge with delicate celebratory sparks over cream paper.",
        "hint": "Tap shelf pill to add book",
        "choreography": [
            "0-90ms: bookmark icon scales 1.3x into warm library green.",
            "60-460ms: 6 radial particles burst outward and fade.",
            "240-400ms: shelf count increments cleanly."
        ],
        "agentPrompt": "Build a Goodreads Want-to-Read shelf toggle on #f4f1ea with #377458 emerald accent: scale the icon 1.3x over 380ms cubic-bezier(0.22, 1.4, 0.36, 1) with a 6-dot spark burst.",
        "cfg": {"bg": "#f4f1ea", "card": "#ffffff", "fg": "#292524", "accent": "#377458", "author": "The Design of Everyday Things", "body": "Shelved in Want to Read · 4.21 avg rating", "icon": "🔖", "count": 912},
    },
    "plex": {
        "motionSlug": "poster-amber-spotlight",
        "motionName": "Poster Metadata Glass Glow & Amber Progress",
        "engine": "cinema_hero_spotlight",
        "use": "Transitions", "stack": "CSS", "trigger": "Click", "feel": "Cinematic", "surface": "dark",
        "dur": 580, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (amber glow)", "width (watch progress)", "opacity"],
        "summary": "Plex's home theater card glows warm gold behind media metadata while smoothly advancing the signature amber watch-progress bar.",
        "hint": "Tap stage to scrub watch progress",
        "choreography": [
            "0-160ms: #E5A00D Plex gold radial aura swells gently.",
            "60-520ms: amber watch-progress bar advances smoothly.",
            "180-580ms: +10s seek badge blooms and fades."
        ],
        "agentPrompt": "Build a Plex cinema poster player on #121316 with #E5A00D amber glow, +10s seek ripple, and smooth 4px amber progress bar.",
        "cfg": {"bg": "#121316", "card": "#1d1f24", "accent": "#E5A00D", "showTitle": "Blade Runner 2049", "showMeta": "Direct Play · 4K Remux"},
    },
    "vimeo": {
        "motionSlug": "minimal-cyan-player",
        "motionName": "Minimalist Cyan Player Glow & Crisp Seek",
        "engine": "cinema_hero_spotlight",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (cyan glow)", "width (minimal scrubber)", "opacity"],
        "summary": "Vimeo's creator-first player delivers an ultra-clean sky-blue timeline glide and subtle ambient glow built for Staff Picks.",
        "hint": "Tap player to advance Staff Pick",
        "choreography": [
            "0-160ms: #1AB7EA sky backlight pulses subtly behind title.",
            "60-500ms: crisp blue timeline bar advances cleanly.",
            "180-560ms: +10s indicator dissolves effortlessly."
        ],
        "agentPrompt": "Recreate Vimeo's Staff Pick minimal player on #0d1115 with #1AB7EA sky-blue glow, crisp title typography, and 4px scrubber.",
        "cfg": {"bg": "#0d1115", "card": "#151c22", "accent": "#1AB7EA", "showTitle": "Staff Pick · Kinetic Reel", "showMeta": "4K ProRes · 60fps"},
    },
    "crunchyroll": {
        "motionSlug": "anime-queue-spotlight",
        "motionName": "Anime Episode Orange Slash Glow & Queue Seek",
        "engine": "cinema_hero_spotlight",
        "use": "Transitions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (orange glow)", "width (episode bar)", "opacity"],
        "summary": "Crunchyroll's episode player bursts vibrant anime orange across dark slate while snapping the episode progress bar forward.",
        "hint": "Tap stage to skip intro +10s",
        "choreography": [
            "0-160ms: #F47521 energetic orange backlight swells cleanly.",
            "60-500ms: orange progress track glides forward.",
            "180-560ms: +10s skip badge pops and fades."
        ],
        "agentPrompt": "Build Crunchyroll's dark episode player on #0d0d10 with #F47521 orange radial glow, +10s ripple, and 4px animated scrubber.",
        "cfg": {"bg": "#0d0d10", "card": "#1a1614", "accent": "#F47521", "showTitle": "Frieren · Ep. 28", "showMeta": "Simulcast · Sub | Dub"},
    },
    "mubi": {
        "motionSlug": "film-of-day-spotlight",
        "motionName": "Film-of-the-Day Editorial Cobalt Reveal",
        "engine": "cinema_hero_spotlight",
        "use": "Typography", "stack": "CSS", "trigger": "Click", "feel": "Editorial", "surface": "dark",
        "dur": 600, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (editorial blue glow)", "width (film bar)", "opacity"],
        "summary": "MUBI's arthouse player wraps curated cinema metadata in deep royal cobalt light with unhurried, gallery-grade pacing.",
        "hint": "Tap frame to advance reel",
        "choreography": [
            "0-180ms: deep #001489/#2563eb gallery glow swells gently.",
            "80-540ms: minimal timeline bar advances evenly.",
            "200-600ms: seek indicator fades softly."
        ],
        "agentPrompt": "Build MUBI's editorial arthouse film player on #080a14 with deep cobalt radial glow, crisp typography, and minimalist scrubber.",
        "cfg": {"bg": "#080a14", "card": "#10162b", "accent": "#2563eb", "showTitle": "In the Mood for Love", "showMeta": "Wong Kar-wai · 4K Restoration"},
    },
    "deezer": {
        "motionSlug": "flow-mood-spotlight",
        "motionName": "Flow Purple Pulse & Beat Scrubber",
        "engine": "cinema_hero_spotlight",
        "use": "Backgrounds", "stack": "CSS", "trigger": "Click", "feel": "Rhythmic", "surface": "dark",
        "dur": 560, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: scale (purple aura)", "width (track bar)", "opacity"],
        "summary": "Deezer's Flow player pulses an electric purple radial aura behind track info while advancing the mix timeline smoothly.",
        "hint": "Tap Flow stage to skip ahead",
        "choreography": [
            "0-160ms: #A238FF vivid purple glow swells behind the active mix.",
            "60-500ms: purple progress bar glides across the track.",
            "180-560ms: +10s ripple expands and disappears."
        ],
        "agentPrompt": "Create Deezer's Flow player card on #0f0c14 with #A238FF electric purple ambient glow and animated 4px scrubber.",
        "cfg": {"bg": "#0f0c14", "card": "#1c1528", "accent": "#A238FF", "showTitle": "Flow · Chill Focus", "showMeta": "HiFi Mix · Infinite Queue"},
    },
    "apple-podcasts": {
        "motionSlug": "chapter-bars-progress",
        "motionName": "Episode Chapter Progress Bars Cascade",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "dark",
        "dur": 620, "ease": {"t": "bezier", "p": [0.22, 1.16, 0.36, 1]},
        "props": ["width (chapter bars)", "transition-delay (90ms)"],
        "summary": "Apple Podcasts' chapter summary cascades purple progress bars across Intro, Deep Dive, and Q&A segments with crisp 90ms stagger.",
        "hint": "Tap card to animate chapter progress",
        "choreography": [
            "0ms: first chapter bar expands in #9933CC -> #c084fc gradient.",
            "90-180ms: subsequent chapters stagger cleanly into full width.",
            "480-620ms: tabular completion percentages settle."
        ],
        "agentPrompt": "Build Apple Podcasts' chapter progress card on #140f1a with #9933CC -> #c084fc bars animating width over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#140f1a", "card": "#1e1726", "accent": "#9933CC", "accent2": "#c084fc", "rows": [("Intro", 100), ("Interview", 74), ("Q&A", 38)]},
    },
    "castro": {
        "motionSlug": "inbox-triage-swipe-deck",
        "motionName": "Podcast Inbox Queue / Archive Swipe Deck",
        "engine": "card_swipe_deck",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "dark",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 21},
        "props": ["transform: translate + rotate", "opacity (QUEUE/ARCHIVE stamp)", "transform: scale"],
        "summary": "Triaging new episodes in Castro flings cards right to Queue or left to Archive with crisp emerald feedback while lifting the next episode forward.",
        "hint": "Tap Queue / Archive or card to triage",
        "choreography": [
            "0-70ms: QUEUE or ARCHIVE stamp appears cleanly on the episode card.",
            "40-360ms: active episode exits ±86px at ±14° tilt.",
            "360-420ms: next inbox episode scales cleanly into foreground."
        ],
        "agentPrompt": "Recreate Castro's podcast triage deck on #0e1412 with #00B265 emerald cards: swipe cards ±86px with ±14deg rotation and QUEUE/ARCHIVE stamps over 420ms cubic-bezier(0.22, 1.2, 0.36, 1).",
        "cfg": {"bg": "#0e1412", "card": "#17221f", "accent": "#00B265", "accent2": "#059669", "stampR": "QUEUE", "stampL": "ARCHIVE", "cards": [("Design Details #492", "54 min · New today"), ("Syntax FM · Springs", "41 min · Tech"), ("Acquired · Apple", "2h 18m · Deep Dive")]},
    },
    "libby": {
        "motionSlug": "library-hold-progress-bars",
        "motionName": "Library Hold Shelf & Reading Progress Bars",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Calm", "surface": "light",
        "dur": 620, "ease": {"t": "bezier", "p": [0.22, 1.16, 0.36, 1]},
        "props": ["width (shelf progress)", "transition-delay (90ms)"],
        "summary": "Libby's warm library shelf cascades plum-magenta progress bars across Loans, Holds, and Reading Goal with friendly staggered rhythm.",
        "hint": "Tap shelf to animate loan progress",
        "choreography": [
            "0ms: Current Loan bar glides smoothly across warm cream.",
            "90-180ms: Hold Queue and Audiobook bars stagger cleanly.",
            "480-620ms: percentages lock crisply."
        ],
        "agentPrompt": "Build Libby's library loan progress card on #fbf6f8 with #A61C4D -> #ec4899 bars animating width over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#fbf6f8", "card": "#ffffff", "fg": "#1f1720", "accent": "#A61C4D", "accent2": "#ec4899", "rows": [("Loan", 88), ("Hold #2", 62), ("Audio", 46)]},
    },
    "storytel": {
        "motionSlug": "audiobook-narration-bars",
        "motionName": "Audiobook Chapter & Bookmark Cascade",
        "engine": "metric_bars_cascade",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Fluid", "surface": "light",
        "dur": 620, "ease": {"t": "bezier", "p": [0.22, 1.16, 0.36, 1]},
        "props": ["width (orange chapter fills)", "transition-delay"],
        "summary": "Storytel's reading tracker sweeps warm vermilion progress bars across Chapters, Bookmarks, and Weekly Listening targets.",
        "hint": "Tap card to animate listening progress",
        "choreography": [
            "0ms: primary chapter bar glides in #FF5A2C warm orange.",
            "90-180ms: secondary progress bars cascade with crisp spring ease.",
            "480-620ms: settled bars display clean completion readouts."
        ],
        "agentPrompt": "Create Storytel's listening progress card on #fff7f4 with #FF5A2C -> #fb923c bars expanding over 620ms cubic-bezier(0.22, 1.16, 0.36, 1) with 90ms stagger.",
        "cfg": {"bg": "#fff7f4", "card": "#ffffff", "fg": "#1c1917", "accent": "#FF5A2C", "accent2": "#fb923c", "rows": [("Chapter", 90), ("Weekly", 72), ("Series", 54)]},
    },
}

out = [build_motion_entry(META[slug], spec) for slug, spec in SPECS.items()]
dest = ROOT / "data" / "packs" / "apps-media.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(out)} motions to {dest.name}")
