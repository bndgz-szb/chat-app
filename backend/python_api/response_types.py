from dataclasses import dataclass


@dataclass
class LoginResponse():
    access_token: str
    username: str
    user_id: int
