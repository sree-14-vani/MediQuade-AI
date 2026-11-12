
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');

:root {
    --pista: #D5E6C1;
    --pista-light: #EDF3E5;
    --pista-dark: #A9C58B;
    --wine: #722F45;
    --wine-dark: #542033;
    --wine-light: #F3E6EA;
    --ivory: #F5F5EC;
    --forest: #46563B;
    --text: #303C2D;
    --muted: #77816F;
}

.stApp {
    background: linear-gradient(
        135deg,
        #F5F5EC 0%,
        #EDF3E5 55%,
        #E3EED8 100%
    );
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
    background: linear-gradient(
        120deg,
        #D5E6C1,
        #E7EEDC 65%,
        #F3E6EA
    );
    border: 1px solid #C1D4AE;
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
    color: rgba(114, 47, 69, 0.08);
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
    max-width: 600px;
    line-height: 1.8;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--wine);
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

.info-icon {
    font-size: 24px;
}

.info-heading {
    color: var(--wine);
    font-weight: 700;
    font-size: 14px;
}

.info-description {
    color: var(--muted);
    font-size: 12px;
    margin-top: 6px;
    line-height: 1.6;
}

.status-pill {
    display: inline-block;
    background: var(--wine-light);
    color: var(--wine);
    border: 1px solid #DFC0CB;
    border-radius: 30px;
    padding: 6px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
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
    background: #FFFFFF !important;
    color: var(--text) !important;
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

[data-testid="stChatInput"] {
    border-color: #C9D8BA !important;
}

hr {
    border-color: #D5DFCA;
}

.footer {
    text-align: center;
    color: var(--muted);
    font-size: 11px;
    padding: 25px 0 5px;
}

.small-muted {
    color: var(--muted);
    font-size: 12px;
}
