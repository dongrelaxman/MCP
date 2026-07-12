import asyncio
import streamlit as st
from main import run

st.title("MCP Demo")
st.caption("Powered by GPT-4o-mini + FastMCP tools")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("tool_calls"):
            with st.expander("Tool calls"):
                for tc in msg["tool_calls"]:
                    st.code(f"{tc['name']}({tc['args']}) → {tc['result']}")
        st.write(msg["content"])

if prompt := st.chat_input("Ask something... e.g. Roll 5 dice and add the results"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = asyncio.run(run(prompt))

        if result["tool_calls"]:
            with st.expander("Tool calls"):
                for tc in result["tool_calls"]:
                    st.code(f"{tc['name']}({tc['args']}) → {tc['result']}")

        st.write(result["answer"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "tool_calls": result["tool_calls"],
    })
