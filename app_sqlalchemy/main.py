from fastapi import FastAPI
from . import models
from .database import engine
from .routes import post, user


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router=post.router)
app.include_router(router=user.router)
