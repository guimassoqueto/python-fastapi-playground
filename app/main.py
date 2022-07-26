from hashlib import new
from random import randint
from fastapi import Body, FastAPI, HTTPException, status, Response, responses

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

def find_post(id: int):
    for index, post in enumerate(all_posts):
        if post['id'] == id: return (index, post)
    return (-1, None)

@app.get("/")
def root():
    return {"message": "Hello Gay"}


@app.get("/posts")
def get_posts():
    return {"data": all_posts}


## SCHEMAS

from pydantic import BaseModel
from typing import Optional, Union


class Post(BaseModel):
    title: str
    description: Optional[str] = None


@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
def get_post(id: int):
    _, post = find_post(id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} was not found"
        )

    return {"data": post}


## DELETE

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index, post_to_delete = find_post(id)
    
    if not post_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} was not found"
        )

    all_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


## PUT

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def put_post(id: int, updated_post: Post):
    index, _ = find_post(id)
    if index == -1: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {id} was not found"
        )
    
    new_post = updated_post.dict()
    new_post["id"] = id
    all_posts[index] = new_post

    return {
        "message": "post updated",
        "data": updated_post
    }