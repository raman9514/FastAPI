from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str
    user_id: int

# Responce Model

# works
# class BlogResponceModel(Blog):
#     pass

# works
# class BlogResponceModel(Blog):
#     class Config():
#         orm_mode = True


class User(BaseModel):
    email: str
    hashed_password: str
    is_active: bool


class BlogResponceModel(BaseModel):
    title: str
    creator: User


class UserResponceModel(BaseModel):
    email: str
    is_active: bool
    blogs: List[Blog]


class Auth(BaseModel):
    email: str
    password: str
