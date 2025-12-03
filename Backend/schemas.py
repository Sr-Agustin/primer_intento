from pydantic import BaseModel, EmailStr
from Backend.models import User
from pydantic import BaseModel

class TokenData(BaseModel):
    email: str | None = None

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
