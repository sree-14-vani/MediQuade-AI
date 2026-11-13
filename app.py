import os
from typing import Any

import requests
import streamlit as st


# --------------------------- Page setup ---------------------------
st.set_page_config(
    page_title="MediQuade AI",
    page_icon="M",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ------------------------- Backend settings -----------------------
def read_setting(name: str) -> str:
    """Read a setting from Streamlit Secrets or environment variables."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, "")).strip()


API_URL = read_setting("API_URL").rstrip("/")
API_KEY = read_setting("API_KEY")

# Accept either the base tunnel URL or a URL ending in /ask.
if API_URL.endswith("/ask"):
    API_URL = API_URL[:-4].rstrip("/")

API_ENDPOINT = f"{API_URL}/ask" if API_URL else ""


# ---------------------------- Chat state --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------ Styling ---------------------------
# Strict two-colour palette: navy and white. Force a light, readable
# interface even when the viewer's Streamlit/browser theme is dark.
st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
        --mq-navy: #17364D;
        --mq-white: #FFFFFF;
        --primary-color: #17364D;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp,
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
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

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    .mq-heading {
        padding: 0 0 1.1rem 0;
        margin-bottom: 1.25rem;
        border-bottom: 2px solid var(--mq-navy);
    }

    .mq-heading h1 {
        color: var(--mq-navy) !important;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
    }

    .mq-heading p {
        color: var(--mq-navy) !important;
        font-size: 0.98rem;
        margin: 0.4rem 0 0 0;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--mq-white) !important;
        border: 1px solid var(--mq-navy) !important;
        border-radius: 12px !important;
        margin-bottom: 0.75rem !important;
    }

    .mq-role {
        color: var(--mq-navy) !important;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }

    [data-testid="stChatInput"] {
        background: var(--mq-white) !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stTextArea"] textarea,
    input {
        background: var(--mq-white) !important;
        color: var(--mq-navy) !important;
        -webkit-text-fill-color: var(--mq-navy) !important;
        caret-color: var(--mq-navy) !important;
        border: 1px solid var(--mq-navy) !important;
        border-radius: 10px !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--mq-navy) !important;
        -webkit-text-fill-color: var(--mq-navy) !important;
        opacity: 0.75 !important;
    }

    div.stButton > button,
    [data-testid="stChatInput"] button {
        background: var(--mq-navy) !important;
        color: var(--mq-white) !important;
        border: 1px solid var(--mq-navy) !important;
        border-radius: 9px !important;
        font-weight: 650 !important;
    }

    div.stButton > button p,
    div.stButton > button span,
    [data-testid="stChatInput"] button svg {
        color: var(--mq-white) !important;
        fill: var(--mq-white) !important;
    }

    div.stButton > button:hover,
    [data-testid="stChatInput"] button:hover {
        background: var(--mq-white) !important;
        color: var(--mq-navy) !important;
    }

    div.stButton > button:hover p,
    div.stButton > button:hover span {
        color: var(--mq-navy) !important;
    }

    [data-testid="stAlert"] {
        background: var(--mq-white) !important;
        border: 1px solid var(--mq-navy) !important;
        color: var(--mq-navy) !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: var(--mq-navy) !important;
    }

    #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------- Header ---------------------------
header_left, header_right = st.columns([5, 1], vertical_alignment="center")
with header_left:
    st.markdown(
        """
        <div class="mq-heading">
            <h1>MediQuade AI</h1>
            <p>Medical information assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ------------------------- Missing configuration ------------------
if not API_URL or not API_KEY:
    st.error(
        "Backend settings are missing. Add API_URL and API_KEY in "
        "Streamlit Community Cloud → App settings → Secrets."
    )


# --------------------------- Message display ----------------------
def render_message(role: str, content: str) -> None:
    """Display a readable message card without coloured avatar icons."""
    label = "YOU" if role == "user" else "MEDIQUADE AI"
    with st.container(border=True):
        st.markdown(
            f'<div class="mq-role">{label}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(content)


# --------------------------- Message history ----------------------
for message in st.session_state.messages:
    render_message(message["role"], message["content"])


# ----------------------------- Chat input -------------------------
question = st.chat_input("Type your medical question here...")

if question is not None:
    question = question.strip()

    if not question:
        st.warning("Please enter a question.")
    elif len(question) > 4000:
        st.error("Please keep your question within 4,000 characters.")
    elif not API_URL or not API_KEY:
        st.error("Configure API_URL and API_KEY in Streamlit Secrets first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})

        render_message("user", question)

        with st.container(border=True):
            st.markdown(
                '<div class="mq-role">MEDIQUADE AI</div>',
                unsafe_allow_html=True,
            )
            with st.spinner("Preparing your answer..."):
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
                        st.error(f"Backend error (HTTP {response.status_code}): {detail}")
                    else:
                        try:
                            data: Any = response.json()
                        except ValueError:
                            data = None

                        if not isinstance(data, dict):
                            st.error("The backend returned an invalid response. Check FastAPI.")
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
                    st.error(
                        "The request timed out. Check that the Colab model and API are running."
                    )
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot reach the backend. Check Colab and update API_URL with "
                        "the current Cloudflare tunnel URL."
                    )
                except requests.exceptions.RequestException as exc:
                    st.error(f"Request failed: {exc}")


# Small, unobtrusive medical safety note.
st.caption("For educational purposes only. Not a medical diagnosis or treatment.")
