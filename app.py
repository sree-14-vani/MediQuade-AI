
import streamlit as st
import requests
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MediQuade AI | Healthcare Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #09131F;
    --panel: #111F2D;
    --panel2: #152737;
    --teal: #42DCC1;
    --mint: #A1F5DC;
    --text: #EAF5F4;
    --muted: #91A8B6;
}

.stApp {
    background:
        radial-gradient(ellipse at 85% 0%, #143A43 0%, transparent 35%),
        radial-gradient(ellipse at 0% 100%, #102C3C 0%, transparent 35%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0D1B28;
    border-right: 1px solid #233B4A;
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.main .block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text) !important;
}

p, label {
    color: #B6C9D1;
}

.brand {
    font-family: 'Outfit', sans-serif;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    color: white;
}

.brand span {
    color: var(--teal);
}

.tagline {
    color: #829AA9;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: -5px;
}

.hero {
    background: linear-gradient(120deg, #142E3C, #123B43 65%, #17443F);
    border: 1px solid #32645F;
    border-radius: 24px;
    padding: 35px;
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
}

.hero:after {
    content: "✚";
    position: absolute;
    right: 45px;
    top: 5px;
    font-size: 145px;
    color: rgba(113, 235, 205, 0.07);
}

.hero-label {
    color: #8DEBD5;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 700;
    text-transform: uppercase;
}

.hero-title {
    color: white;
    font-family: 'Outfit', sans-serif;
    font-size: clamp(30px, 5vw, 43px);
    font-weight: 800;
    line-height: 1.15;
    margin: 15px 0;
}

.hero-description {
    color: #C2D9D9;
    font-size: 15px;
    max-width: 600px;
    line-height: 1.8;
}

.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 19px;
    font-weight: 700;
    color: #EAF5F4;
    margin: 22px 0 12px;
}

.info-card {
    background: linear-gradient(145deg, #142938, #10222F);
    border: 1px solid #284553;
    padding: 19px;
    border-radius: 17px;
    min-height: 115px;
}

.info-icon {
    font-size: 24px;
    margin-bottom: 9px;
}

.info-heading {
    color: #E9F5F2;
    font-weight: 700;
    font-size: 14px;
}

.info-description {
    color: #8EA9B7;
    font-size: 12px;
    margin-top: 6px;
    line-height: 1.6;
}

.status-pill {
    display: inline-block;
    background: #123C38;
    color: #77EBC9;
    border: 1px solid #28665B;
    border-radius: 30px;
    padding: 6px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.stButton > button {
    background: linear-gradient(110deg, #37CDB5, #65E6C3);
    color: #08221F !important;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    min-height: 43px;
    transition: all .2s ease;
}

.stButton > button:hover {
    background: #A1F5DC;
    color: #08221F !important;
    border: none;
    transform: translateY(-2px);
}

.stChatInput textarea,
.stTextArea textarea {
    background: #142737 !important;
    color: white !important;
    border: 1px solid #345264 !important;
    border-radius: 15px !important;
}

[data-testid="stChatMessage"] {
    background: #122432;
    border: 1px solid #294453;
    border-radius: 17px;
    padding: 14px;
    margin-bottom: 12px;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #12302F;
    border-color: #28645A;
}

[data-testid="stChatInput"] {
    border-color: #3D776F !important;
}

div[data-testid="stAlert"] {
    border-radius: 13px;
}

hr {
    border-color: #29404D;
}

.footer {
    text-align: center;
    color: #68818F;
    font-size: 11px;
    padding: 25px 0 5px;
}

.small-muted {
    color: #8099A7;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# BACKEND CONFIGURATION
# ==========================================

try:
    API_URL = st.secrets.get("API_URL", "")
    API_KEY = st.secrets.get("API_KEY", "")
except Exception:
    API_URL = ""
    API_KEY = ""

if not API_URL or not API_KEY:
    st.error("Backend configuration is missing.")
    st.info("Configure API_URL and API_KEY in Streamlit Secrets.")
    st.stop()


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def set_prompt(question):
    st.session_state.pending_question = question


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 0 22px;">
        <div class="brand">MediQuade<span> AI</span></div>
        <div class="tagline">Healthcare Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### ✦ Workspace")

    if st.button("＋  New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.markdown("---")

    st.markdown("### ◈ AI MODEL")

    st.markdown("""
    <div class="info-card">
        <div class="info-heading">Qwen3-4B</div>
        <div class="info-description">
            Fine-tuned with QLoRA<br>
            Medical Q&A · MedQuAD
        </div>
        <br>
        <span class="status-pill">MODEL CONFIGURED</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Recent conversation")

    if st.session_state.messages:
        for msg in st.session_state.messages[-6:]:
            if msg["role"] == "user":
                st.caption("YOU")
                st.write(msg["content"][:75])
    else:
        st.caption("Your conversations will appear here.")

    st.markdown("---")

    st.markdown("""
    <div class="small-muted">
        MEDIQUADE AI v1.0<br><br>
        Designed for accessible medical education.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-label">✦ YOUR INTELLIGENT HEALTHCARE COMPANION</div>
    <div class="hero-title">
        Understand health.<br>
        Make informed decisions.
    </div>
    <div class="hero-description">
        Explore medical knowledge through an AI-powered
        assistant designed to make healthcare information
        easier to understand.
    </div>
    <br>
    <span class="status-pill">✦ POWERED BY QWEN3-4B</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# FEATURE CARDS
# ==========================================

st.markdown(
    '<div class="section-title">Explore your health workspace</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🧬</div>
        <div class="info-heading">Disease Insights</div>
        <div class="info-description">
            Understand diseases, symptoms and medical conditions.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">💊</div>
        <div class="info-heading">Medical Knowledge</div>
        <div class="info-description">
            Explore treatments, medications and healthcare concepts.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🛡️</div>
        <div class="info-heading">Health Awareness</div>
        <div class="info-description">
            Learn about prevention, wellness and healthy habits.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# SUGGESTED QUESTIONS
# ==========================================

st.markdown(
    '<div class="section-title">✦ Start with a question</div>',
    unsafe_allow_html=True
)

questions = [
    "What are the symptoms of diabetes?",
    "Explain how the human immune system works.",
    "What causes high blood pressure?",
    "How can I maintain good heart health?"
]

cols = st.columns(2)

for i, q in enumerate(questions):
    with cols[i % 2]:
        st.button(
            q,
            key=f"suggestion_{i}",
            use_container_width=True,
            on_click=set_prompt,
            args=(q,)
        )


# ==========================================
# CHAT HISTORY
# ==========================================

st.markdown(
    '<div class="section-title">✦ Your AI conversation</div>',
    unsafe_allow_html=True
)

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# CHAT INPUT
# ==========================================

typed_question = st.chat_input(
    "Ask MediQuade AI anything about medical knowledge..."
)

question = (
    st.session_state.pending_question
    or typed_question
)

if question:

    st.session_state.pending_question = None

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("✦ MediQuade AI is thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"question": question},
                    headers={
                        "Authorization": f"Bearer {API_KEY}"
                    },
                    timeout=300
                )

                response.raise_for_status()

                result = response.json()

                answer = result.get("answer", "")

                if not answer:
                    answer = (
                        "I could not generate an answer. "
                        "Please try again."
                    )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "Please check whether the Colab model is running."
                )

            except requests.exceptions.HTTPError as e:

                st.error(f"Backend HTTP error: {e}")

            except requests.exceptions.ConnectionError:

                st.error(
                    "Unable to connect to the backend. "
                    "Check your Cloudflare Tunnel."
                )

            except (ValueError, KeyError):

                st.error("Invalid response received from the backend.")


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div class="footer">
    MEDIQUADE AI · HEALTHCARE INTELLIGENCE STUDIO<br><br>
    For educational purposes only. Not a substitute for
    professional medical diagnosis or treatment.
</div>
""", unsafe_allow_html=True)
