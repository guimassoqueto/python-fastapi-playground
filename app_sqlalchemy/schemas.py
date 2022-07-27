from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: Optional[str] = None
    published: Optional[bool] = True