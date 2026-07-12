import asyncio
import json
import os
from dotenv import load_dotenv
from fastmcp import Client
from openai import AsyncOpenAI

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000/mcp")

def to_openai_tools(mcp_tools):
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        }
        for tool in mcp_tools
    ]

async def run(user_prompt: str) -> dict:
    openai = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tool_calls_log = []

    async with Client(SERVER_URL) as mcp:
        tools = await mcp.list_tools()
        openai_tools = to_openai_tools(tools)
        messages = [{"role": "user", "content": user_prompt}]

        while True:
            response = await openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=openai_tools,
            )

            message = response.choices[0].message
            messages.append(message)

            if not message.tool_calls:
                return {"tool_calls": tool_calls_log, "answer": message.content}

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                result = await mcp.call_tool(name, args)
                tool_calls_log.append({"name": name, "args": args, "result": str(result)})
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })

if __name__ == "__main__":
    prompt = "Roll 3 dice and add the first two results together"
    result = asyncio.run(run(prompt))
    for tc in result["tool_calls"]:
        print(f"  -> {tc['name']}({tc['args']}) = {tc['result']}")
    print(f"Assistant: {result['answer']}")
