from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta

from db.crud.user import create_user, get_user_by_username, get_user_by_email
from db.session import SessionLocal
from python_api.auth import get_password_hash, create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # TODO use fix ip address of frontend
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Origin"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/register")
def register(username: str, email: str, password: str):
    with SessionLocal() as session:
        # check email validity
        # check password validity
        user = get_user_by_username(session, username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        user = get_user_by_email(session, email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )

        create_user(session=session, username=username, email=email, hashed_password=get_password_hash(password))
        return "Account successfully registered."

@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(token_type="bearer", access_token=access_token)
