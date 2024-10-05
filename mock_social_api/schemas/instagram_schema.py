from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class IComment(BaseModel):
    username: str  # The username of the person who made the comment
    content: str  # The content of the comment
    timestamp: datetime  # When the comment was posted

# Define a model for Post
class IPost(BaseModel):
    content: str
    hashtags: list[str] = []
    timestamp: datetime
    likes: int
    link: Optional[HttpUrl] = None  # Optional if not all posts have a link
    comments: list[IComment] = []  # Assuming comments are a list of strings

# Define a model for Story
class IStory(BaseModel):
    content: str
    hashtags: list[str] = []
    timestamp: datetime
    likes: int

# Define a model for User
class IUser(BaseModel):
    stories: list[IStory] = []
    posts: list[IPost] = []
    private: bool
    followers: int