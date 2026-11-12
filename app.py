
import streamlit as st
import requests
import textwrap

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
# 2. PROFESSIONAL TWO-COLOUR THEME
# ==========================================

PISTA = "#DCE8C9"
WINE = "#722F45"


def render_html(content):
    st.markdown(
        textwrap.dedent(content),
        unsafe_allow_html=True
    )


st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"],
.stApp, [data-testid="stMain"] {{
    background: {PISTA} !important;
    color: {WINE} !important;
    font-family: 'DM Sans', sans-serif !important;
}}

[data-testid="stHeader"] {{
    background: {PISTA} !important;
}}

[data-testid="stSidebar"] {{
    background: {PISTA} !important;
    border-right: 2px solid {WINE} !important;
}}

[data-testid="stSidebar"] * {{
    color: {WINE} !important;
}}

.main .block-container {{
    max-width: 1150px;
    padding-top: 35px;
    padding-bottom: 40px;
}}

h1, h2, h3, h4, p, label, span {{
    color: {WINE};
}}

h1, h2, h3 {{
    font-weight: 800 !important;
}}

.brand {{
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -1px;
    color: {WINE};
}}

.brand-sub {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {WINE};
}}

.hero {{
    background: {PISTA};
    border: 2px solid {WINE};
    border-radius: 20px;
    padding: 38px;
    margin-bottom: 30px;
}}

.hero-label {{
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 3px;
    color: {WINE};
}}

.hero-title {{
    font-size: clamp(32px, 5vw, 48px);
    font-weight: 800;
    line-height: 1.2;
    color: {WINE};
    margin-top: 18px;
}}

.hero-description {{
    font-size: 16px;
    line-height: 1.8;
    font-weight: 600;
    color: {WINE};
    max-width: 680px;
}}

.section-heading {{
    font-size: 23px;
    font-weight: 800;
    color: {WINE};
    margin-top: 28px;
    margin-bottom: 16px;
}}

.feature-card {{
    background: {PISTA};
    border: 2px solid {WINE};
    border-radius: 16px;
    padding: 22px;
    min-height: 145px;
}}

.feature-icon {{
    font-size: 26px;
    margin-bottom: 12px;
}}

.feature-title {{
    font-size: 17px;
    font-weight: 800;
    color: {WINE};
}}

.feature-description {{
    font-size: 13px;
    font-weight: 600;
    line-height: 1.6;
    color: {WINE};
    margin-top: 8px;
}}

.model-info {{
    border: 2px solid {WINE};
    border-radius: 15px;
    padding: 16px;
    font-weight: 700;
}}

.stButton > button {{
    background: {WINE} !important;
    color: {PISTA} !important;
    border: 2px solid {WINE} !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    min-height: 44px;
}}

.stButton > button p {{
    color: {PISTA} !important;
    font-weight: 800 !important;
}}

.stButton > button:hover {{
    background: {PISTA} !important;
    color: {WINE} !important;
}}

.stButton > button:hover p {{
    color: {WINE} !important;
}}

.stChatInput {{
    background: {PISTA} !important;
}}

.stChatInput textarea {{
    background: {PISTA} !important;
    color: {WINE} !important;
    border: 2px solid {WINE} !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
}}

.stChatInput textarea::placeholder {{
    color: {WINE} !important;
    opacity: 0.8;
}}

[data-testid="stChatMessage"] {{
    background: {PISTA} !important;
    border: 2px solid {WINE} !important;
    border-radius: 16px !important;
    margin-bottom: 12px;
}}

[data-testid="stChatMessage"] * {{
    color: {WINE} !important;
}}

[data-testid="stMarkdownContainer"] p {{
    color: {WINE};
}}

[data-testid="stAlert"] {{
    background: {PISTA} !important;
    border: 2px solid {WINE} !important;
}}

[data-testid="stAlert"] * {{
    color: {WINE} !important;
}}

input, textarea {{
    color: {WINE} !important;
}}

hr {{
    border-color: {WINE} !important;
}}

.footer {{
    text-align: center;
    font-size: 13px;
    font-weight: 700;
    color: {WINE};
    padding: 25px;
}}

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
    st.stop()


# ==========================================
# 4. SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def clear_chat():
    st.session_state.messages = []
    st.session_state.pending_question = None


def set_question(question):
    st.session_state.pending_question = question


# ==========================================
# 5. SIDEBAR
# ==========================================

