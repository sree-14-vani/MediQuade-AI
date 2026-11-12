
import streamlit as st
import requests

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MediQuade AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. PISTA GREEN + WINE RED THEME
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');

:root {
    --pista: #D5E6C1;
    --pista-light: #EDF3E5;
    --wine: #722F45;
    --wine-dark: #542033;
    --ivory: #F8F8F0;
    --forest: #46563B;
    --text: #303C2D;
    --muted: #77816F;
}

.stApp {
    background: linear-gradient(135deg, #F8F8F0, #EDF3E5, #E2EDD6);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #DCE9CE;
    border-right: 1px solid #C1D4AE;
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
    color: var(--wine) !important;
    font-family: 'Playfair Display', serif !important;
}

p, label {
    color: var(--text);
}

.brand {
    font-family: 'Playfair Display', serif;
    font-size: 29px;
    font-weight: 800;
    color: var(--wine);
}

.brand span {
    color: var(--forest);
}

.tagline {
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero {
    background: linear-gradient(120deg, #D5E6C1, #E7EEDC, #F3E6EA);
    border: 1px solid #C1D4AE;
    border-radius: 24px;
    padding: 35px;
    margin-bottom: 25px;
}

.hero-label {
    color: var(--wine);
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 800;
}

.hero-title {
    color: var(--wine-dark);
    font-family: 'Playfair Display', serif;
    font-size: clamp(30px, 5vw, 43px);
    font-weight: 800;
    line-height: 1.2;
    margin: 15px 0;
}

.hero-description {
    color: #53634A;
    font-size: 15px;
    line-height: 1.8;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 21px;
    font-weight: 700;
    color: var(--wine);
    margin: 22px 0 12px;
}

.info-card {
    background: #FFFFFF;
    border: 1px solid #DCE6D2;
    padding: 20px;
    border-radius: 17px;
    min-height: 130px;
    box-shadow: 0 4px 15px rgba(65, 80, 50, 0.05);
}

.info-icon {
    font-size: 25px;
    margin-bottom: 9px;
}

.info-heading {
    color: var(--wine);
    font-weight: 700;
    font-size: 15px;
}

.info-description {
    color: var(--muted);
    font-size: 12px;
    margin-top: 7px;
    line-height: 1.6;
}

.status-pill {
    display: inline-block;
    background: #F3E6EA;
    color: var(--wine);
    border: 1px solid #DFC0CB;
    border-radius: 30px;
    padding: 7px 13px;
    font-size: 11px;
    font-weight: 700;
}

.stButton > button {
    background: var(--wine);
    color: white !important;
    border: 1px solid var(--wine);
    border-radius: 12px;
    font-weight: 700;
    min-height: 43px;
    transition: all .2s ease;
}

.stButton > button:hover {
    background: var(--wine-dark);
    border-color: var(--wine-dark);
    color: white !important;
    transform: translateY(-2px);
}

.stChatInput textarea,
.stTextArea textarea {
    background: white !important;
    color: var(--text) !important;
    border: 1px solid #C9D8BA !important;
    border-radius: 15px !important;
}

[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid #DCE6D2;
    border-radius: 17px;
    padding: 14px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border-color: #C9D8BA !important;
}

[data-testid="stAlert"] {
    border-radius: 13px;
}

hr {
    border-color: #D5DFCA;
}

.footer {
    text-align: center;
    color: var(--muted);
    font-size: 11px;
    padding: 25px 0;
}

.small-muted {
    color: var(--muted);
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. BACKEND CONFIGURATION
# ==========================================

try:
    API_URL = st.secrets.get("API_URL", "").strip()
    API_KEY = st.secrets.get("API_KEY", "").strip()
except Exception:
    API_URL = ""
    API_KEY = ""

if not API_URL or not API_KEY:
    st.error("Backend configuration is missing.")
    st.info(
        "Add API_URL and API_KEY in "
        "Streamlit Community Cloud → Settings → Secrets."
    )
    st.stop()


# ==========================================
# 4. SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def set_prompt(question):
    st.session_state.pending_question = question


# ==========================================
# 5. SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 0 22px;">
        <div class="brand">MediQuade <span>AI</span></div>
        <div class="tagline">Healthcare Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### ✦ Workspace")

    if st.button("＋ New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.markdown("---")

    st.markdown("### ◈ AI MODEL")

    st.markdown("""
    <div class="info-card">
        <div class="info-heading">Qwen3-4B</div>
        <div class="info-description">
            Fine-tuned using QLoRA<br>
            Medical Question Answering<br>
            Dataset: MedQuAD
        </div>
        <br>
        <span class="status-pill">MODEL CONFIGURED</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Recent Questions")

    recent_questions = [
        m["content"]
        for m in st.session_state.messages
        if m["role"] == "user"
    ]

    if recent_questions:
        for item in recent_questions[-5:]:
            st.caption("• " + item[:65])
    else:
        st.caption("Your questions will appear here.")

    st.markdown("---")

    st.markdown("""
    <div class="small-muted">
        MEDIQUADE AI · VERSION 1.0<br><br>
        Healthcare Intelligence Studio
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 6. HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-label">
        ✦ YOUR INTELLIGENT HEALTHCARE COMPANION
    </div>

    <div class="hero-title">
        Understand Health.<br>
        Discover Knowledge.
    </div>

    <div class="hero-description">
        Explore medical knowledge through an AI-powered
        assistant designed to make healthcare information
        easier to understand.
    </div>

    <br>

    <span class="status-pill">
        ✦ POWERED BY QWEN3-4B
    </span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 7. FEATURE CARDS
# ==========================================

st.markdown(
    '<div class="section-title">Explore Your Health Workspace</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🧬</div>
        <div class="info-heading">Disease Insights</div>
        <div class="info-description">
            Explore diseases, symptoms and medical conditions.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">💊</div>
        <div class="info-heading">Medical Knowledge</div>
        <div class="info-description">
            Understand treatments, medications and medical concepts.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🌿</div>
        <div class="info-heading">Health Awareness</div>
        <div class="info-description">
            Learn about prevention, wellness and healthy habits.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 8. SUGGESTED QUESTIONS
# ==========================================

st.markdown(
    '<div class="section-title">✦ Start With a Question</div>',
    unsafe_allow_html=True
)

questions = [
    "What are the symptoms of diabetes?",
    "How does the human immune system work?",
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
# 9. CHAT HISTORY
# ==========================================

st.markdown(
    '<div class="section-title">✦ Your AI Conversation</div>',
    unsafe_allow_html=True
)

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# 10. CHAT INPUT AND MODEL RESPONSE
# ==========================================

typed_question = st.chat_input(
    "Ask MediQuade AI about medical knowledge..."
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

        with st.spinner("MediQuade AI is thinking..."):

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
                    "Request timed out. "
                    "Check whether your Colab model is running."
                )

            except requests.exceptions.HTTPError as e:

                st.error(f"Backend HTTP error: {e}")

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to the backend. "
                    "Check your Cloudflare Tunnel."
                )

            except (ValueError, KeyError):

                st.error("Invalid response received from backend.")

            except Exception as e:

                st.error(f"Unexpected error: {e}")


# ==========================================
# 11. FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div class="footer">
    MEDIQUADE AI · HEALTHCARE INTELLIGENCE STUDIO<br><br>
    For educational purposes only. Not a substitute
    for professional medical diagnosis or treatment.
</div>
""", unsafe_allow_html=True)
