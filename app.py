
import os
import uuid
from typing import Any

import requests
import streamlit as st


# ================================================================
# MediQuade AI | Streamlit Frontend
# Qwen3-4B + QLoRA backend through FastAPI and Cloudflare Tunnel
# ================================================================

st.set_page_config(
    page_title="MediQuade AI",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------- Configuration -----------------------

def get_setting(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, "")).strip()


API_URL = get_setting("API_URL").rstrip("/")
API_KEY = get_setting("API_KEY")

if API_URL.endswith("/ask"):
    API_URL = API_URL[:-4].rstrip("/")

API_ENDPOINT = f"{API_URL}/ask" if API_URL else ""


# ---------------------------- Session State ----------------------

if "chats" not in st.session_state:
    first_chat_id = str(uuid.uuid4())
    st.session_state.chats = [
        {
            "id": first_chat_id,
            "title": "New conversation",
            "messages": [],
        }
    ]
    st.session_state.active_chat_id = first_chat_id

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = st.session_state.chats[0]["id"]

if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""

if "confirm_clear_all" not in st.session_state:
    st.session_state.confirm_clear_all = False


def get_active_chat():
    """Return the currently selected conversation."""
    for chat in st.session_state.chats:
        if chat["id"] == st.session_state.active_chat_id:
            return chat

    # Recover safely if the selected chat no longer exists.
    new_chat = {
        "id": str(uuid.uuid4()),
        "title": "New conversation",
        "messages": [],
    }
    st.session_state.chats.append(new_chat)
    st.session_state.active_chat_id = new_chat["id"]
    return new_chat


def create_new_chat():
    """Create and select a new conversation."""
    new_chat = {
        "id": str(uuid.uuid4()),
        "title": "New conversation",
        "messages": [],
    }
    st.session_state.chats.insert(0, new_chat)
    st.session_state.active_chat_id = new_chat["id"]
    st.session_state.pending_question = ""
    st.session_state.confirm_clear_all = False


def clear_current_chat():
    """Clear messages in the selected conversation."""
    chat = get_active_chat()
    chat["messages"] = []
    chat["title"] = "New conversation"
    st.session_state.pending_question = ""


def clear_all_history():
    """Remove all conversations and start a fresh one."""
    st.session_state.chats = []
    create_new_chat()
    st.session_state.confirm_clear_all = False


def update_chat_title(chat, question):
    """Use the first question as the conversation title."""
    if chat["title"] == "New conversation":
        title = " ".join(question.split())
        chat["title"] = title[:35] + ("..." if len(title) > 35 else "")


# ------------------------------- Design --------------------------

