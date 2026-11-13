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
