import os
from typing import Any, Dict, List

import requests
import streamlit as st


# ================================================================
# MediQuade AI | Streamlit frontend
# Frontend only: Qwen3-4B + QLoRA inference is served by FastAPI
# from the Google Colab backend through the Cloudflare tunnel.
# ================================================================

st.set_page_config(
    page_title="MediQuade AI",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------- Configuration -----------------------
def get_setting(name: str) -> str:
    """Read a setting from Streamlit Secrets, then environment variables."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, "")).strip()


API_URL = get_setting("API_URL").rstrip("/")
API_KEY = get_setting("API_KEY")

# Allow either the tunnel's base URL or the full /ask endpoint.
if API_URL.endswith("/ask"):
    API_URL = API_URL[:-4].rstrip("/")

API_ENDPOINT = f"{API_URL}/ask" if API_URL else ""


# ---------------------------- Session state ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""


# ------------------------------- Design --------------------------
# Deliberately restricted to two colours: navy and white.
# The CSS also overrides dark browser/Streamlit themes so all text
# and controls remain legible in Streamlit Community Cloud.
st.markdown(
    r"""
    <style>
    :root {
        color-scheme: light;
        --mq-navy: #12344A;
        --mq-white: #FFFFFF;
    }

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background: var(--mq-white) !important;
        color: var(--mq-navy) !important;
    }

    html, body, p, span, label, li, h1, h2, h3, h4, strong,
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    [data-testid="stCaptionContainer"],
    [data-testid="stChatMessage"] * {
        color: var(--mq-navy) !important;
        opacity: 1 !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: var(--mq-white) !important;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    .block-container {
        max-width: 1120px !important;
        padding: 2rem 2.2rem 7rem 2.2rem !important;
    }

    /* Brand header */
    .mq-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        background: var(--mq-navy);
        color: var(--mq-white) !important;
        border-radius: 20px;
        padding: 1.35rem 1.55rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 28px rgba(18, 52, 74, 0.14);
    }

    .mq-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
        min-width: 0;
    }

    .mq-mark {
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 0 0 54px;
        width: 54px;
        height: 54px;
        border: 2px solid var(--mq-white);
        border-radius: 15px;
        color: var(--mq-navy) !important;
        background: var(--mq-white);
        font-size: 1.65rem;
        font-weight: 850;
        letter-spacing: -0.06em;
    }

    .mq-brand-title {
        color: var(--mq-white) !important;
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.035em;
        margin: 0;
    }

    .mq-brand-subtitle {
        color: var(--mq-white) !important;
        font-size: 0.92rem;
        font-weight: 450;
        margin-top: 0.35rem;
        opacity: 1 !important;
    }

    .mq-header-tag {
        color: var(--mq-white) !important;
        border: 1px solid var(--mq-white);
        border-radius: 999px;
        padding: 0.48rem 0.85rem;
        font-size: 0.73rem;
        font-weight: 750;
        letter-spacing: 0.08em;
        white-space: nowrap;
    }

    /* Welcome surface */
    .mq-welcome {
        background: var(--mq-white);
        border: 1.5px solid var(--mq-navy);
        border-radius: 20px;
        padding: 1.65rem 1.8rem 1.45rem 1.8rem;
        margin: 0.25rem 0 1.35rem 0;
    }

    .mq-welcome-kicker {
        color: var(--mq-navy) !important;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin-bottom: 0.6rem;
    }

    .mq-welcome h2 {
        color: var(--mq-navy) !important;
        font-size: 1.65rem;
        font-weight: 800;
        line-height: 1.25;
        letter-spacing: -0.03em;
        margin: 0 0 0.55rem 0;
    }

    .mq-welcome p {
        color: var(--mq-navy) !important;
        font-size: 0.98rem;
        line-height: 1.65;
        margin: 0;
    }

    .mq-section-label {
        color: var(--mq-navy) !important;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.09em;
        margin: 1.15rem 0 0.65rem 0;
    }

    /* Suggestion buttons */
    div.stButton > button {
        background: var(--mq-white) !important;
        color: var(--mq-navy) !important;
        border: 1.5px solid var(--mq-navy) !important;
        border-radius: 13px !important;
        min-height: 3rem !important;
        padding: 0.65rem 0.9rem !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        transition: transform 120ms ease, box-shadow 120ms ease;
    }

    div.stButton > button p,
    div.stButton > button span {
        color: var(--mq-navy) !important;
        font-weight: 700 !important;
    }

    div.stButton > button:hover {
        background: var(--mq-navy) !important;
        border-color: var(--mq-navy) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(18, 52, 74, 0.14) !important;
    }

    div.stButton > button:hover p,
    div.stButton > button:hover span {
        color: var(--mq-white) !important;
    }

    /* Clear-chat button uses the same restrained palette. */
    .mq-clear-help {
        color: var(--mq-navy) !important;
        font-size: 0.78rem;
        text-align: right;
        margin-top: -0.2rem;
    }

    /* Conversation messages */
    [data-testid="stChatMessage"] {
        background: var(--mq-white) !important;
        border: 1.5px solid var(--mq-navy) !important;
        border-radius: 17px !important;
        padding: 1rem 1.15rem !important;
        margin: 0.7rem 0 !important;
        box-shadow: 0 5px 16px rgba(18, 52, 74, 0.06) !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] code {
        color: var(--mq-navy) !important;
        line-height: 1.7 !important;
        opacity: 1 !important;
    }

    /* Native Streamlit chat input */
    [data-testid="stChatInput"] {
        background: var(--mq-white) !important;
        border: 1.5px solid var(--mq-navy) !important;
        border-radius: 17px !important;
        box-shadow: 0 8px 24px rgba(18, 52, 74, 0.13) !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus {
        background: var(--mq-white) !important;
        color: var(--mq-navy) !important;
        -webkit-text-fill-color: var(--mq-navy) !important;
        caret-color: var(--mq-navy) !important;
        opacity: 1 !important;
        font-size: 1rem !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--mq-navy) !important;
        -webkit-text-fill-color: var(--mq-navy) !important;
        opacity: 0.72 !important;
    }

    [data-testid="stChatInput"] button {
        background: var(--mq-navy) !important;
        border: 1px solid var(--mq-navy) !important;
        border-radius: 11px !important;
    }

    [data-testid="stChatInput"] button svg {
        color: var(--mq-white) !important;
        fill: var(--mq-white) !important;
    }

    /* Alerts and status text */
    [data-testid="stAlert"] {
        background: var(--mq-white) !important;
        border: 1.5px solid var(--mq-navy) !important;
        border-radius: 13px !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: var(--mq-navy) !important;
        opacity: 1 !important;
    }

    .mq-footnote {
        color: var(--mq-navy) !important;
        border-top: 1px solid var(--mq-navy);
        padding-top: 0.9rem;
        margin-top: 1.6rem;
        font-size: 0.78rem;
        line-height: 1.5;
    }

    #MainMenu, footer { visibility: hidden; }

    @media (max-width: 700px) {
        .block-container {
            padding: 1rem 0.8rem 6.5rem 0.8rem !important;
        }
        .mq-header {
            padding: 1rem;
            border-radius: 15px;
        }
        .mq-brand-title { font-size: 1.35rem; }
        .mq-mark {
            flex-basis: 45px;
            width: 45px;
            height: 45px;
            border-radius: 12px;
        }
        .mq-header-tag { display: none; }
        .mq-welcome { padding: 1.2rem; }
        .mq-welcome h2 { font-size: 1.35rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------- Header --------------------------
header_col, action_col = st.columns([5.5, 1.25], vertical_alignment="center")
with header_col:
    st.markdown(
        """
        <div class="mq-header">
            <div class="mq-brand">
                <div class="mq-mark">M</div>
                <div>
                    <div class="mq-brand-title">MediQuade AI</div>
                    <div class="mq-brand-subtitle">Medical knowledge, made easier to understand.</div>
                </div>
            </div>
            <div class="mq-header-tag">AI ASSISTANT</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with action_col:
    if st.button("＋  New chat", key="new_chat_button", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = ""
        st.rerun()


# ---------------------------- Welcome area -----------------------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="mq-welcome">
            <div class="mq-welcome-kicker">WELCOME TO MEDIQUADE</div>
            <h2>What would you like to understand today?</h2>
            <p>Ask a health or medical science question. Get a clear, structured explanation from MediQuade AI.</p>
        </div>
        <div class="mq-section-label">START WITH A TOPIC</div>
        """,
        unsafe_allow_html=True,
    )

    prompt_cols = st.columns(3)
    suggested_prompts = [
        "What are the common symptoms of diabetes?",
        "Explain how blood pressure works.",
        "What is the difference between bacteria and viruses?",
    ]

    for col, prompt in zip(prompt_cols, suggested_prompts):
        with col:
            if st.button(prompt, key=f"suggest_{suggested_prompts.index(prompt)}", use_container_width=True):
                st.session_state.pending_question = prompt
                st.rerun()


# --------------------------- Conversation ------------------------
def show_message(role: str, content: str) -> None:
    """Render one conversation message using Streamlit's accessible chat UI."""
    avatar = "Y" if role == "user" else "M"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)


for item in st.session_state.messages:
    show_message(item["role"], item["content"])


# ------------------------------ Input ----------------------------
typed_question = st.chat_input("Write your medical question here...")
prompt_question = st.session_state.pending_question
st.session_state.pending_question = ""
question = prompt_question or typed_question


# --------------------------- Backend request ---------------------
if question:
    question = question.strip()

    if not question:
        st.warning("Please enter a question.")
    elif len(question) > 4000:
        st.error("Please keep your question within 4,000 characters.")
    elif not API_ENDPOINT or not API_KEY:
        st.error(
            "The backend is not configured. Add API_URL and API_KEY in "
            "Streamlit Community Cloud → App settings → Secrets."
        )
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        show_message("user", question)

        with st.chat_message("assistant", avatar="M"):
            with st.spinner("MediQuade AI is preparing your answer..."):
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
                            if isinstance(error_data, dict):
                                detail = error_data.get("detail", response.text)
                            else:
                                detail = response.text
                        except ValueError:
                            detail = response.text or "No additional error details were returned."

                        if response.status_code == 401 or response.status_code == 403:
                            st.error("The backend rejected the API key. Check API_KEY in Streamlit Secrets.")
                        else:
                            st.error(f"Backend error (HTTP {response.status_code}): {detail}")

                    else:
                        try:
                            data: Any = response.json()
                        except ValueError:
                            data = None

                        if not isinstance(data, dict):
                            st.error("The backend returned an invalid response. Check the FastAPI /ask endpoint.")
                        else:
                            answer = data.get("answer", "")

                            if not isinstance(answer, str) or not answer.strip():
                                detail = data.get("detail", "The backend returned an empty answer.")
                                st.error(str(detail))
                            else:
                                answer = answer.strip()
                                st.markdown(answer)
                                st.session_state.messages.append(
                                    {"role": "assistant", "content": answer}
                                )

                except requests.exceptions.Timeout:
                    st.error("The response timed out. Check that the Colab model and FastAPI server are still running.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to the backend. Check Colab and update API_URL with the current Cloudflare tunnel URL.")
                except requests.exceptions.RequestException as exc:
                    st.error(f"The request could not be completed: {exc}")


# ------------------------------- Footer --------------------------
st.markdown(
    """
    <div class="mq-footnote">
        MediQuade AI provides educational information and is not a substitute for professional medical advice.
    </div>
    """,
    unsafe_allow_html=True,
)
