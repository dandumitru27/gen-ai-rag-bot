from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver


def init_model():
    load_dotenv()

    provider = "google_genai"  # "google_genai" / "openai"

    if provider == "google_genai":
        model = init_chat_model("google_genai:gemini-2.5-flash")
    elif provider == "openai":
        model = init_chat_model("gpt-5-mini")
    return model


def load_system_prompt():
    base = Path(__file__).resolve().parent

    with open(f"{base}/system_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()


def configure_agent():
    model = init_model()

    system_prompt = load_system_prompt()

    agent = create_agent(
        model, checkpointer=InMemorySaver(), system_prompt=system_prompt
    )

    return agent
