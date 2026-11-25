from __future__ import annotations

import os

from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv(override=True)

# Import generate_response dynamically after setting provider
def get_generate_response(provider: str):
    """Dynamically import generate_response with the current provider."""
    # Set the provider in environment for openai_service to use
    os.environ["API_PROVIDER"] = provider
    
    # Reimport to get fresh module with new provider
    import importlib
    import openai_service
    importlib.reload(openai_service)
    
    return openai_service.generate_response

st.set_page_config(
    page_title="ChatSynth | AI Workspace",
    page_icon=":material/auto_awesome:",
    layout="wide",
)

# Initialize session state
if "api_provider" not in st.session_state:
    st.session_state.api_provider = os.getenv("API_PROVIDER", "openrouter").lower()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None

if "conversation_messages" not in st.session_state:
    st.session_state.conversation_messages = []

if "active_model" not in st.session_state:
    if st.session_state.api_provider == "openrouter":
        st.session_state.active_model = "nvidia/nemotron-3-ultra-550b-a55b:free"
    elif st.session_state.api_provider == "groq":
        st.session_state.active_model = "openai/gpt-oss-20b"
    elif st.session_state.api_provider == "gemini":
        st.session_state.active_model = "gemini-2.5-flash"
    elif st.session_state.api_provider == "nvidia":
        st.session_state.active_model = "meta/llama-3.1-8b-instruct"
    else:
        st.session_state.active_model = "gpt-4"

st.caption("CHATSYNTH  /  AI WORKSPACE")
st.title("ChatSynth", icon=":material/auto_awesome:")
st.caption("One conversation, with the freedom to choose the model behind it.")

with st.container(horizontal=True, gap="small"):
    st.badge(
        f"{st.session_state.api_provider.upper()} active",
        icon=":material/hub:",
        color="green",
    )
    st.badge(
        st.session_state.active_model,
        icon=":material/neurology:",
        color="blue",
    )
    st.badge(
        f"{len(st.session_state.messages)} messages",
        icon=":material/forum:",
    )

