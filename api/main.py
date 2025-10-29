from fastapi import FastAPI
from init_llm import init_llm

app = FastAPI()


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
