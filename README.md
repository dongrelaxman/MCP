# MCP Demo

A simple [Model Context Protocol](https://modelcontextprotocol.io) project built with [FastMCP](https://gofastmcp.com).

```
mcp-test/
├── server/   # MCP server exposing tools over HTTP
└── client/   # Python client that connects to the server
```

---

## Server

### Setup
```bash
cd server
uv sync
```

### Run
```bash
uv run python main.py
```
Server starts at `http://localhost:8000/mcp`

### Tools
- **rool_dice(n_dice)** — Rolls `n` six-sided dice and returns results
- **add_number(a, b)** — Adds two numbers

### Test with MCP Inspector
```bash
npx @modelcontextprotocol/inspector
```
Set URL to `http://localhost:8000/mcp` and click **Connect**.

### Claude Desktop config
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

---

## Client

### Setup
```bash
cd client
uv sync
```

### Run (server must be running first)
```bash
uv run python main.py
```