with st.sidebar:
    st.title("Your workspace", icon=":material/tune:")
    
    # Provider selection
    st.subheader("Choose your provider", icon=":material/hub:")
    
    provider_option = st.radio(
        "Choose your provider:",
        options=["OpenRouter", "Groq", "Gemini AI Studio", "NVIDIA NIM", "OpenAI"],
        index=["openrouter", "groq", "gemini", "nvidia", "openai"].index(st.session_state.api_provider)
        if st.session_state.api_provider in {"openrouter", "groq", "gemini", "nvidia", "openai"}
        else 0,
        help="Choose OpenRouter, Groq, Gemini AI Studio, NVIDIA NIM, or OpenAI.",
    )
    
    provider_ids = {
        "OpenRouter": "openrouter",
        "Groq": "groq",
        "Gemini AI Studio": "gemini",
        "NVIDIA NIM": "nvidia",
        "OpenAI": "openai",
    }
    selected_provider = provider_ids[provider_option]
    
    # Check if provider changed
    if selected_provider != st.session_state.api_provider:
        st.session_state.api_provider = selected_provider
        st.session_state.messages = []
        st.session_state.previous_response_id = None
        st.session_state.conversation_messages = []
        st.session_state.starter_prompt = None
        
        # Update default model based on new provider
        if selected_provider == "openrouter":
            st.session_state.active_model = "nvidia/nemotron-3-ultra-550b-a55b:free"
        elif selected_provider == "groq":
            st.session_state.active_model = "openai/gpt-oss-20b"
        elif selected_provider == "gemini":
            st.session_state.active_model = "gemini-2.5-flash"
        elif selected_provider == "nvidia":
            st.session_state.active_model = "meta/llama-3.1-8b-instruct"
        else:
            st.session_state.active_model = "gpt-4"
        
        st.success(f"✅ Switched to {provider_option}! Conversation reset.")
        st.rerun()
    
    st.markdown("---")
    
    # API key status
    st.subheader("API key status", icon=":material/key:")
    
    if st.session_state.api_provider == "openrouter":
        if os.getenv("OPENROUTER_API_KEY"):
            st.success("✅ OpenRouter API key detected")
        else:
            st.error("❌ OpenRouter API key missing")
            st.markdown("""
            **Get your key:**
            1. Visit [OpenRouter](https://openrouter.ai/keys)
            2. Create an API key
            3. Add to `.env` file:
            ```
            OPENROUTER_API_KEY=your-key
            ```
            """)
    elif st.session_state.api_provider == "groq":
        if os.getenv("GROQ_API_KEY"):
            st.success("✅ Groq API key detected")
        else:
            st.error("❌ Groq API key missing")
            st.markdown("""
            **Get your key:**
            1. Visit [Groq Console](https://console.groq.com/keys)
            2. Create an API key
            3. Add to `.env` file:
            ```
            GROQ_API_KEY=your-key
            ```
            """)
    elif st.session_state.api_provider == "gemini":
        if os.getenv("GEMINI_API_KEY"):
            st.success("✅ Gemini API key detected")
        else:
            st.error("❌ Gemini API key missing")
            st.markdown("""
            **Get your key:**
            1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
            2. Create an API key
            3. Add to `.env` file:
            ```
            GEMINI_API_KEY=your-key
            ```
            """)
    elif st.session_state.api_provider == "nvidia":
        if os.getenv("NVIDIA_API_KEY"):
            st.success("✅ NVIDIA API key detected")
        else:
            st.error("❌ NVIDIA API key missing")
            st.markdown("""
            **Get your key:**
            1. Visit [NVIDIA NIM](https://build.nvidia.com/)
            2. Create an API key
            3. Add to `.env` file:
            ```
            NVIDIA_API_KEY=your-key
            ```
            """)
    else:
        if os.getenv("OPENAI_API_KEY"):
            st.success("✅ OpenAI API key detected")
        else:
            st.error("❌ OpenAI API key missing")
            st.markdown("""
            **Add to `.env` file:**
            ```
            OPENAI_API_KEY=your-key
            ```
            """)
    
    st.markdown("---")
    
    # Model selection
    st.subheader("Choose a model", icon=":material/neurology:")
    
    if st.session_state.api_provider == "openrouter":
        st.markdown("**Free Models Available:**")
        
        popular_models = [
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "google/gemini-2.0-flash-exp:free",
            "meta-llama/llama-3.1-8b-instruct:free",
            "mistralai/mistral-7b-instruct:free",
            "qwen/qwen-2-7b-instruct:free",
        ]
        
        model = st.selectbox(
            "Choose a model:",
            options=popular_models,
            index=popular_models.index(st.session_state.active_model) if st.session_state.active_model in popular_models else 0,
        )
        
        # Allow custom model input
        with st.expander("🔧 Use custom model"):
            custom_model = st.text_input(
                "Enter model name:",
                placeholder="e.g., anthropic/claude-3.5-sonnet",
                help="Enter any model from OpenRouter. See: https://openrouter.ai/models",
            ).strip()
            
            if custom_model:
                model = custom_model
                st.info(f"Using custom model: {custom_model}")
    elif st.session_state.api_provider == "groq":
        st.markdown("**Groq Models:**")
        groq_models = [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
        ]
        model = st.selectbox(
            "Choose a model:",
            options=groq_models,
            index=groq_models.index(st.session_state.active_model)
            if st.session_state.active_model in groq_models
            else 0,
        )
        with st.expander("🔧 Use custom model"):
            custom_model = st.text_input(
                "Enter model name:",
                placeholder="e.g., openai/gpt-oss-20b",
                help="Enter any model available in the Groq Console.",
            ).strip()
            if custom_model:
                model = custom_model
                st.info(f"Using custom model: {custom_model}")
    elif st.session_state.api_provider == "gemini":
        st.markdown("**Gemini Models:**")
        gemini_models = [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash",
        ]
        model = st.selectbox(
            "Choose a model:",
            options=gemini_models,
            index=gemini_models.index(st.session_state.active_model)
            if st.session_state.active_model in gemini_models
            else 0,
        )
        with st.expander("🔧 Use custom model"):
            custom_model = st.text_input(
                "Enter model name:",
                placeholder="e.g., gemini-2.5-flash",
                help="Enter any model available in Google AI Studio.",
            ).strip()
            if custom_model:
                model = custom_model
                st.info(f"Using custom model: {custom_model}")
    elif st.session_state.api_provider == "nvidia":
        st.markdown("**NVIDIA NIM Models:**")
        nvidia_models = [
            "meta/llama-3.1-8b-instruct",
            "meta/llama-3.3-70b-instruct",
            "nvidia/llama-3.1-nemotron-ultra-253b-v1",
        ]
        model = st.selectbox(
            "Choose a model:",
            options=nvidia_models,
            index=nvidia_models.index(st.session_state.active_model)
            if st.session_state.active_model in nvidia_models
            else 0,
        )
        with st.expander("🔧 Use custom model"):
            custom_model = st.text_input(
                "Enter model name:",
                placeholder="e.g., meta/llama-3.1-8b-instruct",
                help="Enter any model available in NVIDIA NIM.",
            ).strip()
            if custom_model:
                model = custom_model
                st.info(f"Using custom model: {custom_model}")
    else:
        st.markdown("**OpenAI Models:**")
        openai_models = [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
        ]
        
        model = st.selectbox(
            "Choose a model:",
            options=openai_models,
            index=openai_models.index(st.session_state.active_model) if st.session_state.active_model in openai_models else 0,
        )
        
        # Allow custom model input
        with st.expander("🔧 Use custom model"):
            custom_model = st.text_input(
                "Enter model name:",
                placeholder="e.g., gpt-4-1106-preview",
                help="Enter any OpenAI model name",
            ).strip()
            
            if custom_model:
                model = custom_model
                st.info(f"Using custom model: {custom_model}")

    if model != st.session_state.active_model:
        st.session_state.active_model = model
        st.session_state.previous_response_id = None
        st.session_state.conversation_messages = []
        st.session_state.messages = []
        st.session_state.starter_prompt = None
        st.info("✅ Model changed. Conversation reset.")

    st.markdown("---")
    
    # Controls
    st.subheader("Conversation", icon=":material/forum:")
    
    if st.button(
        "Clear conversation",
        icon=":material/delete_sweep:",
        width="stretch",
    ):
        st.session_state.messages = []
        st.session_state.previous_response_id = None
        st.session_state.conversation_messages = []
        st.session_state.starter_prompt = None
        st.success("Conversation cleared!")
        st.rerun()
    
    st.markdown("---")
    
    # Info section
    with st.expander("About this workspace", icon=":material/info:"):
        st.markdown(f"""
        **Current setup**
        - Provider: `{st.session_state.api_provider.upper()}`
        - Model: `{st.session_state.active_model}`
        - Messages: {len(st.session_state.messages)}
        
        **Available providers**
        - Switch between OpenAI, OpenRouter, Groq, Gemini, and NVIDIA NIM
        - Explore models from each provider
        - Conversation history stays available until you clear it
        """)

