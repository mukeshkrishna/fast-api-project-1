from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models, schemas, utils
from sqlalchemy.orm import Session
from app.database import engine, get_db
from typing import Optional, List


# this told the sql-achemy to create all the tables, we can remove it as we will be using alembic
# models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# while True:
#     try:
#         # create postgres connection
#         # cursor_factory=RealDictCursor - this gives the column name, and returns a python dictionary
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connecting to Database Failed")
#         print("Error: ", error)
#         time.sleep(5) # sleep for 5 seconds
#
# my_posts = [{"id": 1,"title": "title of post 1", "content": "content of post 1"},
#             {"id": 2,"title": "title of post 2", "content": "content of post 2"}]
#
#
# def find_post(id):
#     posts = my_posts
#     for post in posts:
#         if post["id"] == id:
#             return post
#
#
# def find_index_post(id):
#     posts = my_posts
#     for index, post in enumerate(posts):
#         if post["id"] == id:
#             return index


@router.post("", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with {id} does not exist")
    return user