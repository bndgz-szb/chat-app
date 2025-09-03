# Chat webapp mini project

This is a side project that i developed with the help of the internet + ChatGPT. Everything is containerized with docker compose, frontend and backend files are mounted. A volume is created for the database.

There are no complex networking set up, so only the host pc is available to message itself on different accounts. There are no security measures, everything is sent/stored in plain text. The websocket messages are in JSON format.

---

## Features

- Real-time messaging via WebSocket protocol
- **Private 1:1 messaging** between users
- **Group channels** for public announcements (not fully implemented)
- Password-based login
- User presence updates (join/leave notifications)
- Message structure validation on server side
- **Frontend built with React + Vite + TypeScript**
- Dockerized project for easy deployment
- Frontend-agnostic (can be connected to any WebSocket-compatible client)

---

## Tech Stack

- **Backend**: Python 3.13, `websockets`
- **Containerization**: Docker
- **Protocol**: WebSocket (`ws://`)

---

## WebSocket Message Format

All messages are sent as JSON. Example:

```json
{
  "msg_type": "message",
  "sender": "alice",
  "target": "bob",
  "message": "hi bob"
}
```

Other message types:

- `login`: client login with username+password
- `register`: client register with username+password
- `broadcast`: message sent to all users
- `user_list`: server sends currently online users
- `user_login`, `user_logout`: events when users join/leave
- `error`: structured error from server

## Components

### Frontend

- accessible on localhost:3000

### Backend

- sqlalchemy for ORM
- alembic for migrations
- accessible on localhost:8765

### Database

- postgresql database
- can be managed with adminer on localhost:8080

## Set up

Create .env in frontend for websocket url (e.g. VITE_WS_URL="ws://localhost:8765").
