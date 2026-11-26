#!/usr/bin/env python3
"""Generates data/packs/apps-productivity.json (25 iconic Productivity & Work apps)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from app_motion_engines import build_motion_entry

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = {a["slug"]: a for a in json.loads((ROOT / ".cache/harvest_200_apps.json").read_text())["apps-productivity"]}

SPECS = {
    "obsidian": {
        "motionSlug": "knowledge-graph-focus",
        "motionName": "Knowledge Graph Node Glow & Edge Focus",
        "engine": "graph_cursor_canvas",
        "use": "Generative", "stack": "SVG", "trigger": "Click", "feel": "Organic", "surface": "dark",
        "dur": 820, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["fill + filter: drop-shadow (active nodes)", "transform: translate (focus labels)"],
        "summary": "Navigating Obsidian's local graph view illuminates connected vault notes in luminous violet while focus tags glide smoothly across linked clusters.",
        "hint": "Tap graph canvas to cycle linked notes",
        "choreography": [
            "0-160ms: target note node and its linked neighbor illuminate with #7C3AED drop-shadow glow.",
            "80-760ms: floating note badges glide smoothly along spring paths across the dotted canvas.",
            "760-820ms: active cluster settles with subtle graph edge contrast."
        ],
        "agentPrompt": "Build an Obsidian interactive SVG knowledge graph on #111116 with #7C3AED violet nodes: render 5 connected circular nodes over a subtle dot grid; on click, illuminate active nodes with drop-shadow glow and smoothly translate floating note badges over 820ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#111116", "card": "#191922", "accent": "#7C3AED", "accent2": "#a855f7", "tag1": "MOC.md", "tag2": "Physics.md"},
    },
    "craft": {
        "motionSlug": "doc-card-stack-peel",
        "motionName": "Document Card Stack Peel & Spring Promote",
        "engine": "card_swipe_deck",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Silky", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 300, "c": 23},
        "props": ["transform: translate + rotate", "transform: scale", "opacity"],
        "summary": "Flipping through Craft's visual document cards peels the foreground page cleanly aside with a gentle rotation while promoting the next doc card from the stack.",
        "hint": "Tap card or arrows to cycle documents",
        "choreography": [
            "0-70ms: action stamp highlights the chosen page gesture.",
            "40-360ms: top doc card glides aside with 14° editorial tilt.",
            "360-420ms: next doc card rises from scale(0.92) -> 1.0."
        ],
        "agentPrompt": "Create Craft's stacked document card peel on #f5f7fb with #2563EB -> #38bdf8 cards: translate the top card off-stack with ±14deg rotation over 420ms cubic-bezier(0.22, 1.2, 0.36, 1) while scaling the next card up from 0.92.",
        "cfg": {"bg": "#f4f7fb", "card": "#ffffff", "fg": "#0f172a", "accent": "#2563EB", "accent2": "#0ea5e9", "stampR": "PINNED", "stampL": "NEXT", "cards": [("Q4 Product Brief", "12 blocks · Updated 4m ago"), ("Design Critique", "8 visual cards · Team"), ("Release Notes", "Ready to publish")]},
    },
    "things-3": {
        "motionSlug": "task-complete-swipe-undo",
        "motionName": "Tactile Checkbox Swipe & Undo Toast Rise",
        "engine": "list_swipe_action",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 23},
        "props": ["transform: translateX (row slide)", "background-color (checkbox fill)", "transform: translateY (toast)"],
        "summary": "Completing or scheduling a Things 3 to-do slides the crisp white task row smoothly over a cobalt action reveal while floating a subtle Undo toast underneath.",
        "hint": "Tap task row to complete & reveal Undo",
        "choreography": [
            "0-100ms: circular #2F7CF6 checkbox fills cleanly on tap.",
            "40-360ms: task card glides +92px rightward exposing the blue action backing.",
            "160-420ms: floating Undo pill rises 10px into view with zero jitter."
        ],
        "agentPrompt": "Build Things 3's tactile task row completion on #f4f6f9 with #2F7CF6 accent: slide the white task row +92px rightward over 420ms cubic-bezier(0.22, 1.14, 0.36, 1) to reveal the action layer while raising a crisp Undo snackbar.",
        "cfg": {"bg": "#f3f5f8", "card": "#ffffff", "fg": "#111827", "accent": "#2F7CF6", "rowTitle": "Finalize spring tokens", "rowSub": "Today · Design System", "actionLbl": "Complete"},
    },
    "ticktick": {
        "motionSlug": "pomodoro-focus-ring",
        "motionName": "Pomodoro Focus Ring Countdown Sweep",
        "engine": "ring_gauge",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Calm", "surface": "dark",
        "dur": 720, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["stroke-dashoffset (focus ring)", "filter: drop-shadow", "textContent"],
        "summary": "TickTick's Pomodoro timer sweeps dual cobalt and sky progress rings smoothly around the remaining focus interval with a calm ambient glow.",
        "hint": "Tap ring to step Pomodoro intervals",
        "choreography": [
            "0-180ms: outer 25-minute ring and inner session ring prime from 12-o'clock.",
            "180-680ms: stroke-dashoffset glides cleanly to the active focus completion percentage.",
            "680-720ms: center minute readout and 'Deep Focus' pill lock cleanly."
        ],
        "agentPrompt": "Build a TickTick Pomodoro focus ring on #101422 with #4772FA and #38bdf8 concentric SVG arcs: animate stroke-dashoffset over 720ms cubic-bezier(0.22, 1, 0.36, 1) around a centered monospace focus percentage.",
        "cfg": {"bg": "#101422", "card": "#181f34", "accent": "#4772FA", "accent2": "#38bdf8", "label": "Pomodoro", "unit": "m", "scores": [25, 18, 12, 5], "tag": "Deep Focus"},
    },
    "bear": {
        "motionSlug": "markdown-tag-graph-link",
        "motionName": "Nested Tag Link Focus & Editorial Cursor",
        "engine": "graph_cursor_canvas",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Editorial", "surface": "light",
        "dur": 800, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["fill (active tag nodes)", "transform: translate (tag pills)"],
        "summary": "Linking nested `#tags` across Bear notes illuminates connected crimson nodes over crisp warm paper as floating tag labels glide between notes.",
        "hint": "Tap canvas to jump across #tags",
        "choreography": [
            "0-160ms: active note nodes light up in Bear crimson (#D94343).",
            "80-740ms: floating #tag pills glide cleanly across connected edges.",
            "740-800ms: settled cluster preserves generous editorial whitespace."
        ],
        "agentPrompt": "Create a Bear Markdown nested-tag link visualizer on #faf8f6 with #D94343 crimson accents: illuminate active SVG note nodes and glide floating #tag badges across edges over 800ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#faf8f6", "card": "#ffffff", "fg": "#1c1917", "accent": "#D94343", "accent2": "#52525b", "tag1": "#writing", "tag2": "#ideas/ui"},
    },
    "fantastical": {
        "motionSlug": "natural-language-parse-chips",
        "motionName": "Natural Language Event Parser Pill Cascade",
        "engine": "streaming_ai_cards",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 330, "c": 22},
        "props": ["opacity", "transform: translateY + scale (parsed chips)"],
        "summary": "Typing 'Coffee with Alex Fri 10am' in Fantastical pops parsed crimson date, time, and invitee chips into place in a crisp staggered sequence.",
        "hint": "Tap card to replay event parsing",
        "choreography": [
            "0-260ms: parsed Date, Time, and Location pills spring upward with 90ms stagger.",
            "160-400ms: structured calendar preview lines settle cleanly below.",
            "400-460ms: live parser caret blinks cleanly in #EF4444."
        ],
        "agentPrompt": "Build Fantastical's natural-language event parser on #faf7f7 with #EF4444 crimson pills: stagger parsed Date/Time/Guest pills upward (translateY 6px -> 0, scale 0.92 -> 1) by 90ms over 380ms cubic-bezier(0.22, 1.2, 0.36, 1).",
        "cfg": {"bg": "#faf6f6", "card": "#ffffff", "fg": "#111827", "accent": "#EF4444", "sources": ["Fri · Nov 27", "10:00 AM", "📍 Sightglass"], "lines": ["Coffee with Alex Fri 10am at Sightglass", "Added to Work Calendar"]},
    },
    "notion-calendar": {
        "motionSlug": "timezone-pill-snap",
        "motionName": "Multi-Timezone Day Switcher Pill Snap",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Crisp", "surface": "dark",
        "dur": 360, "ease": {"t": "spring", "k": 360, "c": 26},
        "props": ["transform: translateX (monochrome pill)", "color", "textContent"],
        "summary": "Toggling timezones in Notion Calendar snaps a razor-sharp graphite pill across SF, Lisbon, and Tokyo slots with zero wasted motion.",
        "hint": "Switch timezone tabs",
        "choreography": [
            "0-50ms: selected city snaps to crisp white text.",
            "50-300ms: sliding indicator translates across columns on tight spring(360, 26).",
            "300-360ms: local time readout updates instantaneously in monospace."
        ],
        "agentPrompt": "Build Notion Calendar's ultra-crisp timezone switcher on #0f0f10 with #3f3f46 pill indicator: glide the active pill horizontally over 360ms cubic-bezier(0.22, 1.18, 0.36, 1) synchronized with a live monospace time readout.",
        "cfg": {"bg": "#0f0f10", "card": "#18181b", "accent": "#3f3f46", "tabs": ["PST", "WET", "JST"], "tabVals": ["09:30 AM", "05:30 PM", "02:30 AM"]},
    },
    "superhuman": {
        "motionSlug": "hotkey-archive-swoosh",
        "motionName": "Keyboard 'E' Archive Swoosh & Undo Toast",
        "engine": "list_swipe_action",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 380, "ease": {"t": "spring", "k": 380, "c": 26},
        "props": ["transform: translateX (thread swoosh)", "transform: translateY (undo snackbar)", "opacity"],
        "summary": "Hitting 'E' to archive in Superhuman launches the email row cleanly across a royal-indigo track while surfacing a razor-fast Undo toast below.",
        "hint": "Tap email row to archive at 100ms speed",
        "choreography": [
            "0-80ms: check indicator lights indigo as row accelerates rightward.",
            "40-320ms: email row translates +92px on taut spring(380, 26).",
            "140-380ms: compact Undo snackbar slides up 10px cleanly."
        ],
        "agentPrompt": "Recreate Superhuman's fast archive swoosh on #0d0e14 with #4F46E5 indigo reveal: translate the dark email row +92px over 380ms cubic-bezier(0.22, 1.14, 0.36, 1) and float an Undo toast underneath.",
        "cfg": {"bg": "#0d0e14", "card": "#171923", "accent": "#4F46E5", "rowTitle": "Investor Update — Q4", "rowSub": "Inbox · Press E to archive", "actionLbl": "Archive"},
    },
    "spark-mail": {
        "motionSlug": "smart-snooze-swipe",
        "motionName": "Smart Inbox Swipe-to-Snooze & Undo Pill",
        "engine": "list_swipe_action",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Fluid", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateX", "transform: translateY (toast)"],
        "summary": "Swiping an email in Spark Mail reveals a crisp blue Snooze band beneath the message card and floats a gentle Undo bar below.",
        "hint": "Tap message row to snooze",
        "choreography": [
            "0-100ms: circular selection ring fills Spark blue (#3B82F6).",
            "40-360ms: email card slides +92px rightward exposing the Snooze action.",
            "180-420ms: Undo pill springs upward smoothly."
        ],
        "agentPrompt": "Build Spark Mail's swipe-to-snooze interaction on #f3f6fb with #3B82F6 reveal backing: slide the white message card +92px over 420ms cubic-bezier(0.22, 1.14, 0.36, 1) and raise an Undo snackbar.",
        "cfg": {"bg": "#f3f6fb", "card": "#ffffff", "fg": "#0f172a", "accent": "#3B82F6", "rowTitle": "Flight confirmation LIS → NYC", "rowSub": "Smart Inbox · Tomorrow 9am", "actionLbl": "Snooze"},
    },
    "microsoft-teams": {
        "motionSlug": "meeting-reaction-stream",
        "motionName": "Live Meeting Status Chips & Chat Reveal",
        "engine": "streaming_ai_cards",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 460, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["opacity", "transform: translateY + scale"],
        "summary": "Microsoft Teams' live call sidebar cascades purple reaction pills and live captions cleanly into view with 90ms stagger.",
        "hint": "Tap call card to replay live reactions",
        "choreography": [
            "0-260ms: raised-hand and reaction pills spring up in #5B5FC7 violet.",
            "160-400ms: live speaker caption lines fade smoothly into place.",
            "400-460ms: live caption caret pulses steadily."
        ],
        "agentPrompt": "Build a Microsoft Teams live meeting caption & reaction stream on #14141c with #5B5FC7 indigo badges: stagger 3 reaction pills upward by 90ms over 380ms cubic-bezier(0.22, 1.2, 0.36, 1) above streaming caption text.",
        "cfg": {"bg": "#14141c", "card": "#1e1f2b", "accent": "#5B5FC7", "sources": ["✋ Hand Raised", "👏 +6", "● Rec"], "lines": ["Product Sync · 12 participants", "Action item: ship API docs Friday"]},
    },
    "zoom": {
        "motionSlug": "active-speaker-waveform",
        "motionName": "Active Speaker Mic Waveform & Mute Toggle",
        "engine": "waveform_audio",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "dark",
        "dur": 260, "ease": {"t": "bezier", "p": [0.22, 1.2, 0.36, 1]},
        "props": ["background-color (live audio bars)", "transform: scaleY"],
        "summary": "Zoom's active-speaker audio bar animates crisp royal-blue voice levels across 18 micro-bars with instant click-to-mute feedback.",
        "hint": "Tap toggle or scrub audio levels",
        "choreography": [
            "Continuous: 18 rounded bars pulse across #0B5CFF blue to visualize active speech.",
            "Active bar pops vertically to scaleY(1.22) in lighter sky accent.",
            "Tap toggles live microphone stream instantaneously."
        ],
        "agentPrompt": "Build Zoom's active-speaker audio monitor pill on #11151e with #0B5CFF blue accent: pair a 38px circular toggle with 18 variable-height bars highlighting speech progression and scaling the active bar to 1.22.",
        "cfg": {"bg": "#11151e", "card": "#1a202e", "accent": "#0B5CFF", "accent2": "#60a5fa", "track": "HD Audio · Active Speaker", "bars": [22, 48, 76, 54, 90, 62, 40, 84, 96, 58, 36, 78, 88, 50, 66, 44, 72, 28]},
    },
    "loom": {
        "motionSlug": "camera-bubble-cursor-tour",
        "motionName": "Async Screen Walkthrough Cursors & Focus Nodes",
        "engine": "graph_cursor_canvas",
        "use": "Micro-interactions", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 820, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: translate (presenter cursor)", "fill + filter: drop-shadow (clicked nodes)"],
        "summary": "Recording a Loom walkthrough glides the presenter's violet highlight cursor cleanly between UI hotspots with crisp click-ring illumination.",
        "hint": "Tap canvas to advance walkthrough cue",
        "choreography": [
            "0-160ms: target UI node illuminates in #625DF5 electric purple.",
            "80-760ms: presenter and viewer cursor pills glide across the canvas.",
            "760-820ms: click target settles cleanly."
        ],
        "agentPrompt": "Create a Loom walkthrough hotspot canvas on #121121 with #625DF5 violet accents: glide two cursor tags across 5 connected SVG hotspots over 820ms cubic-bezier(0.22, 1, 0.36, 1) while glowing the active target.",
        "cfg": {"bg": "#121121", "card": "#1c1a33", "accent": "#625DF5", "accent2": "#ec4899", "tag1": "● Rec 0:18", "tag2": "Viewer"},
    },
    "miro": {
        "motionSlug": "multiplayer-whiteboard-cursors",
        "motionName": "Multiplayer Whiteboard Cursor Chase & Node Snap",
        "engine": "graph_cursor_canvas",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Playful", "surface": "light",
        "dur": 820, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: translate (collaborator cursors)", "fill (connected board nodes)"],
        "summary": "Miro's infinite canvas glides colored teammate cursors smoothly across connected sticky-note clusters over a crisp dotted whiteboard grid.",
        "hint": "Tap whiteboard to move collaborators",
        "choreography": [
            "0-180ms: active flowchart nodes light up in warm Miro amber (#f59e0b).",
            "60-760ms: two labeled collaborator cursors glide smoothly to new board positions.",
            "760-820ms: cursors settle without abrupt stops."
        ],
        "agentPrompt": "Build a Miro multiplayer whiteboard preview on #faf9f5 with dotted grid and #f59e0b/#3b82f6 collaborator cursors: animate cursor tags and connected SVG flowchart nodes over 820ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#faf9f5", "card": "#ffffff", "fg": "#18181b", "accent": "#f59e0b", "accent2": "#2563eb", "tag1": "Sofia", "tag2": "Devon"},
    },
    "figma": {
        "motionSlug": "multiplayer-canvas-cursors",
        "motionName": "Multiplayer Cursor Trail & Vector Node Highlight",
        "engine": "graph_cursor_canvas",
        "use": "Navigation and layout", "stack": "SVG", "trigger": "Click", "feel": "Fluid", "surface": "dark",
        "dur": 800, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: translate (nametag cursors)", "fill + drop-shadow (vector nodes)"],
        "summary": "Collaborating live in Figma glides crisp nametag cursors smoothly across linked vector anchor nodes on a dark precision grid.",
        "hint": "Tap canvas to jump cursors to next frame",
        "choreography": [
            "0-150ms: selected vector anchor points glow in #A259FF Figma purple.",
            "60-740ms: purple and cyan designer cursors glide smoothly across the artboard.",
            "740-800ms: cursors land cleanly on the next anchor pair."
        ],
        "agentPrompt": "Recreate Figma's multiplayer cursor canvas on #1e1e1e with #A259FF purple and #0acf83 emerald cursors: animate labeled cursor pills across 5 linked SVG vector points over 800ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#1a1a1d", "card": "#242428", "accent": "#A259FF", "accent2": "#0acf83", "tag1": "Elena", "tag2": "Kai"},
    },
    "trello": {
        "motionSlug": "kanban-card-move-undo",
        "motionName": "Kanban Card Move Swipe & Done Toast",
        "engine": "list_swipe_action",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 310, "c": 22},
        "props": ["transform: translateX", "transform: translateY (undo bar)"],
        "summary": "Moving a Trello card to Done glides the board tile cleanly rightward across Trello blue while floating an instant Undo snackbar underneath.",
        "hint": "Tap Trello card to move to Done",
        "choreography": [
            "0-90ms: checkbox fills Trello blue (#0079BF).",
            "40-360ms: card translates +92px on spring(310, 22) exposing the Done badge.",
            "160-420ms: Undo toast glides up smoothly."
        ],
        "agentPrompt": "Build a Trello card-to-Done swipe interaction on #eef5fa with #0079BF action layer: slide the card +92px over 420ms cubic-bezier(0.22, 1.14, 0.36, 1) and float an Undo bar.",
        "cfg": {"bg": "#eef5fa", "card": "#ffffff", "fg": "#0f172a", "accent": "#0079BF", "rowTitle": "QA dark-mode shader tiles", "rowSub": "In Review · Board #04", "actionLbl": "Move Done"},
    },
    "asana": {
        "motionSlug": "workflow-stage-tabs",
        "motionName": "Project View Segmented Morph (List / Board / Timeline)",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Fluid", "surface": "dark",
        "dur": 380, "ease": {"t": "spring", "k": 320, "c": 24},
        "props": ["transform: translateX (coral indicator)", "color", "textContent"],
        "summary": "Switching an Asana project between List, Board, and Timeline glides a warm coral pill indicator smoothly across the top segmented switcher.",
        "hint": "Tap tabs to switch project views",
        "choreography": [
            "0-60ms: selected view label snaps to crisp white.",
            "60-320ms: #F06A6A indicator translates horizontally with gentle overshoot.",
            "320-380ms: summary metric card updates immediately."
        ],
        "agentPrompt": "Create Asana's view switcher on #151419 with #F06A6A coral pill: translate the active thumb across List/Board/Timeline over 380ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#151419", "card": "#201e26", "accent": "#F06A6A", "tabs": ["List", "Board", "Timeline"], "tabVals": ["18 tasks", "4 columns", "Q4 launch"]},
    },
    "clickup": {
        "motionSlug": "status-milestone-stepper",
        "motionName": "Task Status Stepper Morph & Glow Ring",
        "engine": "stepper_progress_flow",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Playful", "surface": "dark",
        "dur": 450, "ease": {"t": "spring", "k": 320, "c": 21},
        "props": ["width (connector fill)", "transform: scale (active status)", "box-shadow"],
        "summary": "Advancing a ClickUp task from To Do through Review to Complete sweeps a vibrant purple bar across status milestones with a glowing active ring.",
        "hint": "Tap status steps to advance task",
        "choreography": [
            "0-80ms: active status node scales to 1.2x with translucent #7B68EE aura.",
            "40-390ms: progress connector expands smoothly to the target milestone.",
            "390-450ms: completed steps lock in solid purple."
        ],
        "agentPrompt": "Build ClickUp's status milestone stepper on #13111c with #7B68EE purple fill: animate a 4px progress bar and 4 interactive step nodes scaling 1.2x on spring(320, 21).",
        "cfg": {"bg": "#13111c", "card": "#1d1a2b", "accent": "#7B68EE", "steps": ["To Do", "Active", "Review", "Done"]},
    },
    "jira": {
        "motionSlug": "sprint-issue-stepper",
        "motionName": "Sprint Issue Transition Flow & Blue Connector",
        "engine": "stepper_progress_flow",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 450, "ease": {"t": "spring", "k": 320, "c": 24},
        "props": ["width (sprint bar)", "transform: scale (stage node)"],
        "summary": "Moving a Jira ticket across sprint stages advances an Atlassian-blue progress connector cleanly through Backlog, Dev, QA, and Shipped.",
        "hint": "Click any sprint stage",
        "choreography": [
            "0-70ms: selected sprint stage scales up 1.2x with blue focus ring.",
            "40-390ms: #0052CC progress fill glides cleanly across the track.",
            "390-450ms: prior stages lock filled."
        ],
        "agentPrompt": "Create a Jira sprint transition stepper on #f4f5f7 with #0052CC Atlassian blue: connect 4 stage buttons over a 4px bar animating width over 450ms cubic-bezier(0.22, 1.15, 0.36, 1).",
        "cfg": {"bg": "#f4f5f7", "card": "#ffffff", "fg": "#172b4d", "accent": "#0052CC", "steps": ["Backlog", "In Dev", "QA", "Shipped"]},
    },
    "calendly": {
        "motionSlug": "time-slot-confirm-sheet",
        "motionName": "Booking Time-Slot Sheet & Blue Confirm Snap",
        "engine": "sheet_detent_drawer",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateY (booking sheet)", "background-color (time slot)"],
        "summary": "Choosing an available slot on Calendly springs up a clean booking card where tapping any time chip snaps it into crisp Calendly blue.",
        "hint": "Tap sheet or pick a meeting slot",
        "choreography": [
            "0-360ms: rounded booking sheet rises smoothly from 56px peek to full height.",
            "160-460ms: tapping a time slot highlights it in #006BFF with instant Confirm CTA."
        ],
        "agentPrompt": "Build Calendly's mobile slot-picker sheet on #f3f7ff with #006BFF accent: spring-raise the booking drawer over 460ms cubic-bezier(0.22, 1.18, 0.36, 1) with 3 selectable time chips.",
        "cfg": {"bg": "#f3f7ff", "card": "#ffffff", "fg": "#0f172a", "accent": "#006BFF", "sheetTitle": "30 Min Intro Call", "chips": ["10:00am", "11:30am", "2:00pm"], "cta": "Confirm Booking"},
    },
    "dropbox": {
        "motionSlug": "file-sync-swipe-action",
        "motionName": "Cloud File Offline Sync Swipe & Toast",
        "engine": "list_swipe_action",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateX", "transform: translateY (sync toast)"],
        "summary": "Making a Dropbox folder available offline glides the file row smoothly over cobalt blue while confirming sync status in a bottom toast.",
        "hint": "Tap file row to pin offline",
        "choreography": [
            "0-90ms: sync dot fills #0061FF cobalt.",
            "40-360ms: file row translates +92px revealing the offline pin action.",
            "160-420ms: bottom Undo bar rises cleanly."
        ],
        "agentPrompt": "Build a Dropbox file sync swipe interaction on #f5f7fa with #0061FF accent: translate the file row +92px over 420ms cubic-bezier(0.22, 1.14, 0.36, 1) and float an Undo toast.",
        "cfg": {"bg": "#f5f7fa", "card": "#ffffff", "fg": "#101114", "accent": "#0061FF", "rowTitle": "Brand_Assets_v4.zip", "rowSub": "184 MB · Cloud only", "actionLbl": "Pin Offline"},
    },
    "google-drive": {
        "motionSlug": "quick-upload-sheet-rise",
        "motionName": "Create New Sheet Detent & Quick-Action Chips",
        "engine": "sheet_detent_drawer",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Click", "feel": "Fluid", "surface": "light",
        "dur": 460, "ease": {"t": "spring", "k": 300, "c": 24},
        "props": ["transform: translateY", "background-color"],
        "summary": "Tapping '+' in Google Drive springs up a clean Material bottom sheet with quick chips for Scan, Upload, and New Doc.",
        "hint": "Tap sheet or select upload action",
        "choreography": [
            "0-360ms: Material drawer rises smoothly from translateY(56px) -> 0.",
            "160-460ms: action chips toggle cleanly in #4285F4 Google Blue."
        ],
        "agentPrompt": "Build Google Drive's Create New bottom sheet on #f5f8fd with #4285F4 accent: translate the rounded sheet upward over 460ms cubic-bezier(0.22, 1.18, 0.36, 1) with selectable quick-action pills.",
        "cfg": {"bg": "#f5f8fd", "card": "#ffffff", "fg": "#111827", "accent": "#4285F4", "sheetTitle": "Create in My Drive", "chips": ["Folder", "Scan", "Upload"], "cta": "Continue"},
    },
    "gmail": {
        "motionSlug": "swipe-archive-emerald-undo",
        "motionName": "Swipe-to-Archive Emerald Reveal & Undo Bar",
        "engine": "list_swipe_action",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Tactile", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 320, "c": 23},
        "props": ["transform: translateX (thread card)", "transform: translateY (Undo snackbar)"],
        "summary": "Swiping a Gmail message glides the thread card across an unmistakable green Archive track while lifting a dark Material Undo snackbar.",
        "hint": "Tap email to swipe-archive & Undo",
        "choreography": [
            "0-80ms: tap initiates horizontal thread slide exposing the emerald Archive backing.",
            "40-360ms: message card eases +92px rightward on spring(320, 23).",
            "160-420ms: dark Material Undo snackbar glides up cleanly."
        ],
        "agentPrompt": "Recreate Gmail's swipe-to-archive interaction on #f6f8fc with #16a34a archive reveal: slide the message card +92px over 420ms cubic-bezier(0.22, 1.14, 0.36, 1) and float a dark Undo snackbar underneath.",
        "cfg": {"bg": "#f6f8fc", "card": "#ffffff", "fg": "#111827", "accent": "#16a34a", "rowTitle": "Netlify Deploy Succeeded", "rowSub": "Primary · Just now", "actionLbl": "Archive"},
    },
    "outlook": {
        "motionSlug": "focused-other-pill-glide",
        "motionName": "Focused ↔ Other Inbox Segmented Glide",
        "engine": "segmented_pill_morph",
        "use": "Navigation and layout", "stack": "CSS", "trigger": "Tab switch", "feel": "Crisp", "surface": "light",
        "dur": 380, "ease": {"t": "spring", "k": 340, "c": 25},
        "props": ["transform: translateX (blue pill)", "color", "textContent"],
        "summary": "Flipping between Outlook's Focused, Other, and Flagged tabs glides a crisp Microsoft-blue indicator smoothly across the inbox header.",
        "hint": "Tap tabs to switch inbox views",
        "choreography": [
            "0-60ms: tapped inbox tab takes white active text.",
            "60-320ms: #0078D4 pill glides smoothly across columns.",
            "320-380ms: unread counter card refreshes cleanly."
        ],
        "agentPrompt": "Build Microsoft Outlook's Focused/Other inbox switcher on #f3f7fc with #0078D4 pill indicator: slide the active pill via translateX(i * 100%) over 380ms cubic-bezier(0.22, 1.18, 0.36, 1).",
        "cfg": {"bg": "#f3f7fc", "card": "#ffffff", "fg": "#0f172a", "accent": "#0078D4", "tabs": ["Focused", "Other", "Flagged"], "tabVals": ["4 unread", "19 newsletters", "2 follow-ups"]},
    },
    "evernote": {
        "motionSlug": "quick-note-sync-swipe",
        "motionName": "Quick Note Pin Swipe & Emerald Confirm",
        "engine": "list_swipe_action",
        "use": "Micro-interactions", "stack": "CSS", "trigger": "Click", "feel": "Crisp", "surface": "light",
        "dur": 420, "ease": {"t": "spring", "k": 310, "c": 23},
        "props": ["transform: translateX", "transform: translateY"],
        "summary": "Swiping a note in Evernote glides the crisp white card over Evernote emerald to pin it to Shortcuts with a neat Undo toast below.",
        "hint": "Tap note row to pin to Shortcuts",
        "choreography": [
            "0-80ms: green check ring fills instantaneously.",
            "40-360ms: note row slides +92px revealing Evernote emerald (#00A82D).",
            "160-420ms: Undo toast glides up smoothly."
        ],
        "agentPrompt": "Build Evernote's note-pin swipe row on #f3faf5 with #00A82D backing: translate the card +92px over 420ms cubic-bezier(0.22, 1.14, 0.36, 1) and float an Undo bar.",
        "cfg": {"bg": "#f3faf5", "card": "#ffffff", "fg": "#111827", "accent": "#00A82D", "rowTitle": "Architecture Meeting Notes", "rowSub": "Notebooks · Synced", "actionLbl": "Pin Note"},
    },
    "goodnotes": {
        "motionSlug": "canvas-lasso-node-snap",
        "motionName": "Handwriting Canvas Pen & Lasso Node Glide",
        "engine": "graph_cursor_canvas",
        "use": "Generative", "stack": "SVG", "trigger": "Click", "feel": "Organic", "surface": "light",
        "dur": 800, "ease": {"t": "bezier", "p": [0.22, 1, 0.36, 1]},
        "props": ["transform: translate (stylus & lasso tags)", "fill (highlighted strokes)"],
        "summary": "Annotating a dotted Goodnotes notebook glides stylus and lasso tags across sketched diagram nodes with crisp blue highlight feedback.",
        "hint": "Tap notebook page to move stylus focus",
        "choreography": [
            "0-160ms: targeted diagram nodes highlight in #2B9CF6 ink blue.",
            "80-740ms: Fountain Pen and Lasso tags glide across the dotted paper grid.",
            "740-800ms: active annotation cluster settles smoothly."
        ],
        "agentPrompt": "Build a Goodnotes dotted-paper annotation preview on #f8fafc with #2B9CF6 fountain-pen and #f59e0b highlighter cursor badges gliding across linked SVG nodes over 800ms cubic-bezier(0.22, 1, 0.36, 1).",
        "cfg": {"bg": "#f8fafc", "card": "#ffffff", "fg": "#0f172a", "accent": "#2B9CF6", "accent2": "#f59e0b", "tag1": "Pen 0.5mm", "tag2": "Lasso"},
    },
}

out = [build_motion_entry(META[slug], spec) for slug, spec in SPECS.items()]
dest = ROOT / "data" / "packs" / "apps-productivity.json"
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(out)} motions to {dest.name}")
