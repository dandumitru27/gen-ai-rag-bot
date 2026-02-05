from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_docling import DoclingLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import InMemorySaver

provider = "google_genai"  # "google_genai" / "openai"
vector_store_provider = "chroma"  # "chroma" / "in_memory"
load_docs_in_vector_store_on_startup = (
    False  # change to False if you use Chroma and have already loaded docs
)

vector_store = None


def init_model():
    load_dotenv()

    if provider == "google_genai":
        model = init_chat_model("google_genai:gemini-2.5-flash")
    elif provider == "openai":
        model = init_chat_model("gpt-5-mini")
    return model


def configure_agent():
    model = init_model()

    global vector_store
    vector_store = init_vector_store()

    if load_docs_in_vector_store_on_startup:
        load_documents_to_vector_store()

    tools = [retrieve_context]

    system_prompt = load_system_prompt()

    agent = create_agent(
        model, tools, checkpointer=InMemorySaver(), system_prompt=system_prompt
    )

    return agent


def load_documents_to_vector_store():
    documents = load_source_documents()
    splits = split_documents(documents)

    # filter out complex metadata that Chroma doesn't support
    filtered_splits = filter_complex_metadata(splits)

    vector_store.add_documents(filtered_splits)


def init_vector_store():
    if provider == "google_genai":
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    elif provider == "openai":
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    if vector_store_provider == "chroma":
        return Chroma(
            embedding_function=embeddings,
            persist_directory="./api/chroma_langchain_db",
        )
    else:
        return InMemoryVectorStore(embeddings)


def load_source_documents():
    document_type = "pdf"  # "markdown" / "pdf"

    if document_type == "markdown":
        loader = DirectoryLoader(
            path="./api/documents/markdown",
            loader_cls=TextLoader,
        )
    elif document_type == "pdf":
        loader = DirectoryLoader(
            path="./api/documents/pdf",
            loader_cls=DoclingLoader,
        )

    return loader.load()


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,  # track index in original document
    )

    return text_splitter.split_documents(documents)


@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""

    retrieved_docs = vector_store.similarity_search(query, k=2)

    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )

    return serialized, retrieved_docs


def load_system_prompt():
    with open(f"./api/system_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()
