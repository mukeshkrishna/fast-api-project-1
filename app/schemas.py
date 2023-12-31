from pydantic import BaseModel, EmailStr
from datetime import  datetime
from typing import Optional
from pydantic.types import conint

#this Post class extends from BaseModel from pydantic module, which is used to define our data schema.
# this is defining the data of the request.


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#
# class PostUpdate(BaseModel):
#     title: str
#     content: str
#     published: bool
#
# class PostCreate(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# User schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# this inherits all the fields from PostBase
class PostCreate(PostBase):
    pass


# this inherits all the fields from PostBase
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True



class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # this will support less than or equal to 1.

