from turtle import title
from fastapi import FastAPI, Depends, Response, status, HTTPException
from requests import delete
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .schemas import Post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sqlalchemy/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {
        "data": posts
    }


@app.post("/sqlalchemy/posts", status_code=status.HTTP_201_CREATED)
def post_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "data": new_post
    }


@app.get("/sqlalchemy/posts/{id}", status_code=status.HTTP_200_OK)
def post_post(id: int, db: Session = Depends(get_db)):
    post_from_db = db.query(models.Post).filter(models.Post.id == id).all()
    
    if not post_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} not found")

    return {
        "data": post_from_db
    }


@app.delete("/sqlalchemy/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if not deleted_post.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} doesn't exist")

    deleted_post.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/sqlalchemy/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def put_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_to_change = db.query(models.Post).filter(models.Post.id == id)

    if not post_to_change.all(): 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {id} was not found"
        )

    post_to_change.update(post.dict(), synchronize_session=False)
    db.commit()

    return {
        "message": "post updated",
        "data": post_to_change.all()
    }