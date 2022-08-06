from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# Posts
class BasePost(BaseModel):
    title: str
    content: Optional[str] = None
    published: Optional[bool] = True


class CreatePost(BasePost):
    pass


class UpdatePost(BasePost):
    pass


class Post(BasePost):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Users
class BaseUser(BaseModel):
    email: str
    password: str


class CreateUser(BaseUser):
    pass


class User(BaseModel):
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
