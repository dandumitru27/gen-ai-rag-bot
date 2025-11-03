from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from llm_graph import create_llm_graph, init_llm
from models import PostRequest, PostResponse

graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global graph
    graph = create_llm_graph()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hello")
def read_item():
    llm = init_llm()

    ai_message = llm.invoke(
        "Who's your maker? Also, tell me the name of an interesting historic moment from a random century. "
        "Pick a random number from 1 to 41, then with its index pick a century from 20th century BC to 21st century AD."
    )

    return ai_message.content


@app.post("/chat")
async def reply_chat_message(request: PostRequest):
    config = {"configurable": {"thread_id": "abc123"}}

    output = graph.invoke({"messages": [request.human_message]}, config)

    ai_message = output["messages"][-1]

    print(ai_message.content)

    return PostResponse(ai_message=ai_message.content)
