from fastapi import FastAPI
from db.crud.auth import create_user
from db.session import SessionLocal
from python_api.auth import get_password_hash, create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

app = FastAPI()


@app.post("/register")
def register(username: str, email: str, password: str):
    with SessionLocal() as session:
        # check email validity
        # check if username and email are unique
        # check password validity
        user = create_user(session=session, username=username, email=email, hashed_password=get_password_hash(password))
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return Token(token_type="bearer", access_token=access_token)
