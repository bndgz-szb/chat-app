from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from python_api.routers import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # use fix ip address of frontend and ws server in prod
    allow_origins=["http://localhost:3000", "http://localhost:8765"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Origin", "authorization"]
)


app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(topics_router)
app.include_router(chat_router)
app.include_router(admin_router)
