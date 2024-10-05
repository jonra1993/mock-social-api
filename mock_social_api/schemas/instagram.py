from pydantic import BaseModel


class StoryCheckRequest(BaseModel):
    username: str
    hashtag: str

class StoryCheckResponse(BaseModel):
    result: str