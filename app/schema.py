from datetime import datetime
from typing import Optional
from pydantic import BaseModel , EmailStr
from pydantic.types import conint


class UserBase(BaseModel):
    email: EmailStr
    
 

class UserCreate(UserBase):
     password: str


class User(UserBase):
       id : int
       created_at : datetime

       class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type: str


class TokenData(BaseModel):
    id : Optional[int]= None


class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

class Post(PostBase):
    published: bool
    id : int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class Vote(BaseModel):
    post_id:int
    dir : conint(le=1) 




# class Post(BaseModel):
#     title : str
#     content: str
#     published: bool = True


# class PostUpdate(BaseModel):
#     title : str
#     content: str
#     published: bool


# class PostCreate(BaseModel):
#     title : str
#     content: str
#     published: bool
