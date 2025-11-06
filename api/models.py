from pydantic import BaseModel


class PostRequest(BaseModel):
    human_message: str
    thread_id: str | None = None


class PostResponse(BaseModel):
    ai_message: str
    thread_id: str
