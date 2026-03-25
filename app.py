import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

from src.agent.immigration_agent import chat_with_agent, reset_conversation
from src.agent.knowledge_base import build_vector_store, CHUNKS_DB_PATH
from src.database.airtable_client import create_lead

load_dotenv()


# Load secrets from Streamlit Cloud or .env locally
def load_secrets():
    try:
        # Streamlit Cloud
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
        os.environ["AIRTABLE_API_KEY"] = st.secrets["AIRTABLE_API_KEY"]
        os.environ["AIRTABLE_BASE_ID"] = st.secrets["AIRTABLE_BASE_ID"]
        os.environ["RESEND_API_KEY"] = st.secrets["RESEND_API_KEY"]
    except:
        # Local development - fall back to .env
        from dotenv import load_dotenv

        load_dotenv()


load_secrets()

# --- Page Config -------------------------------------
st.set_page_config(
    page_title="Immigration Law Firm AI Assistant", page_icon="🏛️", layout="wide"
)

# --- Initialize Session State ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client_name" not in st.session_state:
    st.session_state.client_name = ""
if "session_started" not in st.session_state:
    st.session_state.session_started = False
if "kb_built" not in st.session_state:
    st.session_state.kb_built = os.path.exists(CHUNKS_DB_PATH)

# --- Custom CSS --------------------------------------
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #1a365d 80%, #2c5282 40%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
    }
    .main-header h1 {
        color: white;
        font-size: 2rem;
        margin: 0;
    }
    .main-header p {
        color: #bee3f8;
        margin: 0.5rem 0 0 0;
    }
    .info-card {
        background: #ebf8ff;
        border-left: 4px solid #3182ce;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        color: black;
    }
    .success-card {
        background: #f0fff4;
        border-left: 4px solid #38a169;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        color: black;
    }
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- Header ------------------------------------------
st.markdown(
    """
<div class="main-header">
    <h1>🏛️ Immigration Law Firm</h1>
    <p>AI-Powered Immigration Assistant — Available 24/7</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- Layout: Two Columns -----------------------------
left_col, right_col = st.columns([1, 2])

# --- LEFT COLUMN: Sidebar Info -----------------------
with left_col:
    st.markdown("### 👤 Your Information")
    with st.form("client_form"):
        name_input = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            value=st.session_state.client_name,
        )
        email_input = st.text_input("Email Address", placeholder="your@email.com")
        case_type_input = st.selectbox(
            "Case Type", ["", "Work Visa", "Green Card", "Citizenship", "DACA"]
        )
        start_btn = st.form_submit_button(
            "Start Conversation", use_container_width=True
        )

        if start_btn and name_input:
            st.session_state.client_name = name_input
            st.session_state.session_started = True

            # Save lead to Airtable if email provided
            if email_input and case_type_input:
                try:
                    create_lead(
                        name=name_input,
                        email=email_input,
                        phone="",
                        case_type=case_type_input,
                        source="AI Chat Widget",
                    )
                    st.success("✅ Your information has been saved!")
                except Exception as e:
                    st.warning(f"Could not save information: {e}")
            reset_conversation()
            st.rerun()

    st.divider()

    # --- PDF Upload ----------------------------------
    st.markdown("### 📄 Upload Documents")
    st.markdown("Upload firm documents to enhance the AI's knowledge base.")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        help="Upload immigration guides. FAQs, or firm documents",
    )

    if uploaded_file:
        if st.button("📚 Add to Knowledge Base", use_container_width=True):
            with st.spinner("Processing document..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf", dir="knowledge_base"
                    ) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # Rebuild knowledge base
                    build_vector_store()
                    st.session_state.kb_built = True
                    st.success(f"✅ '{uploaded_file.name}' added to knowledge base!")
                except Exception as e:
                    st.error(f"❌ Failed to process document: {e}")
    st.divider()

    # --- Knowledge Base Status -----------------------
    st.markdown("### 🧠 Knowledge Base")
    if st.session_state.kb_built:
        st.markdown(
            """
            <div class="success-card">
            ✅ Knowledge base is active
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="info-card">
            ⚠️ Knowledge base not built yet
            </div>
        """,
            unsafe_allow_html=True,
        )
    if st.button("🔄 Rebuild Knowledge Base", use_container_width=True):
        with st.spinner("Rebuilding..."):
            build_vector_store()
            st.session_state.kb_built = True
            st.success("✅ Knowledge base rebuilt!")

    st.divider()

    # --- Contact Info ----------------------------
    st.markdown("### 📞 Contact Us")
    st.markdown(
        """
    - 📱 +237 (680)749528
    - 📧 delmondbongha147@gmail.com
    - 🕒 Mon–Fri, 9am–6pm EST
    """
    )

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        reset_conversation()
        st.rerun()

# --- RIGHT COLUMN: Chat Interface ---------------
with right_col:
    st.markdown("### 💬 Chat with Our AI Assistant")

    # Show welcome message if session not started
    if not st.session_state.session_started:
        st.markdown(
            """
            <div class="info-card">
        👋 Welcome! Please enter your name on the left to start chatting 
        with our AI immigration assistant. I can answer questions about 
        visas, green cards, citizenship, DACA, and more — 24/7.
            </div>
        """,
            unsafe_allow_html=True,
        )
    # Build knowledge base on first lead
    if not st.session_state.kb_built:
        with st.spinner("Setting up knowledge base..."):
            build_vector_store()
            st.session_state.kb_built = True

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if st.session_state.session_started:
        if prompt := st.chat_input("Ask a question about our immigration case..."):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_with_agent(
                        user_message=prompt, client_name=st.session_state.client_name
                    )
                st.markdown(response)

            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.chat_input("Enter your name first to start chatting...", disabled=True)
