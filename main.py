from fastapi import FastAPI
from routers import chat
import models
from database import base,engine

base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(chat.router)

