from pydantic import BaseModel, EmailStr
from Backend.models import User
from pydantic import BaseModel
from datetime import date, time

# -------------------------
# USER SCHEMAS
# -------------------------

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


# -------------------------
# APPOINTMENT SCHEMAS
# -------------------------

class AppointmentBase(BaseModel):
    date: date
    time: time
    status: str | None = "pending"

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