with st.sidebar:

    render_html("""
    <div style="padding:15px 0 20px;">
        <div class="brand">MediQuade AI</div>
        <div class="brand-sub">HEALTHCARE INTELLIGENCE</div>
    </div>
    """)

    st.divider()

    st.markdown("### WORKSPACE")

    if st.button("＋  New Conversation", use_container_width=True):
        clear_chat()
        st.rerun()

    if st.button("🗑️  Clear Chat History", use_container_width=True):
        clear_chat()
        st.rerun()

    st.divider()

    st.markdown("### AI MODEL")

    render_html("""
    <div class="model-info">
        Qwen3-4B<br><br>
        QLoRA Fine-tuned<br>
        Medical Q&A<br>
        MedQuAD Dataset
    </div>
    """)

    st.divider()

    st.markdown("### RECENT QUESTIONS")

    user_questions = [
        m["content"]
        for m in st.session_state.messages
        if m["role"] == "user"
    ]

    if user_questions:
        for q in user_questions[-5:]:
            st.caption("• " + q[:55])
    else:
        st.caption("No conversations yet.")

    st.divider()

    st.caption("MEDIQUADE AI | VERSION 1.0")


# ==========================================
# 6. MAIN HERO SECTION
# ==========================================

render_html("""
<div class="hero">

    <div class="hero-label">
        YOUR INTELLIGENT HEALTHCARE COMPANION
    </div>

    <div class="hero-title">
        Better Health Begins<br>
        With Better Knowledge.
    </div>

    <div class="hero-description">
        Welcome to MediQuade AI. Explore medical knowledge,
        understand health conditions and discover reliable
        healthcare information with your AI assistant.
    </div>

</div>
""")


# ==========================================
# 7. FEATURE CARDS
# ==========================================

render_html("""
<div class="section-heading">
    Explore Healthcare Knowledge
</div>
""")

c1, c2, c3 = st.columns(3)

with c1:
    render_html("""
    <div class="feature-card">
        <div class="feature-icon">🧬</div>
        <div class="feature-title">Disease Insights</div>
        <div class="feature-description">
            Explore diseases, symptoms and medical conditions.
        </div>
    </div>
    """)

with c2:
    render_html("""
    <div class="feature-card">
        <div class="feature-icon">💊</div>
        <div class="feature-title">Medical Knowledge</div>
        <div class="feature-description">
            Understand medical concepts, treatments and medicines.
        </div>
    </div>
    """)

with c3:
    render_html("""
    <div class="feature-card">
        <div class="feature-icon">🌿</div>
        <div class="feature-title">Health Awareness</div>
        <div class="feature-description">
            Discover prevention, wellness and healthy habits.
        </div>
    </div>
    """)


# ==========================================
# 8. SUGGESTED QUESTIONS
# ==========================================

render_html("""
<div class="section-heading">
    Suggested Questions
</div>
""")

suggestions = [
    "What are the symptoms of diabetes?",
    "What causes high blood pressure?",
    "How does the immune system work?",
    "How can I maintain good heart health?"
]

left, right = st.columns(2)

for i, question in enumerate(suggestions):

    with (left if i % 2 == 0 else right):

        st.button(
            question,
            key=f"suggestion_{i}",
            use_container_width=True,
            on_click=set_question,
            args=(question,)
        )


# ==========================================
# 9. CHAT SECTION + CLEAR OPTION
# ==========================================

st.divider()

chat_col, clear_col = st.columns([5, 1])

with chat_col:
    render_html("""
    <div class="section-heading">
        MediQuade AI Chat
    </div>
    """)

with clear_col:
    st.write("")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()


# ==========================================
# 10. DISPLAY CHAT HISTORY
# ==========================================

if not st.session_state.messages:

    render_html("""
    <div class="feature-card">
        <div class="feature-title">
            Welcome to your medical AI assistant!
        </div>
        <div class="feature-description">
            Type a medical question below or choose one
            of the suggested questions to begin.
        </div>
    </div>
    """)

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# 11. CHAT INPUT
# ==========================================

typed_question = st.chat_input(
    "Ask MediQuade AI your medical question..."
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

        try:

            with st.spinner("MediQuade AI is generating your answer..."):

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
                    answer = "No answer was generated. Please try again."

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except requests.exceptions.Timeout:

            st.error("Request timed out. Check your Colab backend.")

        except requests.exceptions.HTTPError as e:

            st.error(f"Backend HTTP error: {e}")

        except requests.exceptions.ConnectionError:

            st.error("Cannot connect. Check your Cloudflare Tunnel.")

        except requests.exceptions.RequestException as e:

            st.error(f"Request failed: {e}")

        except (ValueError, KeyError):

            st.error("Invalid response received from the backend.")


# ==========================================
# 12. FOOTER
# ==========================================

st.divider()

render_html("""
<div class="footer">
    MEDIQUADE AI | HEALTHCARE INTELLIGENCE STUDIO<br><br>
    For educational purposes only. Not a substitute
    for professional medical diagnosis or treatment.
</div>
""")
