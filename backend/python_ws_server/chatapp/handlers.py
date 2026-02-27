import json
import requests
import os
from typing import Type, TypeVar
from dataclasses import fields, is_dataclass
from dotenv import load_dotenv
from websockets.asyncio.server import ServerConnection

from python_ws_server.chatapp.global_variables import CONNECTIONS
from python_ws_server.chatapp.messages import *
from python_api.auth import get_current_user

load_dotenv()
API_URL = os.getenv("API_URL")
if API_URL == None:
    raise Exception("Don't forget to create .env file")
T = TypeVar("T")


def assert_has_keys(data: dict, model: Type[T]) -> None:
    if not is_dataclass(model):
        raise TypeError(f"{model} must be a dataclass")

    required = {f.name for f in fields(model)}
    missing = required - data.keys()
    assert not missing, f"Missing keys: {missing}"


async def handleHelloMessage(data, websocket: ServerConnection) -> bool:
    assert_has_keys(data, HelloMessage)

    parsed = HelloMessage(**data)
    user = await get_current_user(parsed.token)
    if user is None:
        await sendError(websocket, "Could not validate credentials")
        return False

    headers = {"authorization": f"Bearer {parsed.token}"}
    response = requests.get(
        f"{str(API_URL)}/message-history",
        headers=headers, params={"chat_id": parsed.chat_id}
    )
    if response.status_code == 200:
        history = response.json()
    else:
        await sendError(websocket, "Error while querying message history")
        return False

    msg = HistoryMessage(msg_type="history", messages=history)
    CONNECTIONS[websocket] = parsed.chat_id
    await websocket.send(json.dumps(msg.__dict__))
    return True


async def handleUnicastMessage(data, websocket: ServerConnection) -> None:
    try:
        assert_has_keys(data, UnicastMessage)
    except (AssertionError):
        await sendError(websocket, "Invalid message format")

    parsed = UnicastMessage(**data)
    user = await get_current_user(parsed.token)
    if user is None:
        await sendError(websocket, "Could not validate credentials")
        return

    if user.username != parsed.sender:
        await websocket.close(
            code=4002,
            reason="Can't send messages in someone else's name"
        )

    else:
        await sendMessage(websocket, parsed)


async def sendError(websocket: ServerConnection, message: str) -> None:
    msg = ErrorMessage(msg_type="error", error=message)
    await websocket.send(json.dumps(msg.__dict__))


# save message in db, send message to active users
async def sendMessage(
        websocket: ServerConnection, message: UnicastMessage
) -> None:
    # TODO consume api
    # if success, send message to every connection that has chat_id
    for other_websocket in CONNECTIONS.keys():
        if CONNECTIONS[other_websocket] == message.chat_id:
            await other_websocket.send(json.dumps(message.__dict__))
    # if error, notify client
    await sendError(websocket, "Error")
    pass


async def message_loop(websocket: ServerConnection) -> None:
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("msg_type") == "hello":
                    await handleHelloMessage(data, websocket)
                else:
                    await handleUnicastMessage(data, websocket)
            except (json.JSONDecodeError):
                await sendError(websocket, "Invalid message format")
                continue
    except:
        print(f"[CLOSE] {websocket.remote_address} closed connection")
    finally:
        print(
            f"[DISCONNECTED] {websocket.remote_address} removed from active list")
        del CONNECTIONS[websocket]


async def handle_auth(websocket: ServerConnection) -> None:
    raw_json = await websocket.recv()

    try:
        data = json.loads(raw_json)
        if not await handleHelloMessage(data, websocket):
            return
    except json.JSONDecodeError:
        await sendError(websocket, "JSON decode error")
        return
    except AssertionError:
        await sendError(websocket, "Wrong message format")
        return

    print(f"[LOGIN] {websocket.remote_address} connected")
    await message_loop(websocket)
