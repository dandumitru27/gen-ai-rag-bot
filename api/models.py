from pydantic import BaseModel


class PostRequest(BaseModel):
    human_message: str


class PostResponse(BaseModel):
    ai_message: str
