from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


def init_llm():
    load_dotenv()

    provider = "google_genai"  # "google_genai" / "openai"

    if provider == "google_genai":
        llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    elif provider == "openai":
        llm = init_chat_model("gpt-5-mini", model_provider="openai")

    return llm


def create_llm_graph():
    llm = init_llm()

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Esti un asistent care raspunde la intrebarile clientilor. "
                "Vorbeste in limba romana si raspunde scurt, intr-un singur paragraf.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    workflow = StateGraph(state_schema=MessagesState)

    def call_model(state: MessagesState):
        prompt = prompt_template.invoke(state)
        response = llm.invoke(prompt)
        return {"messages": response}

    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    memory = MemorySaver()

    graph = workflow.compile(checkpointer=memory)
    return graph
