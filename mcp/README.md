# Motion Index MCP Server

Zero-dependency Node.js Model Context Protocol (MCP) server for **Motion Index**, giving coding agents (Claude Code, Cursor, Codex, Windsurf) direct access to curated UI motion specs, stack-adapted code, and custom URL/video motion extraction.

## Tools

1. **`search_motions(query, pattern?, trigger?, feel?, stack?, app?, limit?)`**
   Free, public discovery across the Motion Index library. Returns compact matches, IDs, physics summaries, and interactive preview URLs.
2. **`get_motion_code(id, stack?, designTokens?)`**
   Fetches the structured Motion IR, extractable code, choreography beats, and stack-specific adaptation instructions (`CSS`, `React/Motion`, `GSAP`, `SwiftUI`, `Remotion`). Automatically enforces **Brand Motion Tokens** when using a Teams API key or passing `designTokens`.
3. **`extract_motion(url?, videoUrl?, stack?, notes?)`**
   Queues a custom extraction job from a live web URL or video recording (Pro: 30/mo, Teams: 150/mo, or API Credits: 10 credits/job).

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `MOTION_INDEX_API_KEY` | For `get_motion_code` & `extract_motion` | — | Your `mi_live_...` or `mi_test_...` API key |
| `MOTION_INDEX_API_URL` | No | `https://ai-motion-database.netlify.app` | API origin (set `local` to force local repo catalog) |
| `MOTION_INDEX_LOCAL_ONLY` | No | `0` | Set `1` to run purely against the local `data/motions.json` catalog |

## Setup

### Claude Code

```bash
claude mcp add motion-index \
  -e MOTION_INDEX_API_KEY="mi_test_your_key_here" \
  -- node /absolute/path/to/ai-motion-database/mcp/server.mjs
```

Or connect directly to the hosted HTTP MCP endpoint:

```bash
claude mcp add --transport http motion-index \
  https://ai-motion-database.netlify.app/api/mcp \
  --header "Authorization: Bearer mi_test_your_key_here"
```

### Cursor (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "motion-index": {
      "command": "node",
      "args": ["/absolute/path/to/ai-motion-database/mcp/server.mjs"],
      "env": {
        "MOTION_INDEX_API_KEY": "mi_test_your_key_here",
        "MOTION_INDEX_API_URL": "https://ai-motion-database.netlify.app"
      }
    }
  }
}
```

### Codex (`~/.codex/config.toml`)

```toml
[mcp_servers.motion_index]
command = "node"
args = ["/absolute/path/to/ai-motion-database/mcp/server.mjs"]

[mcp_servers.motion_index.env]
MOTION_INDEX_API_KEY = "mi_test_your_key_here"
MOTION_INDEX_API_URL = "https://ai-motion-database.netlify.app"
```
