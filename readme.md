# gen-ai-rag-bot

GenAI bot to perform RAG on local documents, using Gemini or GPT-5. API with Python, FastAPI, and LangChain, front-end with React, Next.js, and Chatbotify. Work in progress.

## Configurations

In `agent.py` you can change:

LLM Provider: Google Gemini or OpenAI

Vector Store: Chroma (local) or InMemory

## Start API and bot-ui

fastapi dev api/main.py

\bot-ui> npm run dev

## Initial setup

~ new virtual environment  
py -3.10 -m venv .venv

~ activate env  
.venv\Scripts\activate.bat

~ install all dependencies  
poetry install

## Helpful commands

~ add new package  
poetry add package-name
