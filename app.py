
import streamlit as st
import requests

st.set_page_config(
    page_title="MediQuade AI",
    page_icon="🩺",
    layout="wide"
)

# -------------------------------
# PAGE DESIGN
# -------------------------------

st.title("🩺 MediQuade AI")
st.subheader("AI-Powered Medical Information Assistant")

st.markdown(
    "Ask medical questions and receive information "
    "from your fine-tuned Qwen3-4B model."
)

st.info(
    "For educational purposes only. "
    "This application does not replace professional medical advice."
)

# -------------------------------
# LOAD SECRETS SAFELY
# -------------------------------

try:
    API_URL = st.secrets.get("API_URL", "")
    API_KEY = st.secrets.get("API_KEY", "")
except Exception:
    API_URL = ""
    API_KEY = ""

if not API_URL or not API_KEY:
    st.error("Backend configuration is missing.")

    st.markdown("""
    Please configure these two values in:

    **Streamlit Community Cloud → App Settings → Secrets**

    ```toml
    API_URL = "https://YOUR-CLOUDFLARE-URL.trycloudflare.com/ask"
    API_KEY = "YOUR-COLAB-API-KEY"
    ```
    """)

    st.stop()

# -------------------------------
# SESSION STATE
# -------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# SIDEBAR
# -------------------------------

with st.sidebar:
    st.title("MediQuade AI")
    st.write("Model: Qwen3-4B")
    st.write("Fine-tuning: QLoRA")
    st.write("Dataset: MedQuAD")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# USER QUESTION
# -------------------------------

question = st.chat_input("Ask your medical question...")

if question:

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
                answer = result.get("answer")

                if not answer:
                    st.error("The backend returned an empty answer.")
                else:
                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")

            except requests.exceptions.HTTPError as e:
                st.error(f"Backend HTTP error: {e}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the Colab backend. "
                    "Check whether FastAPI and Cloudflare are running."
                )

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

            except ValueError:
                st.error("Backend returned an invalid JSON response.")
