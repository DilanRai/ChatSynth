# ChatSynth — Multi-Provider AI Chat Web Application

A modern, responsive Streamlit chat application featuring **real-time visual provider switching** between OpenAI, OpenRouter, Groq, Google Gemini, and NVIDIA NIM APIs. Access dozens of state-of-the-art AI models through a clean, elegant graphical interface with zero configuration reloads.

---

## ✨ Features

- **🎛️ Real-Time GUI Provider Switching**: Switch between 5 different AI providers instantly from the sidebar radio buttons without restarting the application or modifying `.env`.
- **⚡ 5 Supported AI Providers**:
  - **OpenRouter**: Access 100+ models (including top free-tier models like Nemotron, Llama 3.3, and Mistral).
  - **Groq**: Ultra-low latency inference powered by LPU hardware (Llama 3.3 70B, Llama 3.1 8B, Mixtral).
  - **Google Gemini**: Direct access to Gemini 2.5 Flash, Gemini 2.0 Flash, and Gemini 1.5 Pro via Google AI Studio.
  - **NVIDIA NIM**: Enterprise-grade open models hosted on NVIDIA's accelerated cloud infrastructure.
  - **OpenAI**: Native support for GPT-4, GPT-4o, and GPT-3.5 series models.
- **🧠 Dynamic Model Dropdowns**: Each provider dynamically displays its popular models with an option for custom model IDs.
- **🟢 Live Key Detection Badges**: Instant visual feedback showing whether the required API key for the selected provider is detected.
- **🎨 Modern Dual Theme**: Clean workspace with customized light and dark theme styling, message statistics, and status pills.
- **💬 Chat History Management**: Persistent multi-turn conversation memory within your session and one-click chat clearing.
- **💡 Quick-Start Prompts**: Contextual starter prompts to quickly spark ideas and test models.

---

## 🚀 Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/DilanRai/ChatSynth.git
cd ChatSynth
```

### 2. Set Up Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your API Keys

Copy `.env.example` to `.env`:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

Open `.env` and fill in the keys for any providers you want to use (you do **not** need all keys to get started — any single provider works):

```env
# Free models available via OpenRouter (https://openrouter.ai/keys)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Ultra-fast models via Groq (https://console.groq.com/keys)
GROQ_API_KEY=gsk_your-key-here

# Google Gemini via AI Studio (https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your-gemini-key-here

# NVIDIA NIM (https://build.nvidia.com/)
NVIDIA_API_KEY=nvapi-your-key-here

# OpenAI (https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-proj-your-key-here
```

### 5. Launch the Application

```bash
streamlit run ChatSynth.py
```

Open your browser at `http://localhost:8501`.

---

## 🔌 Supported Providers & Setup

| Provider | Best For | Free Tier Available? | API Key Portal |
| :--- | :--- | :---: | :--- |
| **OpenRouter** | 100+ models, multi-model flexibility |  Yes (e.g. Nemotron, Llama 3.3) | [openrouter.ai/keys](https://openrouter.ai/keys) |
| **Groq** | Blazing-fast inference speeds |  Yes (Generous free tier) | [console.groq.com/keys](https://console.groq.com/keys) |
| **Google Gemini** | Massive context window, multimodal |  Yes (Free rate limits) | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| **NVIDIA NIM** | Leading open-weight foundation models |  Yes (Free initial credits) | [build.nvidia.com](https://build.nvidia.com/) |
| **OpenAI** | Flagship GPT-4o / GPT-4 models | Paid (Pay-as-you-go) | [platform.openai.com](https://platform.openai.com/api-keys) |

> For extended instructions on OpenRouter free models and rankings, see [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md).

---

## 🏗️ Architecture

```text
Streamlit UI (ChatSynth.py)
   │
   ├── Sidebar: Provider selector, Model picker, Status badges
   ├── Main Chat: Message container, Quick prompt pills, Input bar
   │
   ▼
Service Layer (openai_service.py)
   │
   ├── OpenRouter: HTTP API endpoint with streaming & rate limit handling
   ├── Groq: OpenAI-compatible client
   ├── Gemini: Google OpenAI-compatible endpoint
   ├── NVIDIA NIM: NVIDIA OpenAI-compatible endpoint
   └── OpenAI: OpenAI Chat Completions SDK
```

---

## 🧪 Testing

Run the offline unit test suite:

```bash
python -m unittest discover tests
```

Validate code syntax:

```bash
python -m compileall -q .
```

---

## 🔒 Security Best Practices

- **Never commit `.env`**: Your `.gitignore` automatically prevents `.env` and local secrets from being checked into version control.
- **Zero Hardcoded Secrets**: All API calls read securely from environment variables.
- **Safe Unit Tests**: Test suite uses mock clients and makes zero live billable network calls.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
