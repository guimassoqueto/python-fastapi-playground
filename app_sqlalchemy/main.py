from fastapi import FastAPI, Depends
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sqlalchemy")
def get_something(db: Session = Depends(get_db)):
    return {
        "balada": "top"
    }