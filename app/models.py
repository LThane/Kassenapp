import reflex as rx
from sqlmodel import Field, SQLModel
from typing import TypedDict, Optional
from datetime import datetime


class Member(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str


class Cost(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str]
    amount: float
    date: str
    category: str
    member_id: int = Field(foreign_key="member.id")


class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    member_id: int = Field(foreign_key="member.id")
    message: str
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CostWithMember(TypedDict):
    id: int
    description: str
    amount: float
    date: str
    category: str
    member_id: int
    member_name: str


class RegisterForm(TypedDict):
    name: str
    email: str
    password: str


class LoginForm(TypedDict):
    email: str
    password: str


class CostForm(TypedDict):
    description: Optional[str]
    amount: Optional[str]
    date: str
    category: str