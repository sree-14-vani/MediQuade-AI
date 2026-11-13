
import os
import requests
import streamlit as st

# ============================================================
# MediQuade AI - Healthcare Chatbot
# Frontend: Streamlit
# Backend: FastAPI + Qwen3-4B QLoRA on Google Colab
# ============================================================

st.set_page_config(
    page_title="MediQuade AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- API CONFIGURATION --------------------

def get_setting(name):
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

# -------------------- SESSION STATE --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""

# -------------------- TWO-COLOR DESIGN --------------------

st.markdown("""
<style>

:root {
    --navy: #12344A;
    --white: #FFFFFF;
}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #FFFFFF !important;
    color: #12344A !important;
}

[data-testid="stHeader"] {
    background: #FFFFFF !important;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 1050px;
    padding: 1.5rem 2rem 6rem 2rem;
}

/* HEADER */

.mq-header {
    background: #12344A;
    color: #FFFFFF !important;
    padding: 22px 26px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}

.mq-brand {
    display: flex;
    align-items: center;
    gap: 15px;
}

.mq-logo {
    width: 52px;
    height: 52px;
    background: #FFFFFF;
    color: #12344A !important;
    border-radius: 13px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 27px;
    font-weight: 900;
}

.mq-title {
    color: #FFFFFF !important;
    font-size: 27px;
    font-weight: 800;
    margin: 0;
}

.mq-subtitle {
    color: #FFFFFF !important;
    font-size: 13px;
    margin-top: 4px;
}

.mq-tag {
    border: 1px solid #FFFFFF;
    color: #FFFFFF !important;
    border-radius: 30px;
    padding: 8px 13px;
    font-size: 11px;
    font-weight: 700;
}

/* WELCOME */

.mq-welcome {
    background: #FFFFFF;
    border: 2px solid #12344A;
    border-radius: 16px;
    padding: 30px;
    margin: 18px 0 24px 0;
}

.mq-label {
    color: #12344A !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.mq-welcome h2 {
    color: #12344A !important;
    font-size: 27px;
    font-weight: 800;
    margin: 12px 0;
}

.mq-welcome p {
    color: #12344A !important;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 0;
}

/* SECTION */

.mq-section {
    color: #12344A !important;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 25px 0 12px 0;
}

/* BUTTONS */

div.stButton > button {
    background: #FFFFFF !important;
    color: #12344A !important;
    border: 1.5px solid #12344A !important;
    border-radius: 11px !important;
    min-height: 48px;
    font-weight: 700 !important;
    transition: 0.2s ease;
}

div.stButton > button p,
div.stButton > button span {
    color: #12344A !important;
}

div.stButton > button:hover {
    background: #12344A !important;
    color: #FFFFFF !important;
}

div.stButton > button:hover p,
div.stButton > button:hover span {
    color: #FFFFFF !important;
}

/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1.5px solid #12344A !important;
    border-radius: 14px !important;
    padding: 15px !important;
    margin: 12px 0 !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: #12344A !important;
    line-height: 1.7 !important;
}

/* CHAT INPUT */

[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 2px solid #12344A !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #12344A !important;
    -webkit-text-fill-color: #12344A !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #12344A !important;
    opacity: 0.7 !important;
}

[data-testid="stChatInput"] button {
    background: #12344A !important;
    border-radius: 9px !important;
}

[data-testid="stChatInput"] button svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* ALERTS */

[data-testid="stAlert"] {
    background: #FFFFFF !important;
    border: 1.5px solid #12344A !important;
    border-radius: 10px;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #12344A !important;
}

/* FOOTER */

.mq-footer {
    border-top: 1px solid #12344A;
    margin-top: 35px;
    padding-top: 15px;
    color: #12344A !important;
    font-size: 12px;
    text-align: center;
    line-height: 1.6;
}

#MainMenu, footer {
    visibility: hidden;
}

@media(max-width: 700px) {
    .block-container {
        padding: 1rem 0.8rem 6rem 0.8rem;
    }

    .mq-header {
        padding: 16px;
    }

    .mq-title {
        font-size: 21px;
    }

    .mq-tag {
        display: none;
    }

    .mq-welcome {
        padding: 20px;
    }

    .mq-welcome h2 {
        font-size: 22px;
    }
}

</style>
""", unsafe_allow_html=True)


# -------------------- HEADER --------------------

st.markdown("""
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
    <div class="mq-tag">AI HEALTH ASSISTANT</div>
</div>
""", unsafe_allow_html=True)


# -------------------- CHAT CONTROLS --------------------

control1, control2, empty = st.columns([1.2, 1.2, 5])

with control1:
    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = ""
        st.rerun()

with control2:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = ""
        st.rerun()


# -------------------- WELCOME SCREEN --------------------

if not st.session_state.messages:

    st.markdown("""
    <div class="mq-welcome">
        <div class="mq-label">WELCOME TO MEDIQUADE AI</div>
        <h2>How can I help you today?</h2>
        <p>
            Ask questions about diseases, symptoms, health conditions,
            prevention and medical science. Get clear explanations
            through an AI-powered conversational assistant.
        </p>
    </div>
    <div class="mq-section">SUGGESTED QUESTIONS</div>
    """, unsafe_allow_html=True)

    prompts = [
        "What are the common symptoms of diabetes?",
        "What causes high blood pressure?",
        "Explain the difference between Type 1 and Type 2 diabetes.",
        "What are the symptoms of anemia?",
        "How can I maintain a healthy lifestyle?",
        "What is the difference between bacteria and viruses?"
    ]

    for start in range(0, len(prompts), 2):
        col1, col2 = st.columns(2)

        with col1:
            prompt = prompts[start]
            if st.button(prompt, key=f"prompt_{start}",
                         use_container_width=True):
                st.session_state.pending_question = prompt
                st.rerun()

        if start + 1 < len(prompts):
            with col2:
                prompt = prompts[start + 1]
                if st.button(prompt, key=f"prompt_{start+1}",
                             use_container_width=True):
                    st.session_state.pending_question = prompt
                    st.rerun()


# -------------------- DISPLAY CHAT HISTORY --------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------- QUESTION INPUT --------------------

typed_question = st.chat_input(
    "Ask MediQuade AI a medical question..."
)

question = st.session_state.pending_question or typed_question
st.session_state.pending_question = ""


# -------------------- BACKEND REQUEST --------------------

if question:

    question = question.strip()

    if not question:
        st.warning("Please enter a question.")

    elif len(question) > 4000:
        st.error("Question must not exceed 4,000 characters.")

    elif not API_ENDPOINT or not API_KEY:
        st.error(
            "Backend configuration missing. "
            "Check API_URL and API_KEY in Streamlit Secrets."
        )

    else:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("MediQuade AI is thinking..."):

                try:

                    response = requests.post(
                        API_ENDPOINT,
                        json={"question": question},
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        },
                        timeout=(20, 300)
                    )

                    response.raise_for_status()

                    data = response.json()

                    answer = data.get("answer", "")

                    if not isinstance(answer, str) or not answer.strip():
                        st.error("The backend returned an empty answer.")

                    else:

                        answer = answer.strip()

                        st.markdown(answer)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                except requests.exceptions.Timeout:
                    st.error(
                        "Request timed out. "
                        "Check whether your Colab backend is running."
                    )

                except requests.exceptions.HTTPError as exc:

                    status = (
                        exc.response.status_code
                        if exc.response is not None else "Unknown"
                    )

                    if status in (401, 403):
                        st.error(
                            "Invalid API key. Check API_KEY in Streamlit Secrets."
                        )
                    else:
                        detail = (
                            exc.response.text[:1000]
                            if exc.response is not None else str(exc)
                        )
                        st.error(f"Backend HTTP error {status}: {detail}")

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to the backend. "
                        "Check Colab and your Cloudflare tunnel URL."
                    )

                except (requests.exceptions.RequestException, ValueError) as exc:
                    st.error(f"Request failed: {exc}")


# -------------------- FOOTER --------------------

st.markdown("""
<div class="mq-footer">
    <strong>MediQuade AI</strong><br>
    AI-powered medical question answering assistant.<br>
    This application provides educational information and
    does not replace professional medical advice.
</div>
""", unsafe_allow_html=True)
