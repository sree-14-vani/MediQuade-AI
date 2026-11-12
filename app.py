
# ==========================================
# CUSTOM CSS - PISTA GREEN & WINE RED
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');

.stApp {
    background: linear-gradient(
        135deg,
        #F5F5EC 0%,
        #EDF3E5 55%,
        #D5E6C1 100%
    );
    color: #303C2D;
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
    color: #303C2D;
}

.main .block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #722F45 !important;
    font-family: 'Playfair Display', serif !important;
}

.brand {
    font-family: 'Playfair Display', serif;
    font-size: 29px;
    font-weight: 800;
    color: #722F45;
}

.brand span {
    color: #46563B;
}

.tagline {
    color: #77816F;
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
    color: #722F45;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 800;
}

.hero-title {
    color: #542033;
    font-family: 'Playfair Display', serif;
    font-size: 40px;
    font-weight: 800;
    line-height: 1.2;
}

.hero-description {
    color: #53634A;
    font-size: 15px;
    line-height: 1.8;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: #722F45;
    margin: 22px 0 12px;
}

.info-card {
    background: #FFFFFF;
    border: 1px solid #DCE6D2;
    padding: 19px;
    border-radius: 17px;
    min-height: 115px;
    box-shadow: 0 4px 15px rgba(65, 80, 50, 0.05);
}

.info-heading {
    color: #722F45;
    font-weight: 700;
    font-size: 14px;
}

.info-description {
    color: #77816F;
    font-size: 12px;
    line-height: 1.6;
}

.status-pill {
    display: inline-block;
    background: #F3E6EA;
    color: #722F45;
    border: 1px solid #DFC0CB;
    border-radius: 30px;
    padding: 6px 12px;
    font-size: 11px;
    font-weight: 700;
}

.stButton > button {
    background: #722F45;
    color: white !important;
    border: 1px solid #722F45;
    border-radius: 12px;
    font-weight: 700;
    min-height: 43px;
}

.stButton > button:hover {
    background: #542033;
    color: white !important;
}

.stChatInput textarea,
.stTextArea textarea {
    background: #FFFFFF !important;
    color: #303C2D !important;
    border: 1px solid #C9D8BA !important;
    border-radius: 15px !important;
}

[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border: 1px solid #DCE6D2;
    border-radius: 17px;
    padding: 14px;
    margin-bottom: 12px;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #F0F5E9;
    border-color: #C9DABB;
}

hr {
    border-color: #D5DFCA;
}

.footer {
    text-align: center;
    color: #77816F;
    font-size: 11px;
    padding: 25px 0;
}

.small-muted {
    color: #77816F;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)
