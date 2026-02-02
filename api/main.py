import uuid
from random import randint

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from api.agent import configure_agent, init_model
from api.models import PostRequest, PostResponse

agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent
    agent = configure_agent()
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
def healthcheck():
    return {"Health": "OK"}


@app.get("/intro")
def run_intro_query():
    model = init_model()

    century = randint(1, 21)
    ad_bc = "AD" if randint(1, 2) == 1 else "BC"

    ai_message = model.invoke(
        f"Who's your maker? Also, tell me in a sentence about an interesting historic moment from the {century}th century {ad_bc}."
    )

    return ai_message.content


@app.post("/chat")
async def reply_chat_message(request: PostRequest):
    thread_id = request.thread_id

    if not thread_id or thread_id == "":
        thread_id = str(uuid.uuid4())[:8]

    config = {"configurable": {"thread_id": thread_id}}

    output = agent.invoke({"messages": [request.human_message]}, config)

    ai_message = output["messages"][-1].content

    print(ai_message)

    if isinstance(ai_message, str):
        ai_message_text = ai_message
    else:
        ai_message_text = ai_message[0]["text"]

    return PostResponse(ai_message=ai_message_text, thread_id=thread_id)
