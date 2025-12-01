from enum import StrEnum
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Gender(StrEnum):
    Male = "male"
    Female = "female"


class Role(StrEnum):
    Principal = "principal"
    Worker = "worker"
    User = "user"


class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="User Name")
    age: int = Field(..., ge=6, le=60, description="User Age")
    gender: Gender = Field(default=Gender.Male, description="User Gender")
    email: EmailStr = Field(..., description="User Email")
    password: str = Field(..., min_length=8, description="User Password")
    role: Role = Field(default=Role.User, description="User Role")


class UserID(User):
    user_id: int = Field(..., description="User ID")


class UserEnter(User):
    pass


class UserUpdate(BaseModel):
    """Model for updating user - all fields are optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="User name")
    age: Optional[int] = Field(None, ge=6, le=60, description="User age")
    gender: Optional[Gender] = Field(None, description="User Gender")
    email: Optional[EmailStr] = Field(None, description="User Email")
    password: Optional[str] = Field(None, min_length=8, description="User Password")
    role: Optional[Role] = Field(None, description="User Role")


class UserResponse(BaseModel):
    """Model for user responses - excludes password for security"""
    user_id: int = Field(..., description="User ID")
    name: str = Field(..., min_length=1, max_length=50, description="User Name")
    age: int = Field(..., ge=6, le=60, description="User Age")
    gender: Gender = Field(default=Gender.Male, description="User Gender")
    email: EmailStr = Field(..., description="User Email")
    role: Role = Field(default=Role.User, description="User Role")