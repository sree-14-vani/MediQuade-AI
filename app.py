
import os
from typing import Any

import requests
import streamlit as st


# ============================================================
# MediQuade AI - Streamlit Frontend
# Qwen3-4B + QLoRA model runs on Google Colab using FastAPI.
# ============================================================

st.set_page_config(
    page_title="MediQuade AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ---------------------- API CONFIGURATION --------------------

def read_setting(name: str) -> str:
    """Read settings from Streamlit Secrets or environment variables."""
    value = ""

    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""

    return str(value or os.getenv(name, "")).strip()


API_URL = read_setting("API_URL").rstrip("/")
API_KEY = read_setting("API_KEY")

# Remove /ask if it was accidentally included in API_URL.
if API_URL.endswith("/ask"):
    API_URL = API_URL[:-4].rstrip("/")

API_ENDPOINT = f"{API_URL}/ask" if API_URL else ""


# ---------------------- SESSION STATE ------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------- PROFESSIONAL UI ----------------------

st.markdown(
    """
    <style>
    :root {
        --mq-navy: #123B50;
        --mq-teal: #159D98;
        --mq-bg: #F4F8FA;
        --mq-border: #D6E4E9;
    }

    .stApp {
        background: var(--mq-bg);
    }

    [data-testid="stHeader"] {
        background: rgba(244,248,250,0.96);
    }

    .block-container {
        max-width: 900px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    .mq-hero {
        background: var(--mq-navy);
        color: white;
        padding: 1.4rem 1.5rem;
        border-radius: 16px;
        border-bottom: 5px solid var(--mq-teal);
        margin-bottom: 1rem;
    }

    .mq-hero h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 750;
    }

    .mq-hero p {
        color: #E8F4F5;
        margin-top: 0.45rem;
        font-size: 1rem;
    }

    div[data-testid="stChatMessage"] {
        background: white;
        border: 1px solid var(--mq-border);
        border-radius: 13px;
        padding: 0.65rem 0.85rem;
    }

    div.stButton > button {
        background: var(--mq-navy);
        color: white;
        border: 1px solid var(--mq-navy);
        border-radius: 9px;
        min-height: 2.55rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background: var(--mq-teal);
        color: white;
        border-color: var(--mq-teal);
    }

    .mq-footer {
        color: var(--mq-navy);
        border-top: 1px solid var(--mq-border);
        padding-top: 0.9rem;
        margin-top: 2rem;
        font-size: 0.84rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------- HEADER -------------------------------

st.markdown(
    """
    <div class="mq-hero">
        <h1>🩺 MediQuade AI</h1>
        <p>Your AI-powered medical information and learning assistant</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "MediQuade AI provides educational information only. "
    "It cannot diagnose medical conditions or prescribe medicines. "
    "Consult a qualified healthcare professional for personal "
    "medical concerns. Seek urgent medical care for emergencies."
)


# ---------------------- SIDEBAR ------------------------------

with st.sidebar:

    st.markdown("## About MediQuade AI")

    st.write("**Base model:** Qwen3-4B")
    st.write("**Fine-tuning:** QLoRA")
    st.write("**Training dataset:** MedQuAD")

    st.divider()

    if API_URL and API_KEY:
        st.success("Backend settings configured")
    elif not API_URL:
        st.error("Backend URL is missing")
    else:
        st.error("Backend API key is missing")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption(
        "Avoid entering names, phone numbers, addresses, "
        "or confidential medical records."
    )


# ---------------------- CONFIGURATION NOTICE -----------------

if not API_URL or not API_KEY:

    st.warning(
        "Backend settings are incomplete. "
        "Add API_URL and API_KEY in your Streamlit app's "
        "Settings → Secrets."
    )

    st.code(
        'API_URL = "https://YOUR-CURRENT-TUNNEL.trycloudflare.com"\n'
        'API_KEY = "YOUR_COLAB_API_KEY"',
        language="toml",
    )


# ---------------------- CHAT HISTORY -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------- USER QUESTION ------------------------

question = st.chat_input(
    "Ask a medical or health-science question..."
)


if question is not None:

    question = question.strip()

    if not question:
        st.warning("Please type a question.")

    elif len(question) > 4000:
        st.error("Please keep your question within 4,000 characters.")

    elif not API_URL or not API_KEY:
        st.error(
            "Backend settings are missing. "
            "Configure API_URL and API_KEY in Streamlit Secrets."
        )

    else:

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "MediQuade AI is preparing your answer..."
            ):

                try:

                    response = requests.post(
                        API_ENDPOINT,
                        json={"question": question},
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json",
                        },
                        timeout=(20, 300),
                    )

                    if not response.ok:

                        try:
                            error_data: Any = response.json()

                            detail = (
                                error_data.get("detail", response.text)
                                if isinstance(error_data, dict)
                                else response.text
                            )

                        except ValueError:
                            detail = response.text or "No error details returned."

                        st.error(
                            f"Backend error (HTTP {response.status_code}): "
                            f"{detail}"
                        )

                    else:

                        try:
                            data: Any = response.json()
                        except ValueError:
                            data = None

                        if not isinstance(data, dict):

                            st.error(
                                "The backend did not return valid JSON. "
                                "Check your FastAPI server."
                            )

                        else:

                            answer = data.get("answer", "")

                            if not isinstance(answer, str) or not answer.strip():

                                detail = data.get(
                                    "detail",
                                    "The backend returned an empty answer."
                                )

                                st.error(str(detail))

                            else:

                                answer = answer.strip()

                                st.markdown(answer)

                                st.session_state.messages.append(
                                    {
                                        "role": "assistant",
                                        "content": answer
                                    }
                                )

                except requests.exceptions.Timeout:

                    st.error(
                        "The backend took too long to respond. "
                        "Check that Colab and the model are still running."
                    )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to the backend. "
                        "Check Colab and update API_URL with the "
                        "latest Cloudflare tunnel URL."
                    )

                except requests.exceptions.RequestException as exc:

                    st.error(f"Network request failed: {exc}")


# ---------------------- FOOTER -------------------------------

st.markdown(
    """
    <div class="mq-footer">
        <strong>MediQuade AI</strong> · Qwen3-4B · QLoRA · MedQuAD<br>
        Educational information only — not a substitute for
        professional medical care.
    </div>
    """,
    unsafe_allow_html=True,
)
