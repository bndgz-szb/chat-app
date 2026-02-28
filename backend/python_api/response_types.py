from dataclasses import dataclass
from typing import List

from db.models import Topic


@dataclass
class LoginResponse():
    access_token: str
    username: str
    user_id: int
    is_admin: bool


@dataclass
class TaskWithTopic():
    id: int
    name: str
    created_by: int
    done: bool
    topics: List[Topic]
    chat_id: int | None
