import os
import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

st.set_page_config(page_title="MediQuade AI", page_icon="🩺", layout="centered")
BASE_MODEL_ID = "Qwen/Qwen3-4B"
ADAPTER_ID = os.getenv("MEDIQUADE_ADAPTER", "./mediQuade_lora_adapter")
SYSTEM_PROMPT = (
    "You are MediQuade AI, an educational medical information assistant. "
    "Provide cautious general information. Do not diagnose, prescribe, or replace "
    "a qualified healthcare professional. For potentially serious symptoms, "
    "recommend prompt professional medical care."
)

@st.cache_resource(show_spinner="Loading MediQuade AI model...")
def load_model():
    if not torch.cuda.is_available():
        raise RuntimeError(
            "A CUDA GPU is required to run Qwen3-4B with this app. Use a GPU-backed "
            "host or connect this Streamlit frontend to a separate inference API."
        )
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID, quantization_config=quant_config, device_map="auto",
        torch_dtype=torch.float16, trust_remote_code=True,
    )
    model = PeftModel.from_pretrained(base_model, ADAPTER_ID)
    model.eval()
    return tokenizer, model

st.title("🩺 MediQuade AI")
st.subheader("Your AI-powered medical learning assistant")
st.caption("Ask general educational questions about medical concepts and health.")
with st.expander("Important medical disclaimer"):
    st.warning(
        "This application provides educational information only. It does not "
        "provide diagnosis, prescriptions, or personalized treatment. Consult a "
        "qualified healthcare professional; seek emergency care when needed."
    )

try:
    tokenizer, model = load_model()
    st.success("MediQuade AI is ready.")
except Exception as exc:
    st.error("The model could not be loaded.")
    st.exception(exc)
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
with st.sidebar:
    st.markdown("### Model information")
    st.write("Base model: Qwen3-4B")
    st.write("Fine-tuning: QLoRA / LoRA")
    st.write("Quantization: 4-bit NF4")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask your medical question...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
    conversation.extend(st.session_state.messages[-10:])
    with st.chat_message("assistant"):
        with st.spinner("MediQuade AI is preparing an answer..."):
            prompt = tokenizer.apply_chat_template(
                conversation, tokenize=False, add_generation_prompt=True, enable_thinking=False
            )
            inputs = tokenizer(prompt, return_tensors="pt")
            input_device = model.get_input_embeddings().weight.device
            inputs = {key: value.to(input_device) for key, value in inputs.items()}
            with torch.inference_mode():
                output = model.generate(
                    **inputs, max_new_tokens=350, do_sample=True, temperature=0.3,
                    top_p=0.9, repetition_penalty=1.1,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                )
            answer = tokenizer.decode(
                output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
            ).strip()
            if not answer:
                answer = "I couldn't generate an answer. Please try again."
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
