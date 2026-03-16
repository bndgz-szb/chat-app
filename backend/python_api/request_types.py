from pydantic import BaseModel
from typing import List

from db.crud.task import TaskParticipant


class Topic(BaseModel):
    id: int
    name: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateTaskRequest(BaseModel):
    name: str
    done: bool
    topics: List[Topic]
    participants: List[TaskParticipant]
