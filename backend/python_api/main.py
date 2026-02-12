import uvicorn
from fastapi import FastAPI
from db.crud.auth import create_user
from db.session import SessionLocal
from python_api.auth import get_password_hash

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/register")
def register(username: str, email: str, password: str):
    with SessionLocal() as session:
        # check email validity
        # check if username and email are unique
        # check password validity
        # save data in db
        user = create_user(session=session, username=username, email=email, hashed_password=get_password_hash(password))
        # return bearer token for login
        return user
