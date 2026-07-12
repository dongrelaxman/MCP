# MCP Demo

A simple [Model Context Protocol](https://modelcontextprotocol.io) project built with [FastMCP](https://gofastmcp.com).

The client is a Streamlit chat UI powered by GPT-4o-mini. It talks to an MCP server over HTTP and uses its tools to answer questions.

```
mcp-test/
├── server/             # FastMCP server exposing tools over streamable-http
│   └── main.py
├── client/
│   ├── main.py         # MCP client + OpenAI tool-calling logic
│   └── streamlit_app.py  # Streamlit chat UI
└── docker-compose.yaml
```

---

## Quickstart (Docker)

```bash
cp .env.example .env   # add your OPENAI_API_KEY
docker compose up --build
```

Open **http://localhost:8501** in your browser.

The compose file starts the server first, waits for it to be healthy, then starts the Streamlit client.

### Environment variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Required. Used by the client to call GPT-4o-mini. |
| `SERVER_URL` | MCP server URL. Defaults to `http://localhost:8000/mcp`. |

---

## Architecture

```
 Streamlit
     │
     ▼
  Client (LLM)
     │                   ┌─────────────┐
     ├── calls tools ──► │   Server    │
     │                   └──────┬──────┘
     │◄── tool results ─────────┘
     │
     ▼
  Client (LLM)
     │
     ▼
 Streamlit
```

> For a detailed breakdown of how each piece works, see [docs/architecture.md](docs/architecture.md).

---

## Server tools

- **rool_dice(n_dice)** — Rolls `n` six-sided dice and returns the results
- **add_number(a, b)** — Adds two numbers

---

## Running locally (without Docker)

### Server
```bash
cd server
pip install -r requirements.txt
python main.py
```
Server starts at `http://localhost:8000/mcp`.

### Client
```bash
cd client
pip install -r requirements.txt
streamlit run streamlit_app.py
```
UI starts at `http://localhost:8501`.

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
