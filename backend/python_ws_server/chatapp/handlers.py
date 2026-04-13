import json
import requests
import os
from sqlalchemy.orm import Session
from typing import Type, TypeVar, Dict
from dataclasses import fields, is_dataclass
from dotenv import load_dotenv
from websockets.asyncio.server import ServerConnection

from db.session import SessionLocal
from python_ws_server.chatapp.global_variables import CONNECTIONS
from python_ws_server.chatapp.messages import *
from python_api.auth import get_current_user

load_dotenv()
API_URL = str(os.getenv("API_URL"))
if API_URL == "":
    raise Exception("Don't forget to create .env file")
T = TypeVar("T")


def assert_has_keys(data: dict, model: Type[T]) -> None:
    if not is_dataclass(model):
        raise TypeError(f"{model} must be a dataclass")

    required = {f.name for f in fields(model)}
    missing = required - data.keys()
    assert not missing, f"Missing keys: {missing}"


def prepareAuthHeader(token: str) -> Dict[str, str]:
    return {"authorization": f"Bearer {token}"}


async def handleHelloMessage(data, ws: ServerConnection) -> bool:
    assert_has_keys(data, HelloMessage)

    parsed = HelloMessage(**data)
    with SessionLocal() as session:
        user = await get_current_user(parsed.token, session)
    if user is None:
        await sendError(ws, "Could not validate credentials")
        return False

    headers = prepareAuthHeader(parsed.token)
    response = requests.get(
        f"{API_URL}/message-history",
        headers=headers, params={"chat_id": parsed.chat_id}
    )
    if response.status_code == 200:
        history = response.json()
    else:
        error = response.json()
        if "detail" in error:
            await sendError(ws, error["detail"])
        else:
            await sendError(ws, "Error while querying message history")
        return False

    msg = HistoryMessage(msg_type="history", messages=history)
    CONNECTIONS[ws] = parsed.chat_id
    await ws.send(json.dumps(msg.__dict__))
    return True


async def handleUnicastMessage(data, ws: ServerConnection) -> None:
    assert_has_keys(data, UnicastMessage)

    parsed = UnicastMessage(**data)
    with SessionLocal() as session:
        user = await get_current_user(parsed.token, session)
    if user is None:
        await sendError(ws, "Could not validate credentials")
        return

    if user.id != parsed.sender_id:
        await ws.close(
            code=4002,
            reason="Can't send messages in someone else's name"
        )
    else:
        await sendMessage(ws, parsed)


async def sendError(ws: ServerConnection, message: str) -> None:
    msg = ErrorMessage(msg_type="error", error=message)
    await ws.send(json.dumps(msg.__dict__))


# save message in db, send message to active users
async def sendMessage(
        ws: ServerConnection, message: UnicastMessage
) -> None:
    headers = prepareAuthHeader(message.token)
    response = requests.post(
        f"{API_URL}/message",
        headers=headers,
        json={**message.__dict__}
    )
    response_message = response.json()
    if response.status_code == 200:
        for other_websocket in CONNECTIONS.keys():
            if CONNECTIONS[other_websocket] == message.chat_id:
                await other_websocket.send(json.dumps(
                    {"msg_type": "message", "message": response_message}
                ))
                pass
    else:
        error = response.json()
        if "detail" in error:
            await sendError(ws, error["detail"])
        else:
            await sendError(ws, "Error while sending message")


async def message_loop(ws: ServerConnection) -> None:
    try:
        async for message in ws:
            try:
                data = json.loads(message)
                if data.get("msg_type") == "hello":
                    await handleHelloMessage(data, ws)
                else:
                    await handleUnicastMessage(data, ws)
            except (json.JSONDecodeError):
                await sendError(ws, "JSON decode error")
                continue
            except (AssertionError):
                await sendError(ws, "Invalid message format")
                continue
    except:
        print(f"[CLOSE] {ws.remote_address} closed connection")
    finally:
        print(f"[DISCONNECTED] {ws.remote_address} removed from active list")
        del CONNECTIONS[ws]


async def handle_auth(ws: ServerConnection) -> None:
    raw_json = await ws.recv()

    try:
        data = json.loads(raw_json)
        if not await handleHelloMessage(data, ws):
            return
    except json.JSONDecodeError:
        await sendError(ws, "JSON decode error")
        return
    except AssertionError:
        await sendError(ws, "Wrong message format")
        return

    print(f"[LOGIN] {ws.remote_address} connected")
    await message_loop(ws)
