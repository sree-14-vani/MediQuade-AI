
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="MediQuade AI",
    page_icon="🩺",
    layout="centered"
)

# API configuration
API_URL = st.secrets.get(
    "MEDIQUADE_API_URL",
    os.getenv("MEDIQUADE_API_URL", "")
)

API_KEY = st.secrets.get(
    "MEDIQUADE_API_KEY",
    os.getenv("MEDIQUADE_API_KEY", "")
)

SYSTEM_TITLE = "MediQuade AI"

st.title("🩺 MediQuade AI")
st.subheader("Your AI-powered medical learning assistant")
st.caption(
    "Ask general educational questions about medical concepts and health."
)

with st.expander("Important medical disclaimer"):
    st.warning(
        "This application provides educational information only. "
        "It does not provide diagnosis, prescriptions, or personalized "
        "treatment. Consult a qualified healthcare professional."
    )

with st.sidebar:
    st.markdown("### Model information")
    st.write("Base model: Qwen3-4B")
    st.write("Fine-tuning: QLoRA / LoRA")
    st.write("Quantization: 4-bit NF4")
    st.write("Inference: Separate GPU server")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not API_URL or not API_KEY:
    st.error("Inference API is not configured.")
    st.info(
        "Add MEDIQUADE_API_URL and MEDIQUADE_API_KEY "
        "in Streamlit Cloud Secrets."
    )
    st.stop()

# Check backend connection
try:
    response = requests.get(
        f"{API_URL.rstrip('/')}/health",
        timeout=15
    )
    response.raise_for_status()
    st.success("MediQuade AI inference server connected.")
except requests.RequestException:
    st.error(
        "GPU inference server is unavailable. "
        "Start your Colab inference server and try again."
    )

# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User question
question = st.chat_input("Ask your medical question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("MediQuade AI is preparing your answer..."):
            try:
                response = requests.post(
                    f"{API_URL.rstrip('/')}/ask",
                    headers={
                        "Authorization": f"Bearer {API_KEY}"
                    },
                    json={"question": question},
                    timeout=180
                )

                response.raise_for_status()
                answer = response.json().get("answer", "")

                if not answer:
                    answer = "No answer was generated. Please try again."

                st.markdown(answer)

            except requests.Timeout:
                answer = "The model took too long to respond. Please try again."
                st.error(answer)

            except requests.RequestException as exc:
                answer = "Unable to connect to the inference server."
                st.error(answer)
                st.caption(str(exc))

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
