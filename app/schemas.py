from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True # this is so that sqlalchemy results are treated as dict type

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# FastAPI will validate data automatically based on a model
class PostBase(BaseModel):
    title: str # see field types in pydantic documentation
    content: str
    published: bool = True #default value

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True # this is so that sqlalchemy results are treated as dict type

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)