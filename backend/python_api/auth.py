from pwdlib import PasswordHash
from pydantic import BaseModel


password_hash = PasswordHash.recommended()

# temp
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
	return password_hash.hash(password)

def get_user(username: str):
	if username in fake_users_db:
		user_dict = fake_users_db[username]
		return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
	user = get_user(username)
