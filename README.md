# Chat webapp BSc thesis

## Introduction

This is the program part of my BSc thesis that I developed with the help of the internet (documentations and forums) + ChatGPT (very little help in some frontend layouts and some basic methods in backend, every instance of AI generated code should be marked with comments). The main goal of the program was for me to try out different technologies and try to make them work together as best as I can.

Tech stack:
- React + Redux with TypeScript (frontend)
- Python using the websockets, FastAPI, SQLAlchemy libraries (backend)
- PostgreSQL (database)
- Docker Compose

Everything is containerized with Docker Compose, in a way that frontend and backend files are mounted to minimize container size. A volume is created for the database.
There is no complex networking set up, therefore only the host PC is available to message itself on different accounts. There are no security measures, everything is sent/stored in plain text (the user passwords are stored hashed). The WebSocket messages are in JSON format.

---

## WebSocket Message Format

All messages are sent as JSON. For example:

```json
{
  "msg_type": "message",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "sender_id": "1",
  "chat_id": "11",
  "content": "hi bob"
}
```

Other message types:

- `hello`: client saying hello and implicitly asking for message history in given chat
- `error`: structured error from server
- `history`: list of messages in given chat

(Definitions are at /backend/python_ws_server/chatapp/messages.py)

## Components

### Frontend

- accessible on localhost:3000

### Backend

#### WebSocket server

- accessible on localhost:8765

#### API

- accessible on localhost:8000

### Database

- postgresql database
- can be managed with adminer on localhost:8080
- there is a test database that uses postgres as well, the databases are only accessible from within the default docker network, both on port 5432

## Set up

### Front-end

Create .env in /frontend/ similar to /frontend/example.env.
Example values without any extra configuration:
```
VITE_WS_URL="ws://localhost:8765"
VITE_API_URL="http://localhost:8000"
```

### Back-end

Create .env in /backend/ according to /backend/example.env.

Create a random secret key that will be used to sign the JWT tokens.
To generate a secure random secret key use the command:
```bash
openssl rand -hex 32
```

Example Values without any further configuration:
```
SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DB_URL="postgresql+psycopg://chatuser:chatpass@db:5432/chatapp"
DB_TEST_URL="postgresql+psycopg://myuser:mypassword@db-test:5432/mydatabase_test"
API_URL="http://backend-api:8000"
```

### Database
I will give examples as to how to set up the database with the given compose environment.

**Note:** This might take a while on the first run

First, start all the containers (from the project root):
```bash
docker compose up --build
```

Next, the tables need to be created in the database. For this, connect to the backend-ws docker container, and run the migration(s) from there.
Example command:
```bash
docker compose run --rm --name name backend-ws alembic upgrade head
```

Now that the database has tables, they need to be filled with data. There is a seeder in this project, that generates example data to try out the features with.
Example command:
```bash
docker compose run --rm --name name backend-api python -um db.seeder
```

## Testing
There are integration tests written for the API at backend/python_api/tests.

Example command for running these:
```bash
docker compose run --rm --name name backend-api pytest
```

**Note**: The tests require the test database to be running (the db-test service in the compose).