if not st.session_state.messages:
    with st.container(border=True):
        st.subheader("Start with a thought, a question, or a rough idea.")
        st.write(
            "Your selected model can help you untangle a topic, shape a plan, "
            "or explore a new direction."
        )
        st.caption("Pick a starting point below, or write your own message.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Write a message...")

if not st.session_state.messages:
    suggestions = {
        "Explain something simply": (
            "Explain a complex topic in simple terms, with a clear example."
        ),
        "Plan a small project": (
            "Help me turn a project idea into a practical step-by-step plan."
        ),
        "Find a fresh perspective": (
            "Give me three unexpected perspectives on a topic I care about."
        ),
    }
    selected_suggestion = st.pills(
        "Try a starting point",
        options=list(suggestions),
        key="starter_prompt",
        label_visibility="collapsed",
        width="stretch",
        wrap=True,
    )
    if selected_suggestion:
        prompt = suggestions[selected_suggestion]

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Get the generate_response function with current provider
                generate_response = get_generate_response(st.session_state.api_provider)
                
                if st.session_state.api_provider in {"openrouter", "groq", "gemini", "nvidia"}:
                    # For OpenRouter, pass the full conversation history
                    answer, response_id = generate_response(
                        prompt,
                        model=st.session_state.active_model,
                        previous_messages=st.session_state.conversation_messages.copy(),
                    )
                    # Update conversation history
                    st.session_state.conversation_messages.append(
                        {"role": "user", "content": prompt}
                    )
                    st.session_state.conversation_messages.append(
                        {"role": "assistant", "content": answer}
                    )
                else:
                    # For OpenAI, use chat completions (since Responses API may not be available)
                    from openai import OpenAI
                    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    
                    # Build messages for OpenAI
                    messages = st.session_state.conversation_messages.copy()
                    messages.append({"role": "user", "content": prompt})
                    
                    response = client.chat.completions.create(
                        model=st.session_state.active_model,
                        messages=messages,
                    )
                    
                    answer = response.choices[0].message.content
                    response_id = response.id
                    
                    # Update conversation history
                    st.session_state.conversation_messages.append(
                        {"role": "user", "content": prompt}
                    )
                    st.session_state.conversation_messages.append(
                        {"role": "assistant", "content": answer}
                    )
            
            st.markdown(answer)

        # Add assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
        st.session_state.previous_response_id = response_id

    except Exception as exc:
        st.error(f"❌ Error: {type(exc).__name__}: {exc}")
        st.info("Check your API key and model selection in the sidebar.")
