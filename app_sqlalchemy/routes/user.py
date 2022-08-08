from fastapi import Depends, Response, status, HTTPException, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils


router = APIRouter()


@router.get(path="/sqlalchemy/users", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@router.get(path="/sqlalchemy/users/{_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_users(_id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == _id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {_id} does not exist"
        )

    return user


@router.post("/sqlalchemy/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_request: schemas.CreateUser, db: Session = Depends(get_db)):
    new_user = db.query(models.User).filter(models.User.email == user_request.email.strip()).first()

    if new_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="email already taken"
        )

    user_request = utils.pwd_hash_middleware(user_request=user_request)
    new_user = models.User(**user_request.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
