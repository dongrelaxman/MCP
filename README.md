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

## Running the Server

```bash
python main.py
```
