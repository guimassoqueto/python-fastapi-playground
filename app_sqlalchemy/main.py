from fastapi import FastAPI, Depends
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/sqlalchemy")
def get_something(db: Session = Depends(get_db)):

    return {
        "balada": "top"
    }