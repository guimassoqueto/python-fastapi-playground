from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

# help imports
from datetime import datetime
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sqlalchemy/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.post("/sqlalchemy/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post_request: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post_request.dict())

    # add the new_post to the database
    db.add(new_post)
    # commit the changes e insert the new_post into database
    db.commit()
    # retrieve the new_post created
    db.refresh(new_post)

    return new_post


@app.get("/sqlalchemy/posts/{_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(_id: int, db: Session = Depends(get_db)):
    single_post = db.query(models.Post).filter(models.Post.id == _id).first()
    
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={_id} not found")

    return single_post


@app.delete("/sqlalchemy/posts/{_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(_id: int,  db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == _id)

    if not deleted_post.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} doesn't exist")

    deleted_post.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/sqlalchemy/posts/{_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(_id: int, post_request: schemas.UpdatePost, db: Session = Depends(get_db)):
    changed_post = db.query(models.Post).filter(models.Post.id == _id)

    post_request = post_request.dict()
    post_request['updated_at'] = datetime.now().isoformat()

    if not changed_post: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {_id} was not found"
        )

    changed_post.update(post_request, synchronize_session="TRUE")
    db.commit()

    return changed_post.first()


@app.get(path="/sqlalchemy/users", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@app.post("/sqlalchemy/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_request: schemas.CreateUser, db: Session = Depends(get_db)):
    new_user = db.query(models.User).filter(models.User.email == user_request.email.strip()).first()

    if new_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="email already taken"
        )

    hashed_password = password_context.hash(user_request.password)
    user_request.password = hashed_password
    new_user = models.User(**user_request.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
