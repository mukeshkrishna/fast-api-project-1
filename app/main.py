from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, users, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # this tells, our API/server is globally accessible from all website, and there will be no CORS error


# middleware is a function that will run before every request call.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # what domains that are allowed to talk to our API/server
    allow_credentials=True,
    allow_methods=["*"], # what HTTP Methods allowed, like POST, PUT, PATCH, DELETE etc
    allow_headers=["*"], # What headers to allow
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}
