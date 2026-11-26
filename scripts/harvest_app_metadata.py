#!/usr/bin/env python3
"""
Concurrent iTunes App Store metadata harvester for 200 target apps.
Writes verified App Store icons, bundle IDs, store URLs, and categories to .cache/harvest_200_apps.json.
"""
import concurrent.futures
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / ".cache" / "harvest_200_apps.json"

TARGET_APPS = {
    "apps-finance": [
        ("cash-app", "Cash App", "Cash App", "#00D632", "Finance"),
        ("venmo", "Venmo", "Venmo", "#008CFF", "Finance"),
        ("robinhood", "Robinhood", "Robinhood: Investing for All", "#00C805", "Finance"),
        ("coinbase", "Coinbase", "Coinbase: Buy Bitcoin & Ether", "#0052FF", "Finance"),
        ("paypal", "PayPal", "PayPal: Pay, Send, Save", "#003087", "Finance"),
        ("monzo", "Monzo", "Monzo Mobile Banking", "#FF4F40", "Finance"),
        ("n26", "N26", "N26 — The Mobile Bank", "#36A18B", "Finance"),
        ("nubank", "Nubank", "Nubank", "#820AD1", "Finance"),
        ("klarna", "Klarna", "Klarna | Shop now. Pay later.", "#FFB3C7", "Shopping"),
        ("ramp", "Ramp", "Ramp: Business Banking", "#E4F222", "Finance"),
        ("mercury", "Mercury", "Mercury Business Banking", "#5E6AD2", "Finance"),
        ("brex", "Brex", "Brex", "#F46A25", "Finance"),
        ("wealthfront", "Wealthfront", "Wealthfront: Save and Invest", "#4840BB", "Finance"),
        ("betterment", "Betterment", "Betterment Investing & Saving", "#1D6AE5", "Finance"),
        ("chime", "Chime", "Chime - Mobile Banking", "#1EC677", "Finance"),
        ("sofi", "SoFi", "SoFi: Banking & Investing", "#00A2C7", "Finance"),
        ("splitwise", "Splitwise", "Splitwise", "#1CC29F", "Finance"),
        ("copilot-money", "Copilot Money", "Copilot: Track & Budget Money", "#4F6BFF", "Finance"),
        ("monarch-money", "Monarch Money", "Monarch: Budget & Track Money", "#FF6B35", "Finance"),
        ("phantom", "Phantom", "Phantom Crypto Wallet", "#AB9FF2", "Finance"),
        ("metamask", "MetaMask", "MetaMask - Blockchain Wallet", "#F6851B", "Finance"),
        ("rainbow-wallet", "Rainbow", "Rainbow: Ethereum Wallet", "#001E59", "Finance"),
        ("ynab", "YNAB", "YNAB", "#3B5EDA", "Finance"),
        ("acorns", "Acorns", "Acorns: Invest Spare Change", "#74C947", "Finance"),
        ("trading-212", "Trading 212", "Trading 212", "#00A7E1", "Finance"),
    ],
    "apps-social": [
        ("whatsapp", "WhatsApp", "WhatsApp Messenger", "#25D366", "Social Networking"),
        ("snapchat", "Snapchat", "Snapchat", "#FFFC00", "Photo & Video"),
        ("x-twitter", "X", "X", "#101114", "News"),
        ("bluesky", "Bluesky", "Bluesky Social", "#1185FE", "Social Networking"),
        ("mastodon", "Mastodon", "Mastodon for iPhone and iPad", "#6364FF", "Social Networking"),
        ("signal", "Signal", "Signal - Private Messenger", "#3A76F0", "Social Networking"),
        ("messenger", "Messenger", "Messenger", "#0084FF", "Social Networking"),
        ("linkedin", "LinkedIn", "LinkedIn: Network & Job Finder", "#0A66C2", "Business"),
        ("substack", "Substack", "Substack", "#FF6719", "News"),
        ("bereal", "BeReal", "BeReal. Your friends for real.", "#101114", "Social Networking"),
        ("locket", "Locket Widget", "Locket Widget", "#FFB800", "Social Networking"),
        ("partiful", "Partiful", "Partiful: Fun Party Invites", "#8B5CF6", "Social Networking"),
        ("retro-photo", "Retro", "Retro - Photo Journal", "#FF5C35", "Photo & Video"),
        ("vsco", "VSCO", "VSCO: Photo & Video Editor", "#1A1A1A", "Photo & Video"),
        ("tumblr", "Tumblr", "Tumblr - Social Fandom Art", "#001935", "Social Networking"),
        ("wechat", "WeChat", "WeChat", "#07C160", "Social Networking"),
        ("line", "LINE", "LINE", "#06C755", "Social Networking"),
        ("viber", "Viber", "Rakuten Viber Messenger", "#7360F2", "Social Networking"),
        ("clubhouse", "Clubhouse", "Clubhouse", "#F2EFE4", "Social Networking"),
        ("hinge", "Hinge", "Hinge Dating App: Meet People", "#1A1A1A", "Lifestyle"),
        ("bumble", "Bumble", "Bumble Dating App: Meet & Date", "#FFC629", "Lifestyle"),
        ("tinder", "Tinder", "Tinder: Chat, Dating & Friends", "#FE3C72", "Lifestyle"),
        ("nextdoor", "Nextdoor", "Nextdoor: Neighborhood Network", "#8ED500", "Social Networking"),
        ("meetup", "Meetup", "Meetup: Social Events & Groups", "#F64060", "Social Networking"),
        ("twitch", "Twitch", "Twitch: Live Streaming", "#9146FF", "Entertainment"),
    ],
    "apps-productivity": [
        ("obsidian", "Obsidian", "Obsidian - Connected Notes", "#7C3AED", "Productivity"),
        ("craft", "Craft", "Craft - Docs and Notes Editor", "#2563EB", "Productivity"),
        ("things-3", "Things 3", "Things 3", "#2F7CF6", "Productivity"),
        ("ticktick", "TickTick", "TickTick: To-Do List & Calendar", "#4772FA", "Productivity"),
        ("bear", "Bear", "Bear Markdown Notes", "#D94343", "Productivity"),
        ("fantastical", "Fantastical", "Fantastical Calendar", "#EF4444", "Productivity"),
        ("notion-calendar", "Notion Calendar", "Notion Calendar", "#101114", "Productivity"),
        ("superhuman", "Superhuman", "Superhuman Mail", "#4F46E5", "Productivity"),
        ("spark-mail", "Spark Mail", "Spark Mail - Email by Readdle", "#3B82F6", "Productivity"),
        ("microsoft-teams", "Microsoft Teams", "Microsoft Teams", "#5B5FC7", "Business"),
        ("zoom", "Zoom", "Zoom Workplace", "#0B5CFF", "Business"),
        ("loom", "Loom", "Loom: Screen Recorder", "#625DF5", "Productivity"),
        ("miro", "Miro", "Miro: Collaborative Whiteboard", "#FFD02F", "Productivity"),
        ("figma", "Figma", "Figma", "#A259FF", "Productivity"),
        ("trello", "Trello", "Trello: Organize anything!", "#0079BF", "Productivity"),
        ("asana", "Asana", "Asana: Work in one place", "#F06A6A", "Business"),
        ("clickup", "ClickUp", "ClickUp - Manage Teams & Tasks", "#7B68EE", "Productivity"),
        ("jira", "Jira", "Jira Cloud by Atlassian", "#0052CC", "Business"),
        ("calendly", "Calendly", "Calendly Mobile", "#006BFF", "Productivity"),
        ("dropbox", "Dropbox", "Dropbox: Cloud Storage & Drive", "#0061FF", "Productivity"),
        ("google-drive", "Google Drive", "Google Drive", "#4285F4", "Productivity"),
        ("gmail", "Gmail", "Gmail - Email by Google", "#EA4335", "Productivity"),
        ("outlook", "Microsoft Outlook", "Microsoft Outlook", "#0078D4", "Productivity"),
        ("evernote", "Evernote", "Evernote - Notes Organizer", "#00A82D", "Productivity"),
        ("goodnotes", "Goodnotes", "Goodnotes 6", "#2B9CF6", "Productivity"),
    ],
    "apps-media": [
        ("apple-music", "Apple Music", "Apple Music", "#FA243C", "Music"),
        ("youtube", "YouTube", "YouTube", "#FF0000", "Photo & Video"),
        ("youtube-music", "YouTube Music", "YouTube Music", "#FF0000", "Music"),
        ("netflix", "Netflix", "Netflix", "#E50914", "Entertainment"),
        ("disney-plus", "Disney+", "Disney+", "#113CCF", "Entertainment"),
        ("hbo-max", "Max", "Max: Stream HBO, TV, & Movies", "#002BE7", "Entertainment"),
        ("prime-video", "Prime Video", "Amazon Prime Video", "#00A8E1", "Entertainment"),
        ("soundcloud", "SoundCloud", "SoundCloud: Discover New Music", "#FF5500", "Music"),
        ("bandcamp", "Bandcamp", "Bandcamp", "#1DA0C3", "Music"),
        ("tidal", "TIDAL", "TIDAL Music: HiRes Sound", "#101114", "Music"),
        ("pocket-casts", "Pocket Casts", "Pocket Casts", "#F43E37", "Entertainment"),
        ("overcast", "Overcast", "Overcast", "#FC7E0F", "News"),
        ("audible", "Audible", "Audible: Audio Entertainment", "#F8991D", "Books"),
        ("kindle", "Kindle", "Amazon Kindle", "#1A73E8", "Books"),
        ("letterboxd", "Letterboxd", "Letterboxd", "#00E054", "Entertainment"),
        ("goodreads", "Goodreads", "Goodreads: Book Reviews", "#553B08", "Books"),
        ("plex", "Plex", "Plex: Watch Live TV and Movies", "#E5A00D", "Entertainment"),
        ("vimeo", "Vimeo", "Vimeo", "#1AB7EA", "Photo & Video"),
        ("crunchyroll", "Crunchyroll", "Crunchyroll", "#F47521", "Entertainment"),
        ("mubi", "MUBI", "MUBI", "#001489", "Entertainment"),
        ("deezer", "Deezer", "Deezer: Music & Podcast Player", "#A238FF", "Music"),
        ("apple-podcasts", "Apple Podcasts", "Apple Podcasts", "#9933CC", "Entertainment"),
        ("castro", "Castro", "Castro Podcast Player", "#00B265", "Entertainment"),
        ("libby", "Libby", "Libby, the library app", "#A61C4D", "Books"),
        ("storytel", "Storytel", "Storytel: Audiobooks & Ebooks", "#FF5A2C", "Books"),
    ],
    "apps-travel-food": [
        ("uber", "Uber", "Uber - Request a ride", "#101114", "Travel"),
        ("lyft", "Lyft", "Lyft", "#FF00BF", "Travel"),
        ("google-maps", "Google Maps", "Google Maps", "#4285F4", "Navigation"),
        ("waze", "Waze", "Waze Navigation & Live Traffic", "#33CCFF", "Navigation"),
        ("citymapper", "Citymapper", "Citymapper: All Your Transit", "#2DC937", "Navigation"),
        ("booking-com", "Booking.com", "Booking.com: Hotels & Travel", "#003580", "Travel"),
        ("expedia", "Expedia", "Expedia: Hotels, Flights & Car", "#FFCB00", "Travel"),
        ("hopper", "Hopper", "Hopper: Hotels, Flights & Cars", "#FA6866", "Travel"),
        ("tripit", "TripIt", "TripIt: Travel Planner", "#0066CC", "Travel"),
        ("delta", "Delta Air Lines", "Fly Delta", "#C8102E", "Travel"),
        ("united", "United Airlines", "United Airlines", "#005DAA", "Travel"),
        ("alltrails", "AllTrails", "AllTrails: Hike, Bike & Run", "#2C5601", "Health & Fitness"),
        ("komoot", "Komoot", "komoot - hike, bike & run", "#6AA127", "Health & Fitness"),
        ("lime", "Lime", "Lime - #RideGreen", "#00DD00", "Travel"),
        ("bolt", "Bolt", "Bolt: Request a Ride", "#34D186", "Travel"),
        ("doordash", "DoorDash", "DoorDash - Food Delivery", "#FF3008", "Food & Drink"),
        ("uber-eats", "Uber Eats", "Uber Eats: Food Delivery", "#06C167", "Food & Drink"),
        ("deliveroo", "Deliveroo", "Deliveroo: Food & Shopping", "#00CCBC", "Food & Drink"),
        ("instacart", "Instacart", "Instacart: Same-day delivery", "#43B02A", "Food & Drink"),
        ("opentable", "OpenTable", "OpenTable", "#DA3743", "Food & Drink"),
        ("resy", "Resy", "Resy", "#D3452A", "Food & Drink"),
        ("beli", "Beli", "Beli: Restaurant List & Guide", "#0B5D69", "Food & Drink"),
        ("starbucks", "Starbucks", "Starbucks", "#00704A", "Food & Drink"),
        ("too-good-to-go", "Too Good To Go", "Too Good To Go: End Food Waste", "#00635B", "Food & Drink"),
        ("yuka", "Yuka", "Yuka - Food & Cosmetic Scanner", "#50C878", "Health & Fitness"),
    ],
    "apps-health-lifestyle": [
        ("oura", "Oura", "Oura", "#2D3142", "Health & Fitness"),
        ("whoop", "WHOOP", "WHOOP", "#101114", "Health & Fitness"),
        ("nike-run-club", "Nike Run Club", "Nike Run Club: Running Coach", "#CCFF00", "Health & Fitness"),
        ("peloton", "Peloton", "Peloton: Fitness & Workouts", "#DF1C2F", "Health & Fitness"),
        ("myfitnesspal", "MyFitnessPal", "MyFitnessPal: Calorie Counter", "#0066EE", "Health & Fitness"),
        ("macrofactor", "MacroFactor", "MacroFactor - Macro Tracker", "#1F2937", "Health & Fitness"),
        ("gentler-streak", "Gentler Streak", "Gentler Streak Workout Tracker", "#78C850", "Health & Fitness"),
        ("hevy", "Hevy", "Hevy - Gym Log Workout Tracker", "#1E88E5", "Health & Fitness"),
        ("strong", "Strong", "Strong Workout Tracker Gym Log", "#38BDF8", "Health & Fitness"),
        ("ladder", "Ladder", "Ladder: Strength Training", "#CCFF00", "Health & Fitness"),
        ("fitbit", "Fitbit", "Fitbit: Health & Fitness", "#00B0B9", "Health & Fitness"),
        ("garmin-connect", "Garmin Connect", "Garmin Connect", "#007CC3", "Health & Fitness"),
        ("flo", "Flo", "Flo Period & Cycle Tracker", "#FF5C8D", "Health & Fitness"),
        ("clue", "Clue", "Clue Period & Cycle Tracker", "#FF5252", "Health & Fitness"),
        ("sleep-cycle", "Sleep Cycle", "Sleep Cycle: Sleep Tracker", "#F59E0B", "Health & Fitness"),
        ("endel", "Endel", "Endel: Focus, Sleep, Relax", "#101114", "Health & Fitness"),
        ("waking-up", "Waking Up", "Waking Up: Beyond Meditation", "#E06D3B", "Health & Fitness"),
        ("finch", "Finch", "Finch: Self-Care Pet", "#62C370", "Health & Fitness"),
        ("waterllama", "Waterllama", "Water Tracker Waterllama", "#38BDF8", "Health & Fitness"),
        ("streaks", "Streaks", "Streaks", "#FF6B35", "Health & Fitness"),
        ("lifesum", "Lifesum", "Lifesum: Healthy Eating", "#4ADE80", "Health & Fitness"),
        ("noom", "Noom", "Noom: Healthy Weight Loss", "#F25C54", "Health & Fitness"),
        ("runna", "Runna", "Runna: Running Training Plans", "#FF3B5C", "Health & Fitness"),
        ("eight-sleep", "Eight Sleep", "Eight Sleep", "#3B82F6", "Health & Fitness"),
        ("cronometer", "Cronometer", "Calorie Counter by Cronometer", "#FF702A", "Health & Fitness"),
    ],
    "apps-shopping-creative": [
        ("shop-app", "Shop", "Shop: All your favorite brands", "#5A31F4", "Shopping"),
        ("amazon", "Amazon", "Amazon Shopping", "#FF9900", "Shopping"),
        ("ebay", "eBay", "eBay: Marketplace & Deals", "#E53238", "Shopping"),
        ("depop", "Depop", "Depop - Buy & Sell Clothes", "#FF2300", "Shopping"),
        ("vinted", "Vinted", "Vinted - Sell vintage clothes", "#09B1BA", "Shopping"),
        ("stockx", "StockX", "StockX: Sneakers & Streetwear", "#006340", "Shopping"),
        ("goat", "GOAT", "GOAT – Sneakers & Apparel", "#101114", "Shopping"),
        ("nike", "Nike", "Nike: Shoes, Apparel & Stories", "#101114", "Shopping"),
        ("zara", "ZARA", "ZARA", "#101114", "Shopping"),
        ("ikea", "IKEA", "IKEA", "#0058A3", "Shopping"),
        ("etsy", "Etsy", "Etsy: Custom & Creative Goods", "#F1641E", "Shopping"),
        ("asos", "ASOS", "ASOS", "#101114", "Shopping"),
        ("sephora", "Sephora", "Sephora: Cosmetics & Beauty", "#101114", "Shopping"),
        ("capcut", "CapCut", "CapCut - Video Editor", "#101114", "Photo & Video"),
        ("lightroom", "Adobe Lightroom", "Lightroom Photo & Video Editor", "#31A8FF", "Photo & Video"),
        ("snapseed", "Snapseed", "Snapseed", "#34A853", "Photo & Video"),
        ("halide", "Halide", "Halide Mark II - Pro Camera", "#FACC15", "Photo & Video"),
        ("kino", "Kino", "Kino - Pro Video Camera", "#FF4D2D", "Photo & Video"),
        ("darkroom", "Darkroom", "Darkroom: Photo & Video Editor", "#8B5CF6", "Photo & Video"),
        ("procreate-pocket", "Procreate Pocket", "Procreate Pocket", "#E11D48", "Graphics & Design"),
        ("canva", "Canva", "Canva: Design, Art & AI Editor", "#00C4CC", "Graphics & Design"),
        ("unfold", "Unfold", "Unfold: Story & Collage Maker", "#18181B", "Photo & Video"),
        ("dazz-cam", "Dazz Cam", "Dazz Cam - Vintage Camera", "#F59E0B", "Photo & Video"),
        ("lapse", "Lapse", "Lapse - Disposable Camera", "#F97316", "Photo & Video"),
        ("photomator", "Photomator", "Photomator – Photo Editor", "#EC4899", "Photo & Video"),
    ],
    "apps-ai-dev-utilities": [
        ("chatgpt", "ChatGPT", "ChatGPT", "#10A37F", "Productivity"),
        ("claude", "Claude", "Claude by Anthropic", "#D97757", "Productivity"),
        ("perplexity", "Perplexity", "Perplexity: Ask Anything", "#20B2AA", "Productivity"),
        ("grok", "Grok", "Grok", "#101114", "Productivity"),
        ("gemini", "Google Gemini", "Google Gemini", "#4285F4", "Productivity"),
        ("poe", "Poe", "Poe - Fast AI Chat", "#5D5CDE", "Productivity"),
        ("elevenlabs", "ElevenLabs", "ElevenLabs Reader: AI Audio", "#101114", "Books"),
        ("otter-ai", "Otter", "Otter: Transcribe Voice Notes", "#1E66F5", "Productivity"),
        ("suno", "Suno", "Suno - AI Songs & Music", "#FF4D4D", "Music"),
        ("arc-search", "Arc Search", "Arc Search – Find it, Faster", "#4F46E5", "Utilities"),
        ("github", "GitHub", "GitHub", "#24292F", "Developer Tools"),
        ("1password", "1Password", "1Password 8 - Password Manager", "#0572EC", "Productivity"),
        ("bitwarden", "Bitwarden", "Bitwarden Password Manager", "#175DDC", "Utilities"),
        ("tailscale", "Tailscale", "Tailscale", "#242424", "Utilities"),
        ("philips-hue", "Philips Hue", "Philips Hue", "#8B5CF6", "Lifestyle"),
        ("sonos", "Sonos", "Sonos", "#101114", "Music"),
        ("tesla", "Tesla", "Tesla", "#E82127", "Lifestyle"),
        ("rivian", "Rivian", "Rivian", "#F59E0B", "Lifestyle"),
        ("carrot-weather", "CARROT Weather", "CARROT Weather: Alerts & Radar", "#38BDF8", "Weather"),
        ("flightradar24", "Flightradar24", "Flightradar24 Flight Tracker", "#FACC15", "Travel"),
        ("speedtest", "Speedtest", "Speedtest by Ookla", "#141526", "Utilities"),
        ("nyt", "The New York Times", "The New York Times", "#101114", "News"),
        ("readwise-reader", "Readwise Reader", "Readwise Reader", "#F59E0B", "Productivity"),
        ("brilliant", "Brilliant", "Brilliant: Learn interactively", "#101114", "Education"),
        ("khan-academy", "Khan Academy", "Khan Academy", "#14BF96", "Education"),
    ],
}


