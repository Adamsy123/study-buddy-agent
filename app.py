import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOL_SCHEMAS, call_tool

load_dotenv()

# Page setup
st.set_page_config(page_title="Study Buddy AI Agent", page_icon="🎓", layout="wide")

st.title("🎓 Study Buddy AI Agent")
st.caption("Your smart tutor for finding notes, creating flashcards, generating quizzes, and live web lookup!")

SYSTEM_PROMPT = """You are 'Study Buddy', an encouraging and efficient AI tutor.
Always use your available tools to search notes, create flashcards, test the user with quizzes, or search Wikipedia for extra context.
Break down complex topics clearly. Always format flashcards and quizzes cleanly using markdown.
"""

# ----------------------------------------------------------------------
# Sidebar & API Key Logic (Support custom key fallback for +3 Bonus Marks)
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Agent Settings")
    st.markdown("Customize your agent or clear session context.")
    
    custom_key = st.text_input("Use your own OpenAI Key (optional):", type="password")
    
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

    st.markdown("---")
    st.markdown("### 🧰 Available Tools")
    st.markdown("- 📌 `search_notes`\n- 🎴 `make_flashcards`\n- 📝 `quiz_me`\n- 🌐 `search_wikipedia` (Live API)")


def get_api_key():
    if custom_key.strip():
        return custom_key.strip()
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None


api_key = get_api_key()
if not api_key:
    st.error("⚠️ No API Key detected! Please enter your OpenAI API key in the sidebar or setup .env.")
    st.stop()

client = OpenAI(api_key=api_key)
MODEL = "gpt-4o-mini"

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Replay previous chat history
for msg in st.session_state.messages:
    role = msg["role"] if isinstance(msg, dict) else msg.role
    if role in ("user", "assistant"):
        content = msg["content"] if isinstance(msg, dict) else msg.content
        if content:
            with st.chat_message(role):
                st.markdown(content)

# ----------------------------------------------------------------------
# Chat Loop
# ----------------------------------------------------------------------
if prompt := st.chat_input("Ask for study notes, flashcards, or a quiz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("🧠 Agent thinking and running tools...", expanded=True) as status:
            while True:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    tools=TOOL_SCHEMAS,
                )
                message = response.choices[0].message

                if not message.tool_calls:
                    break

                st.session_state.messages.append(message)

                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    st.write(f"🔧 Calling **`{name}`** with args: `{args}`")

                    try:
                        result = call_tool(name, args)
                    except Exception as e:
                        result = f"Tool Execution Error: {e}"

                    st.write(f"↳ *Result:* {result[:120]}...")
                    st.session_state.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })

            status.update(label="✅ Reasoning complete!", state="complete", expanded=False)

        # Streaming Final Answer
        def stream_answer():
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                piece = chunk.choices[0].delta.content or ""
                if piece:
                    yield piece

        answer = st.write_stream(stream_answer())
        st.session_state.messages.append({"role": "assistant", "content": answer})