st.markdown(
    """
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
        background: #FFFFFF !important;
        color: #12344A !important;
    }

    html, body, p, span, label, li, h1, h2, h3, h4, strong,
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    [data-testid="stCaptionContainer"],
    [data-testid="stChatMessage"] * {
        color: #12344A !important;
        opacity: 1 !important;
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        background: #FFFFFF !important;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    .block-container {
        max-width: 1250px !important;
        padding: 1.7rem 1.7rem 5rem 1.7rem !important;
    }

    /* Header */

    .mq-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        background: #12344A;
        color: #FFFFFF !important;
        border-radius: 18px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
    }

    .mq-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .mq-mark {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        flex-shrink: 0;
        border: 2px solid #FFFFFF;
        border-radius: 14px;
        background: #FFFFFF;
        color: #12344A !important;
        font-size: 1.6rem;
        font-weight: 850;
    }

    .mq-brand-title {
        color: #FFFFFF !important;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
    }

    .mq-brand-subtitle {
        color: #FFFFFF !important;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }

    .mq-header-tag {
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF;
        border-radius: 30px;
        padding: 0.45rem 0.8rem;
        font-size: 0.72rem;
        font-weight: 750;
        white-space: nowrap;
    }

    /* History panel */

    .mq-history {
        border: 1.5px solid #12344A;
        border-radius: 16px;
        padding: 1rem;
        background: #FFFFFF;
        margin-bottom: 1rem;
    }

    .mq-history-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #12344A !important;
        margin-bottom: 0.2rem;
    }

    .mq-history-subtitle {
        font-size: 0.78rem;
        color: #12344A !important;
        margin-bottom: 1rem;
    }

    .mq-welcome {
        background: #FFFFFF;
        border: 1.5px solid #12344A;
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.3rem;
    }

    .mq-welcome-kicker {
        color: #12344A !important;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    .mq-welcome h2 {
        color: #12344A !important;
        font-size: 1.55rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
    }

    .mq-welcome p {
        color: #12344A !important;
        line-height: 1.6;
        margin: 0;
    }

    .mq-section-label {
        color: #12344A !important;
        font-size: 0.77rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin: 1rem 0 0.6rem 0;
    }

    /* Buttons */

    div.stButton > button {
        background: #FFFFFF !important;
        color: #12344A !important;
        border: 1.5px solid #12344A !important;
        border-radius: 11px !important;
        min-height: 2.65rem !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }

    div.stButton > button p,
    div.stButton > button span {
        color: #12344A !important;
        font-weight: 700 !important;
    }

    div.stButton > button:hover {
        background: #12344A !important;
        color: #FFFFFF !important;
    }

    div.stButton > button:hover p,
    div.stButton > button:hover span {
        color: #FFFFFF !important;
    }

    /* Chat messages */

    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border: 1.5px solid #12344A !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        margin: 0.65rem 0 !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong {
        color: #12344A !important;
        line-height: 1.7 !important;
    }

    /* Chat input */

    [data-testid="stChatInput"] {
        background: #FFFFFF !important;
        border: 1.5px solid #12344A !important;
        border-radius: 15px !important;
    }

    [data-testid="stChatInput"] textarea {
        background: #FFFFFF !important;
        color: #12344A !important;
        -webkit-text-fill-color: #12344A !important;
        caret-color: #12344A !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #12344A !important;
        opacity: 0.7 !important;
    }

    [data-testid="stChatInput"] button {
        background: #12344A !important;
        border: 1px solid #12344A !important;
    }

    [data-testid="stChatInput"] button svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* Alerts */

    [data-testid="stAlert"] {
        background: #FFFFFF !important;
        border: 1.5px solid #12344A !important;
        border-radius: 12px !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: #12344A !important;
    }

    .mq-footer {
        color: #12344A !important;
        border-top: 1px solid #12344A;
        padding-top: 0.8rem;
        margin-top: 1.5rem;
        font-size: 0.78rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    @media (max-width: 700px) {
        .block-container {
            padding: 1rem 0.7rem 5rem 0.7rem !important;
        }

        .mq-header {
            padding: 1rem;
        }

        .mq-brand-title {
            font-size: 1.3rem;
        }

        .mq-header-tag {
            display: none;
        }

        .mq-welcome {
            padding: 1.1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------- Header --------------------------

st.markdown(
    """
    <div class="mq-header">
        <div class="mq-brand">
            <div class="mq-mark">M</div>
            <div>
                <div class="mq-brand-title">MediQuade AI</div>
                <div class="mq-brand-subtitle">
                    Medical knowledge, made easier to understand.
                </div>
            </div>
        </div>
        <div class="mq-header-tag">AI ASSISTANT</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------------- Main Layout --------------------------

history_col, chat_col = st.columns([1.15, 3.4], gap="large")


# ================================================================
# LEFT PANEL: CHAT HISTORY
# ================================================================

with history_col:

    st.markdown(
        """
        <div class="mq-history">
            <div class="mq-history-title">Chat History</div>
            <div class="mq-history-subtitle">
                Open your previous conversations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "＋  New Chat",
        key="new_chat_button",
        use_container_width=True,
    ):
        create_new_chat()
        st.rerun()

    st.markdown(
        '<div class="mq-section-label">YOUR CONVERSATIONS</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.chats:
        st.caption("No conversations yet.")

    for chat in st.session_state.chats:
        is_active = chat["id"] == st.session_state.active_chat_id

        button_title = chat["title"]

        if is_active:
            button_title = "▶  " + button_title

        if st.button(
            button_title,
            key=f"history_{chat['id']}",
            use_container_width=True,
        ):
            st.session_state.active_chat_id = chat["id"]
            st.session_state.pending_question = ""
            st.rerun()

    st.markdown("---")

    # Clear current conversation
    if st.button(
        "Clear Current Chat",
        key="clear_current",
        use_container_width=True,
    ):
        clear_current_chat()
        st.rerun()

    # Clear all history with confirmation
    if st.button(
        "Clear All History",
        key="clear_all",
        use_container_width=True,
    ):
        st.session_state.confirm_clear_all = True

    if st.session_state.confirm_clear_all:
        st.warning("Delete all saved conversations?")

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button(
                "Yes, Delete",
                key="confirm_delete",
                use_container_width=True,
            ):
                clear_all_history()
                st.rerun()

        with cancel_col:
            if st.button(
                "Cancel",
                key="cancel_delete",
                use_container_width=True,
            ):
                st.session_state.confirm_clear_all = False
                st.rerun()


# ================================================================
# RIGHT PANEL: CHAT WINDOW
# ================================================================

with chat_col:

    active_chat = get_active_chat()

    # Welcome screen
    if not active_chat["messages"]:

        st.markdown(
            """
            <div class="mq-welcome">
                <div class="mq-welcome-kicker">
                    WELCOME TO MEDIQUADE
                </div>
                <h2>What would you like to understand today?</h2>
                <p>
                    Ask a health or medical science question.
                    Get a clear, structured explanation from MediQuade AI.
                </p>
            </div>
            <div class="mq-section-label">START WITH A TOPIC</div>
            """,
            unsafe_allow_html=True,
        )

        suggested_prompts = [
            "What are the common symptoms of diabetes?",
            "Explain how blood pressure works.",
            "What is the difference between bacteria and viruses?",
        ]

        for index, prompt in enumerate(suggested_prompts):
            if st.button(
                prompt,
                key=f"suggest_{active_chat['id']}_{index}",
                use_container_width=True,
            ):
                st.session_state.pending_question = prompt
                st.rerun()

    else:
        st.markdown(
            f"""
            <div class="mq-section-label">
                CONVERSATION: {active_chat['title']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Display selected conversation
    for message in active_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    typed_question = st.chat_input(
        "Write your medical question here..."
    )

    pending_question = st.session_state.pending_question
    st.session_state.pending_question = ""

    question = pending_question or typed_question


    # ============================================================
    # BACKEND REQUEST
    # ============================================================

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
            # Store user message exactly once
            active_chat["messages"].append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            update_chat_title(active_chat, question)

            # Display the submitted question
            with st.chat_message("user"):
                st.markdown(question)

            # Generate response
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

                                if isinstance(error_data, dict):
                                    detail = error_data.get(
                                        "detail",
                                        response.text,
                                    )
                                else:
                                    detail = response.text

                            except ValueError:
                                detail = response.text or (
                                    "No additional error details returned."
                                )

                            if response.status_code in (401, 403):
                                st.error(
                                    "Backend rejected the API key. "
                                    "Check API_KEY in Streamlit Secrets."
                                )
                            else:
                                st.error(
                                    f"Backend error "
                                    f"(HTTP {response.status_code}): {detail}"
                                )

                        else:

                            try:
                                data: Any = response.json()
                            except ValueError:
                                data = None

                            if not isinstance(data, dict):
                                st.error(
                                    "Invalid response from backend. "
                                    "Check the FastAPI /ask endpoint."
                                )

                            else:
                                answer = data.get("answer", "")

                                if (
                                    not isinstance(answer, str)
                                    or not answer.strip()
                                ):
                                    detail = data.get(
                                        "detail",
                                        "Backend returned an empty answer.",
                                    )
                                    st.error(str(detail))

                                else:
                                    answer = answer.strip()

                                    st.markdown(answer)

                                    # Save answer in selected history
                                    active_chat["messages"].append(
                                        {
                                            "role": "assistant",
                                            "content": answer,
                                        }
                                    )

                    except requests.exceptions.Timeout:
                        st.error(
                            "Response timed out. Check that the Colab "
                            "model and FastAPI server are running."
                        )

                    except requests.exceptions.ConnectionError:
                        st.error(
                            "Cannot connect to backend. Check Colab "
                            "and update API_URL with the current "
                            "Cloudflare tunnel URL."
                        )

                    except requests.exceptions.RequestException as exc:
                        st.error(
                            f"The request could not be completed: {exc}"
                        )

            # Refresh history and show the saved response
            st.rerun()


# ------------------------------- Footer --------------------------

st.markdown(
    """
    <div class="mq-footer">
        MediQuade AI provides educational information and is not
        a substitute for professional medical advice.
    </div>
    """,
    unsafe_allow_html=True,
)
