import os

import requests
import streamlit as st


def normalize_api_url(url: str) -> str:
    cleaned = (url or "").strip().rstrip("/")
    if not cleaned:
        return "http://localhost:8000"
    if cleaned.startswith(("http://", "https://")):
        return cleaned
    if cleaned.startswith("localhost") or cleaned.startswith("127.0.0.1"):
        return f"http://{cleaned}"
    return f"https://{cleaned}"


def get_default_api_url() -> str:
    env_url = os.getenv("API_URL")
    secret_url = None
    try:
        secret_url = st.secrets.get("API_URL")
    except Exception:
        secret_url = None
    return normalize_api_url(env_url or secret_url or "http://localhost:8000")


st.set_page_config(page_title="Disaster Forecast AI Application", layout="wide")
st.title("Disaster Forecast AI Application")
st.write(
    "This starter app combines a knowledge base, retrieval pipeline, domain-adapted model, "
    "agent reasoning, and Snowflake-ready warehouse facts."
)

with st.sidebar:
    st.subheader("Architecture")
    st.markdown(
        "\n".join(
            [
                "- Data Sources",
                "- Knowledge Base",
                "- Retrieval Pipeline",
                "- Domain-Adapted Model",
                "- AI Agent Reasoning",
                "- Snowflake Data Warehouse",
                "- Application Interface",
                "- Monitoring and Deployment",
            ]
        )
    )
    default_api_url = get_default_api_url()
    api_url = normalize_api_url(st.text_input("API URL", default_api_url))

st.subheader("Application Workflow")
st.markdown(
    "\n".join(
        [
            "1. The user enters an instruction, region, and forecast indicators.",
            "2. The system retrieves the most relevant planning guidance from the knowledge base.",
            "3. The agent queries Snowflake-ready warehouse facts or falls back to sample structured data.",
            "4. The agent combines user input, retrieved context, and facts into a grounded prompt.",
            "5. The domain-adapted model generates an explanation, or a safe fallback response is returned.",
            "6. Monitoring endpoints track health, metrics, and lightweight evaluation results.",
        ]
    )
)

instruction = st.text_input(
    "Instruction",
    "Explain hurricane forecast uncertainty for emergency planners.",
)
region = st.text_input("Region", "Gulf Coast")
user_input = st.text_area(
    "Forecast Input",
    "Storm probability 74%, confidence interval ±85 km, coastal population exposure 390000.",
    height=140,
)
top_k = st.slider("Retrieved documents", min_value=1, max_value=5, value=3)

if st.button("Run AI Pipeline", type="primary"):
    if not instruction or not user_input:
        st.warning("Please provide both an instruction and forecast input.")
    else:
        with st.spinner("Running retrieval, warehouse grounding, and generation..."):
            try:
                response = requests.post(
                    f"{api_url}/generate",
                    json={
                        "instruction": instruction,
                        "input": user_input,
                        "region": region,
                        "top_k": top_k,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                result = response.json()

                st.subheader("Explanation")
                st.write(result.get("explanation", ""))

                if result.get("used_fallback_model"):
                    st.info(
                        "The adapted model was not available at runtime, so the app returned a "
                        "fallback answer grounded in retrieval and warehouse context."
                    )

                left_col, right_col = st.columns(2)

                with left_col:
                    st.subheader("Retrieved Context")
                    for doc in result.get("retrieved_context", []):
                        st.markdown(
                            f"**{doc['title']}**  \n"
                            f"Type: {doc['source_type']} | Score: {doc['score']}  \n"
                            f"{doc['content']}"
                        )

                with right_col:
                    st.subheader("Warehouse Facts")
                    for fact in result.get("warehouse_facts", []):
                        st.markdown(
                            f"**{fact['metric']}**: {fact['value']}  \n"
                            f"Source: {fact['source']}"
                        )

                st.subheader("Reasoning Trace")
                for step in result.get("reasoning_trace", []):
                    st.write(f"- {step}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI server. Start `api.py` on port 8000.")
            except requests.exceptions.HTTPError as exc:
                st.error(f"API error: {exc}")

st.subheader("System Evaluation And Monitoring")
monitor_left, monitor_right = st.columns(2)

with monitor_left:
    if st.button("Check Health"):
        try:
            health = requests.get(f"{api_url}/health", timeout=30).json()
            st.json(health)
        except requests.exceptions.RequestException as exc:
            st.error(f"Health check failed: {exc}")

    if st.button("Show Metrics"):
        try:
            metrics = requests.get(f"{api_url}/metrics", timeout=30).json()
            st.json(metrics)
        except requests.exceptions.RequestException as exc:
            st.error(f"Metrics request failed: {exc}")

with monitor_right:
    if st.button("Run Sample Evaluation"):
        try:
            evaluation = requests.get(f"{api_url}/evaluation", timeout=60).json()
            st.json(evaluation)
        except requests.exceptions.RequestException as exc:
            st.error(f"Evaluation request failed: {exc}")

st.subheader("Logging, Debugging, And Stability")
st.markdown(
    "\n".join(
        [
            "- Request logging is enabled in the FastAPI backend with per-request IDs.",
            "- Rotating application logs are written to `logs/application.log`.",
            "- The `/metrics` endpoint summarizes request count, errors, fallback usage, and average latency.",
            "- The `/health` endpoint reports model readiness, knowledge-base readiness, and Snowflake configuration.",
            "- If the adapted model or Snowflake are unavailable, the app remains stable by using grounded fallback behavior.",
        ]
    )
)
