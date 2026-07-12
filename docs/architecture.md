# Architecture — How Everything Is Connected

## Overview

This project has three layers that work together:

```
┌─────────────────────────────────────────────────────┐
│                    Browser                          │
│              http://localhost:8501                  │
└─────────────────────┬───────────────────────────────┘
                      │ user types a message
                      ▼
┌─────────────────────────────────────────────────────┐
│             Streamlit UI  (streamlit_app.py)        │
│                                                     │
│  - Renders the chat interface                       │
│  - Calls run(prompt) from main.py                   │
│  - Displays the answer + tool call details          │
└─────────────────────┬───────────────────────────────┘
                      │ calls run(prompt)
                      ▼
┌─────────────────────────────────────────────────────┐
│              MCP Client  (main.py)                  │
│                                                     │
│  - Connects to the MCP server                       │
│  - Fetches the list of available tools              │
│  - Converts MCP tools → OpenAI function format      │
│  - Sends the prompt + tools to GPT-4o-mini          │
│  - Executes any tool calls the model requests       │
│  - Returns { answer, tool_calls } to Streamlit      │
└──────────┬──────────────────────────┬───────────────┘
           │ list_tools / call_tool   │ chat.completions.create
           ▼                          ▼
┌──────────────────┐       ┌──────────────────────────┐
│   MCP Server     │       │     GPT-4o-mini           │
│   (server/)      │       │     (OpenAI API)          │
│                  │       │                           │
│  rool_dice()     │       │  Decides which tools      │
│  add_number()    │       │  to call and with         │
│                  │       │  what arguments           │
│  port 8000       │       └──────────────────────────┘
└──────────────────┘
```

---

## Step-by-Step Flow

### 1. Streamlit collects the user message

`streamlit_app.py` renders a chat input box. When the user submits a message, it calls:

```python
result = asyncio.run(run(prompt))
```

`run()` lives in `main.py` and does all the heavy lifting.

---

### 2. The client connects to the MCP server and fetches tools

Inside `run()`, a FastMCP `Client` connects to the server and asks what tools are available:

```python
async with Client(SERVER_URL) as mcp:
    tools = await mcp.list_tools()
```

The server responds with:

```
rool_dice(n_dice: int) → list[int]
add_number(a: float, b: float) → float
```

---

### 3. MCP tools are converted to OpenAI function format

GPT-4o-mini expects tools in OpenAI's function-calling schema. The client converts them:

```python
{
    "type": "function",
    "function": {
        "name": "rool_dice",
        "description": "Rolls n_dice 6-sided dice and returns results",
        "parameters": { "type": "object", "properties": { "n_dice": { "type": "integer" } } }
    }
}
```

---

### 4. The prompt + tools are sent to GPT-4o-mini

```python
response = await openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=openai_tools,
)
```

The model reads the prompt and decides:
- **If no tool is needed** → returns a plain text answer. Done.
- **If a tool is needed** → returns a `tool_calls` list with the tool name and arguments to use.

---

### 5. The client executes tool calls against the MCP server

For each tool call the model requested:

```python
result = await mcp.call_tool(name, args)
```

The MCP server runs the actual Python function (`rool_dice` or `add_number`) and returns the result.

The client appends the result back into the conversation as a `tool` message and calls the model again.

---

### 6. The model produces a final answer

With the tool results now in context, GPT-4o-mini generates a natural language answer:

> "You rolled [5, 4, 6]. The sum of the first two results is 9."

`run()` returns:

```python
{
    "answer": "You rolled [5, 4, 6]. The sum of the first two results is 9.",
    "tool_calls": [
        {"name": "rool_dice", "args": {"n_dice": 3}, "result": "[5, 4, 6]"},
        {"name": "add_number", "args": {"a": 5, "b": 4}, "result": "9.0"}
    ]
}
```

---

### 7. Streamlit displays the result

`streamlit_app.py` renders the answer in the chat bubble and shows the tool calls in a collapsible expander:

```
Assistant: You rolled [5, 4, 6]. The sum of the first two is 9.
  ▶ Tool calls
      rool_dice({'n_dice': 3}) → [5, 4, 6]
      add_number({'a': 5, 'b': 4}) → 9.0
```

---

## File Reference

| File | Role |
|---|---|
| `server/main.py` | Defines MCP tools using FastMCP, serves them over HTTP on port 8000 |
| `client/main.py` | MCP client + OpenAI tool-calling loop, exposes `run(prompt)` |
| `client/streamlit_app.py` | Chat UI, calls `run()`, displays answer and tool call trace |
| `docker-compose.yaml` | Starts server first (health check), then client on port 8501 |

---

## Why MCP?

Without MCP, you would hardcode tool definitions in the client. With MCP, the server owns and exposes its own tools — the client discovers them at runtime. This means you can add new tools to the server without touching the client code.
