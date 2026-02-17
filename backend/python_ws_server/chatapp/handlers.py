import json
import websockets

from typing import Type, TypeVar
from dataclasses import fields, is_dataclass
from python_ws_server.chatapp.global_variables import CONNECTIONS
from python_ws_server.chatapp.messages import *
from python_ws_server.chatapp.services.auth import broadcastConnectionsState, login, register

T = TypeVar("T")


def assert_has_keys(data: dict, model: Type[T]) -> None:
    if not is_dataclass(model):
        raise TypeError(f"{model} must be a dataclass")

    required = {f.name for f in fields(model)}
    missing = required - data.keys()
    assert not missing, f"Missing keys: {missing}"


async def sendError(websocket, message):
    msg = ErrorMessage(msg_type="error", message=message)
    await websocket.send(json.dumps(msg.__dict__))


def broadcastMessage(sender, message):
    msg = BroadcastMessage(msg_type="broadcast",
                           sender=sender, message=message)
    websockets.broadcast(filter(lambda websocket: websocket !=
                         CONNECTIONS[sender], CONNECTIONS.values()), json.dumps(msg.__dict__))


async def message_loop(websocket, username):
    try:
        async for message in websocket:
            # check message format
            try:
                data = json.loads(message)
                assert all(key in data for key in (
                    "msg_type", "sender", "target", "message"))
            except (json.JSONDecodeError, AssertionError):
                await sendError(websocket, "Invalid message format")
                continue

            parsed = UnicastMessage(**data)

            if parsed.target == "":
                broadcastMessage(parsed.sender, parsed.message)
                continue

            if websocket != CONNECTIONS[parsed.sender]:  # check sender address
                await websocket.close(code=4002, reason="Can't send messages in someone else's name")

            elif parsed.target not in CONNECTIONS.keys():  # check if receiver is online
                await sendError(websocket, "User currently offline")

            else:  # send message to receiver, save to history
                try:
                    await sendMessage(parsed.sender, parsed.target, parsed.message)
                except:
                    await sendError(websocket, "User disconnected before receiving the message")
    except:
        print(f"[CLOSE] {username} closed connection")
    finally:
        print(f"[DISCONNECTED] {username} removed from active list")
        del CONNECTIONS[username]
        broadcastConnectionsState("user_logout", username)


async def handle_auth(websocket):
    raw_json = await websocket.recv()

    try:
        data = json.loads(raw_json)
        if data.get("msg_type") == "login":
            assert_has_keys(data, LoginAttempt)
        elif data.get("msg_type") == "register":
            assert_has_keys(data, RegisterAttempt)
        else:
            raise AssertionError()
    except json.JSONDecodeError:
        await sendError(websocket, "JSON decode error")
        return
    except AssertionError:
        await sendError(websocket, "Wrong message format")
        return

    if data.get("msg_type") == "login":
        response = await login(LoginAttempt(**data))
    elif data.get("msg_type") == "register":
        response = await register(RegisterAttempt(**data))

    if response["status"] == "error":
        await sendError(websocket, response["error"])
        return

    msg = UserListMessage(msg_type="user_list", users=response["chats"])
    await websocket.send(json.dumps(msg.__dict__))
    await message_loop(websocket, response["username"])
