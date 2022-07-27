from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sqlalchemy/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.post("/sqlalchemy/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def post_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/sqlalchemy/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def post_post(id: int, db: Session = Depends(get_db)):
    single_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} not found")

    return single_post


@app.delete("/sqlalchemy/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if not deleted_post.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} doesn't exist")

    deleted_post.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/sqlalchemy/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def put_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
    changed_post = db.query(models.Post).filter(models.Post.id == id)

    if not changed_post: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {id} was not found"
        )

    changed_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return changed_post.first()