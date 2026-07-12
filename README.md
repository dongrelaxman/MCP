# MCP Demo Server

A simple MCP (Model Context Protocol) server built with [FastMCP](https://github.com/jlowin/fastmcp).

## Requirements

- Python >= 3.11
- fastmcp

## Installation

```bash
pip install -r requirements.txt
```

Or with uv:

```bash
uv sync
```

## Tools

- **roll_dice(n_dice)** — Rolls `n` six-sided dice and returns the results
- **add_number(a, b)** — Adds two numbers and returns the result

## Local vs Remote Server

### Local (stdio)
- Runs as a subprocess, communicates via stdin/stdout
- Only accessible to the process that spawned it (e.g. Claude Desktop)
- No network port, no auth needed

**Claude Desktop config** (`~/.claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "demo": {
      "command": "python",
      "args": ["/path/to/main.py"]
    }
  }
}
```

**Test with inspector:**
```bash
uv run fastmcp dev main.py
```

---

### Remote (streamable-http)
- Runs as a persistent HTTP server accessible over the network
- Any client connects via URL — Claude Desktop, inspector, or custom apps
- Server must be running before clients connect

**Start the server:**
```bash
python main.py
```

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "demo": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**Test with inspector:**
```bash
npx @modelcontextprotocol/inspector
```
Then change the URL field to `http://localhost:8000/mcp` and click **Connect**.
