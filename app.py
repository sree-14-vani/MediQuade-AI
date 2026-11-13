
import os
from typing import Any

import requests
import streamlit as st


# ============================================================
# MEDIQUADE AI - FRONTEND
# Qwen3-4B + QLoRA inference runs through FastAPI in Colab.
# ============================================================

st.set_page_config(
    page_title="MediQuade AI",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------- API CONFIGURATION ----------------------

def get_setting(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""

    return str(value or os.getenv(name, "")).strip()


API_URL = get_setting("API_URL").rstrip("/")
API_KEY = get_setting("API_KEY")

# Accept both base URL and full /ask URL.
if API_URL.endswith("/ask"):
    API_URL = API_URL[:-4].rstrip("/")

API_ENDPOINT = f"{API_URL}/ask" if API_URL else ""


# ------------------------ SESSION STATE -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""


# ----------------------------- CSS -----------------------------

st.markdown(
    """
    <style>

    :root {
        color-scheme: light;
        --navy: #12344A;
        --white: #FFFFFF;
    }

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background: #FFFFFF !important;
        color: #12344A !important;
    }

    [data-testid="stHeader"] {
        background: #FFFFFF !important;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    .block-container {
        max-width: 1100px !important;
        padding: 1.5rem 1.5rem 7rem 1.5rem !important;
    }

    /* HEADER */

    .mq-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
        background: #12344A;
        color: #FFFFFF !important;
        padding: 20px 24px;
        border-radius: 17px;
        margin-bottom: 20px;
    }

    .mq-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .mq-logo {
        width: 50px;
        height: 50px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #FFFFFF;
        color: #12344A !important;
        border-radius: 13px;
        font-size: 26px;
        font-weight: 850;
    }

    .mq-title {
        color: #FFFFFF !important;
        font-size: 26px;
        font-weight: 800;
        line-height: 1.2;
    }

    .mq-subtitle {
        color: #FFFFFF !important;
        font-size: 13px;
        margin-top: 5px;
    }

    .mq-tag {
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF;
        padding: 9px 14px;
        border-radius: 30px;
        font-size: 11px;
        font-weight: 750;
        white-space: nowrap;
    }

    /* WELCOME SECTION */

    .mq-welcome {
        border: 1.5px solid #12344A;
        border-radius: 16px;
        padding: 25px;
        margin: 10px 0 18px 0;
        background: #FFFFFF;
    }

    .mq-label {
        color: #12344A !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.3px;
        margin-bottom: 9px;
    }

    .mq-welcome-title {
        color: #12344A !important;
        font-size: 26px;
        font-weight: 800;
        line-height: 1.3;
        margin-bottom: 8px;
    }

    .mq-description {
        color: #12344A !important;
        font-size: 14px;
        line-height: 1.7;
    }

    .mq-section {
        color: #12344A !important;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 20px 0 10px 0;
    }

    /* BUTTONS */

    div.stButton > button {
        background: #FFFFFF !important;
        color: #12344A !important;
        border: 1.5px solid #12344A !important;
        border-radius: 11px !important;
        min-height: 44px !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }

    div.stButton > button p,
    div.stButton > button span {
        color: #12344A !important;
    }

    div.stButton > button:hover {
        background: #12344A !important;
        border-color: #12344A !important;
    }

    div.stButton > button:hover p,
    div.stButton > button:hover span {
        color: #FFFFFF !important;
    }

    /* CHAT MESSAGES */

    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border: 1.4px solid #12344A !important;
        border-radius: 14px !important;
        padding: 15px 18px !important;
        margin: 12px 0 !important;
        box-shadow: none !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3 {
        color: #12344A !important;
        opacity: 1 !important;
        line-height: 1.7 !important;
    }

    /* Hide default chat avatars */

    [data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* CHAT INPUT */

    [data-testid="stChatInput"] {
        background: #FFFFFF !important;
        border: 1.5px solid #12344A !important;
        border-radius: 14px !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus {
        background: #FFFFFF !important;
        color: #12344A !important;
        -webkit-text-fill-color: #12344A !important;
        caret-color: #12344A !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #12344A !important;
        -webkit-text-fill-color: #12344A !important;
        opacity: 0.7 !important;
    }

    [data-testid="stChatInput"] button {
        background: #12344A !important;
        border: 1px solid #12344A !important;
        border-radius: 10px !important;
    }

    [data-testid="stChatInput"] button svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* ALERTS */

    [data-testid="stAlert"] {
        background: #FFFFFF !important;
        border: 1px solid #12344A !important;
        border-radius: 11px !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: #12344A !important;
    }

    /* FOOTER */

    .mq-footer {
        border-top: 1px solid #12344A;
        padding-top: 12px;
        margin-top: 25px;
        text-align: center;
        color: #12344A !important;
        font-size: 11px;
        line-height: 1.6;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    /* MOBILE RESPONSIVENESS */

    @media (max-width: 700px) {

        .block-container {
            padding: 0.8rem 0.7rem 6rem 0.7rem !important;
        }

        .mq-header {
            padding: 14px;
        }

        .mq-title {
            font-size: 20px;
        }

        .mq-logo {
            width: 42px;
            height: 42px;
        }

        .mq-tag {
            display: none;
        }

        .mq-welcome {
            padding: 17px;
        }

        .mq-welcome-title {
            font-size: 21px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------- HEADER ----------------------------

st.markdown(
    """
    <div class="mq-header">

        <div class="mq-brand">

            <div class="mq-logo">M</div>

            <div>
                <div class="mq-title">MediQuade AI</div>
                <div class="mq-subtitle">
                    Medical knowledge, made easier to understand.
                </div>
            </div>

        </div>

        <div class="mq-tag">
            AI HEALTH ASSISTANT
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------------- CHAT CONTROLS -------------------------

col1, col2, col3 = st.columns([1.2, 1.2, 5])

with col1:
    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = ""
        st.rerun()

with col2:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = ""
        st.rerun()


# --------------------------- WELCOME PAGE -------------------------

if not st.session_state.messages:

    st.markdown(
        """
        <div class="mq-welcome">

            <div class="mq-label">
                WELCOME TO MEDIQUADE
            </div>

            <div class="mq-welcome-title">
                What would you like to understand today?
            </div>

            <div class="mq-description">
                Ask a health or medical science question and
                receive a clear explanation from MediQuade AI.
            </div>

        </div>

        <div class="mq-section">
            SUGGESTED QUESTIONS
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggestions = [
        "What are the common symptoms of diabetes?",
        "What is the difference between bacteria and viruses?",
        "How does high blood pressure affect the body?",
    ]

    suggestion_cols = st.columns(3)

    for index, suggestion in enumerate(suggestions):

        with suggestion_cols[index]:

            if st.button(
                suggestion,
                key=f"suggestion_{index}",
                use_container_width=True,
            ):

                st.session_state.pending_question = suggestion
                st.rerun()


# --------------------------- CHAT HISTORY -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"], avatar=None):
        st.markdown(message["content"])


# ----------------------------- INPUT ------------------------------

typed_question = st.chat_input(
    "Ask MediQuade AI a medical question..."
)

pending_question = st.session_state.pending_question
st.session_state.pending_question = ""

question = pending_question or typed_question


# ------------------------- BACKEND REQUEST ------------------------

if question:

    question = question.strip()

    if not question:
        st.warning("Please enter a question.")

    elif len(question) > 4000:
        st.error("Please keep your question within 4,000 characters.")

    elif not API_ENDPOINT or not API_KEY:

        st.error(
            "Backend is not configured. Add API_URL and API_KEY "
            "in Streamlit Community Cloud → App settings → Secrets."
        )

    else:

        # Save the user question once.
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        answer = ""
        error_message = ""

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
                            detail = error_data.get(
                                "detail",
                                response.text
                            )
                        else:
                            detail = response.text

                    except ValueError:
                        detail = response.text or "Unknown backend error."

                    if response.status_code in (401, 403):

                        error_message = (
                            "Invalid API key. Check API_KEY in "
                            "Streamlit Secrets and your current Colab key."
                        )

                    else:

                        error_message = (
                            f"Backend error (HTTP {response.status_code}): "
                            f"{detail}"
                        )

                else:

                    try:
                        data: Any = response.json()
                    except ValueError:
                        data = None

                    if not isinstance(data, dict):

                        error_message = (
                            "Invalid backend response. Check the FastAPI /ask endpoint."
                        )

                    else:

                        answer_value = data.get("answer", "")

                        if (
                            isinstance(answer_value, str)
                            and answer_value.strip()
                        ):
                            answer = answer_value.strip()

                        else:
                            error_message = str(
                                data.get(
                                    "detail",
                                    "The backend returned an empty answer."
                                )
                            )

            except requests.exceptions.Timeout:

                error_message = (
                    "Request timed out. Check whether Colab, FastAPI "
                    "and Cloudflare Tunnel are running."
                )

            except requests.exceptions.ConnectionError:

                error_message = (
                    "Cannot connect to the backend. Check Colab and "
                    "update API_URL with the latest Cloudflare URL."
                )

            except requests.exceptions.RequestException as exc:

                error_message = f"Request failed: {exc}"

        # Save the answer or error once.
        if answer:

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        else:

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"**Unable to answer:** {error_message}"
                }
            )

        # Rerender the complete conversation from session state.
        st.rerun()


# ------------------------------ FOOTER ----------------------------

st.markdown(
    """
    <div class="mq-footer">
        MediQuade AI provides educational information and is not
        a substitute for professional medical advice, diagnosis, or treatment.
    </div>
    """,
    unsafe_allow_html=True,
)
