# OpenRouter Setup Guide

## What Changed?

Your application now supports **five API providers**:
1. **OpenAI** - Original OpenAI API
2. **OpenRouter** - Access to multiple AI models through one API
3. **Groq** - Fast inference through the Groq API
4. **Gemini AI Studio** - Google's Gemini API
5. **NVIDIA NIM** - NVIDIA's hosted model API

## Quick Setup

### 1. Get Your OpenRouter API Key

1. Visit: https://openrouter.ai/keys
2. Sign up or log in
3. Click "Create Key"
4. Copy your API key (starts with `sk-or-v1-...`)

### 2. Update Your `.env` File

Open `.env` and add your OpenRouter API key:

```env
# API Provider: "openai" or "openrouter"
API_PROVIDER=openrouter

# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free

# Optional: For OpenRouter rankings
OPENROUTER_SITE_URL=http://localhost:8502
OPENROUTER_SITE_NAME=ChatSynth
```

### 3. Restart the Application

```bash
streamlit run ChatSynth.py
```

## Switching Between Providers

### Use OpenRouter (Default)
```env
API_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
```

### Use OpenAI
```env
API_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
```

### Use Groq
```env
API_PROVIDER=groq
GROQ_API_KEY=gsk_...
GROQ_MODEL=openai/gpt-oss-20b
```

Create a Groq key at [console.groq.com/keys](https://console.groq.com/keys).

### Use Gemini AI Studio
```env
API_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash
```

Create a Gemini key at [Google AI Studio](https://aistudio.google.com/apikey).

### Use NVIDIA NIM
```env
API_PROVIDER=nvidia
NVIDIA_API_KEY=your-nvidia-api-key
NVIDIA_MODEL=meta/llama-3.1-8b-instruct
```

Create a key at [NVIDIA NIM](https://build.nvidia.com/).

## Available Free Models on OpenRouter

The app includes these popular **FREE** models:

1. **nvidia/nemotron-3-ultra-550b-a55b:free** - NVIDIA's powerful reasoning model
2. **google/gemini-2.0-flash-exp:free** - Google's fast Gemini model
3. **meta-llama/llama-3.1-8b-instruct:free** - Meta's Llama 3.1
4. **mistralai/mistral-7b-instruct:free** - Mistral AI's model
5. **qwen/qwen-2-7b-instruct:free** - Alibaba's Qwen model

You can also enter any custom model from the [OpenRouter models page](https://openrouter.ai/models).

## Features

✅ **Provider switching** - Choose between OpenAI and OpenRouter
✅ **Multiple models** - Access dozens of AI models through OpenRouter
✅ **Free models** - Many models available for free
✅ **Conversation history** - Maintains context across messages
✅ **Model selection** - Choose from popular models or enter custom ones
✅ **Easy configuration** - All settings in `.env` file

## Model Selection in UI

The sidebar now shows:
- Current API provider
- Model selection dropdown (for OpenRouter)
- Custom model input field
- API key status

## Troubleshooting

### "OPENROUTER_API_KEY not set"
- Make sure your `.env` file has `OPENROUTER_API_KEY=sk-or-v1-...`
- Restart the Streamlit app

### "API request failed"
- Check your API key is valid
- Verify the model name is correct
- Check your OpenRouter account has credits (free models don't need credits)

### "429 Too Many Requests"
This is an OpenRouter rate-limit response. Free-model requests are subject to
per-minute and daily limits, and the limit can apply across free models rather
than only to the model selected in the app. Wait until the reset time shown by
the app, or switch to OpenAI or a paid OpenRouter model. Adding credits can
increase the free-model quota according to OpenRouter's current limits.

### Want to use a different model?
- Visit https://openrouter.ai/models
- Copy the model ID (e.g., `openai/gpt-4`)
- Paste it in the "custom model" field in the sidebar

## Cost Information

- **Free models** - Many models are completely free (marked with `:free`)
- **Paid models** - Some models require credits, check pricing at https://openrouter.ai/models
- Your OpenRouter dashboard shows your usage and costs

## Benefits of OpenRouter

1. **One API key** - Access multiple AI providers
2. **Model variety** - GPT, Claude, Gemini, Llama, and more
3. **Free options** - Many powerful free models
4. **Fallback support** - Automatically try alternative models if one fails
5. **Usage tracking** - Built-in analytics dashboard

## Links

- OpenRouter Dashboard: https://openrouter.ai/
- API Keys: https://openrouter.ai/keys
- Model List: https://openrouter.ai/models
- Documentation: https://openrouter.ai/docs