def lookup_one(pack_name: str, entry: tuple[str, str, str, str, str]) -> dict:
    slug, name, query, accent, fallback_cat = entry
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode({
        "term": query,
        "entity": "software",
        "limit": 3,
        "country": "us",
    })
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"},
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])
            chosen = results[0] if results else None
            # Prefer exact/prefix match on trackName
            if results:
                nl = name.lower()
                for r in results:
                    tn = (r.get("trackName") or "").lower()
                    if tn == nl or tn.startswith(nl + ":") or tn.startswith(nl + " ") or tn.startswith(nl + "–") or tn.startswith(nl + "-"):
                        chosen = r
                        break
            if chosen:
                icon = chosen.get("artworkUrl100") or chosen.get("artworkUrl512") or ""
                return {
                    "pack": pack_name,
                    "slug": slug,
                    "name": name,
                    "category": chosen.get("primaryGenreName") or fallback_cat,
                    "platform": ["iOS", "Android"],
                    "accent": accent,
                    "iconUrl": icon,
                    "storeUrl": chosen.get("trackViewUrl") or "",
                    "bundleId": chosen.get("bundleId") or "",
                    "seller": chosen.get("sellerName") or "",
                    "ok": True,
                }
            break
        except Exception as exc:
            if attempt < 2:
                time.sleep(0.6 * (attempt + 1))
            else:
                return {
                    "pack": pack_name,
                    "slug": slug,
                    "name": name,
                    "category": fallback_cat,
                    "platform": ["iOS", "Android"],
                    "accent": accent,
                    "iconUrl": "",
                    "storeUrl": "",
                    "bundleId": "",
                    "seller": "",
                    "ok": False,
                    "error": str(exc),
                }
    return {
        "pack": pack_name,
        "slug": slug,
        "name": name,
        "category": fallback_cat,
        "platform": ["iOS", "Android"],
        "accent": accent,
        "iconUrl": "",
        "storeUrl": "",
        "bundleId": "",
        "seller": "",
        "ok": False,
    }


def main() -> int:
    jobs = [(pack, entry) for pack, entries in TARGET_APPS.items() for entry in entries]
    print(f"Harvesting App Store metadata for {len(jobs)} apps...")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(lookup_one, pack, entry) for pack, entry in jobs]
        for fut in concurrent.futures.as_completed(futs):
            results.append(fut.result())

    by_pack: dict[str, list[dict]] = {p: [] for p in TARGET_APPS}
    order = {entry[0]: idx for entries in TARGET_APPS.values() for idx, entry in enumerate(entries)}
    for r in results:
        by_pack[r["pack"]].append(r)
    for p in by_pack:
        by_pack[p].sort(key=lambda r: order[r["slug"]])

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(by_pack, indent=2, ensure_ascii=False), encoding="utf-8")
    ok_count = sum(1 for r in results if r.get("ok") and r.get("iconUrl"))
    missing = [r["name"] for r in results if not (r.get("ok") and r.get("iconUrl"))]
    print(f"Saved {len(results)} apps to {OUT_PATH} ({ok_count} with verified App Store icon + storeUrl).")
    if missing:
        print("Missing/fallback:", missing)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
