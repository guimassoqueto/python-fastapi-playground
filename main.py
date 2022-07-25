from hashlib import new
from random import randint
from fastapi import Body, FastAPI

app = FastAPI()

all_posts = [
    {
        "id": 1,
        "title": "Post1",
        "description": "Description1"
    },
    {
        "id": 2,
        "title": "Post2",
        "description": "Description1"    
    }
]

@app.get("/")
def root():
    return {"message": "Hello Gay"}


@app.get("/posts")
def get_posts():
    return {"data": all_posts}


## Schemas


from pydantic import BaseModel
from typing import Optional, Union


class Post(BaseModel):
    title: str
    description: Optional[str] = None


@app.post("/posts")
def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randint(1, 1_000_000)
    all_posts.append(post_dict)

    return {
        "new_post": "Post created",
        "all_posts": all_posts
    }

@app.get("/posts/latest")
def get_latest():
    return {"latest post": all_posts[-1]}


## URL PARAMS
@app.get("/posts/{id}")
def get_posts(id: int):
    return {"data": f"retrieving post {id}"}