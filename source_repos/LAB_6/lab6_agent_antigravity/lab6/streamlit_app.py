import os
import streamlit as st

from lab6.agent import run_agent

st.set_page_config(page_title="Lab 6 Agent Chat (No Snowflake)", layout="wide")
st.title("Lab 6: Agent-enabled Streamlit App (No Snowflake)")

st.caption("This app demonstrates an agent that can call local tools (RAG retrieval, summarization, analytics, plotting).")

with st.sidebar:
    st.subheader("Settings")
    model = st.text_input("OpenAI model (if using OPENAI_API_KEY)", value="gpt-4.1-mini")
    st.markdown("**Tip:** Set `OPENAI_API_KEY` in your environment to enable tool-calling agent.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

        if m.get("image_path"):
            st.image(m["image_path"])

user_input = st.chat_input("Ask something (e.g., 'retrieve docs about hurricane risk' or 'summarize hurricane notes')")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Agent is working..."):
            result = run_agent(user_input, model=model)

        if not result.get("ok"):
            st.error(result.get("error", "Unknown error"))
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {result.get('error','Unknown')}"})
        else:
            answer = result.get("answer", "")
            st.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})
