from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


def init_llm():
    load_dotenv()

    provider = "google_genai"  # "google_genai" / "openai"

    if provider == "google_genai":
        llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    elif provider == "openai":
        llm = init_chat_model("gpt-5-mini", model_provider="openai")

    return llm
