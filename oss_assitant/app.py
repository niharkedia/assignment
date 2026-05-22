import streamlit as st 
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="OSS AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown(
    """
    <style>
    /* Gradient headers */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Custom sidebar style */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }

    /* Card background for welcome state */
    .welcome-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
    }
    
    .welcome-card h3 {
        color: #f3f4f6;
        margin-top: 0;
    }

    .welcome-card p {
        color: #9ca3af;
        line-height: 1.6;
    }

    /* Custom buttons style */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/brain.png", width=64)
    st.markdown("### Assistant Configuration")
    st.markdown("Customize settings for the conversational agent.")
    
    # Model Selection
    model_name = st.selectbox(
        "Model",
        options=["llama-3.3-70b-versatile"],
        index=0,
        help="Select the Groq-hosted LLM to power the conversations."
    )
    
    # Hyperparameters
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls output randomness: lower values are more factual, higher values are more creative."
    )
    
    st.markdown("---")
    
    # Clear History Button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat history cleared!")
        st.rerun()

# Main Application Title
st.markdown("<h1 class='main-title'>OSS ASSISTANT</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by LangChain & Groq Llama-3.3</p>", unsafe_allow_html=True)

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Welcome Card if History is Empty
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
            <h3>Hello! How can I help you today? 🤖</h3>
            <p>I am your open-source powered assistant. I support <b>multi-turn conversations</b> and maintain <b>short-term context</b> across messages. Ask me a question, describe a problem, or let's just write some code!</p>
            <span style="font-size: 0.85rem; color: #a855f7; font-weight: 500;">✓ Short-term memory active</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input
if user_input := st.chat_input("Message OSS Assistant..."):
    # Append and show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Prepare full context including system instructions and chat memory
        formatted_messages = [
            SystemMessage(content="You are a helpful, professional, and friendly AI assistant. Give concise, accurate, and markdown-formatted answers.")
        ]
        
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        
        try:
            # Initialize ChatGroq instance
            llm = ChatGroq(
                model=model_name,
                temperature=temperature,
                api_key=os.environ.get("GROQ_API_KEY")
            )
            
            # Stream the generated response token by token
            for chunk in llm.stream(formatted_messages):
                full_response += chunk.content
                # Update UI with the incremental content
                message_placeholder.markdown(full_response + "▌")
            
            # Final render without caret
            message_placeholder.markdown(full_response)
            
            # Append assistant response to memory
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error generating response: {e}")
