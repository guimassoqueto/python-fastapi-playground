from hashlib import new
from random import randint
from fastapi import Body, FastAPI, HTTPException, status, Response, responses
from .db_conn import cursor, conn

## Init FastAPI 

app = FastAPI()

all_posts = [
    {
        "id": 1,
        "title": "Post1",
        "content": "content1"
    },
    {
        "id": 2,
        "title": "Post2",
        "content": "content1"    
    }
]

def find_post(id: int):
    for index, post in enumerate(all_posts):
        if post['id'] == id: return (index, post)
    return (-1, None)

## BASIC GET
@app.get("/")
def root():
    return {"message": "Hello Gay"}

## GET FROM DB

@app.get("/posts")
def get_posts():
    cursor.execute(''' 
        SELECT * FROM posts;
    ''')
    posts_from_database = cursor.fetchall()

    return {"data": posts_from_database}


## SCHEMAS WITH DATABASE

from pydantic import BaseModel
from typing import Optional, Union


class Post(BaseModel):
    title: str
    content: Optional[str] = None


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(req_body: Post):
    cursor.execute('''
        INSERT INTO 
            posts(title, content)
        VALUES
            (%s, %s)
        RETURNING *;
    ''', (req_body.title, req_body.content))

    new_post = cursor.fetchone()
    conn.commit()

    return {
        "message": "Post Created sucessfully",
        "data": new_post
    }


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute('''
        SELECT * FROM posts ORDER BY created_at DESC LIMIT 1;
    ''')
    last_post = cursor.fetchone()

    return {
        "message": "Last post successfully retrieved",
        "data": last_post
    }


## URL PARAMS

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute('''
        SELECT * FROM posts WHERE id=%s; 
    ''', (str(id),))

    post_by_id_from_db = cursor.fetchall()

    if not post_by_id_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} was not found"
        )

    return {
        "message": "Post sucessfuly retrieved",
        "data": post_by_id_from_db
    }


## DELETE

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''
        DELETE FROM posts
        WHERE id=%s
        RETURNING *
    ''', (str(id),))
    
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {id} was not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


## PUT

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def put_post(id: int, post: Post):
    cursor.execute('''
        UPDATE posts
        SET title=%s, content=%s
        WHERE id=%s
        RETURNING *;
    ''', (post.title, post.content, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {id} was not found"
        )

    return {
        "message": "post updated",
        "data": updated_post
    }