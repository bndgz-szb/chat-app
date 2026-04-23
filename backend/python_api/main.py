from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from python_api.routers import *

tags_metadata = [
	{
        "name": "Users",
        "description": "Endpoints related to the user table"
    },
	{
		"name": "Tasks",
		"description": "Endpoints related to the task table"
    },
	{
		"name": "Topics",
		"description": "Endpoints related to the topic table"
    },
	{
		"name": "Chat",
		"description": "Endpoints related to the chat feature"
    },
	{
		"name": "Admin",
		"description": "Endpoints only accessible to the admin"
    }
]

app = FastAPI(openapi_tags=tags_metadata)

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
