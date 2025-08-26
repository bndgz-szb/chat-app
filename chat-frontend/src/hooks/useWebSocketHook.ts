import { ChatContext } from '@/contexts/ChatContext';
import type { WebSocketContextInterface } from '@/contexts/WebSocketContext';
import type {
	LoginMessage,
	ServerToClientMessage,
	UnicastMessage,
} from '@/resources/ServerMessages';
import { useContext, useRef } from 'react';

function useWebSocket(): WebSocketContextInterface {
	const ws = useRef<WebSocket | null>(null);
	const currentSocketId = useRef<number>(0);

	const {
		username,
		setUsername,
		messageHistory,
		setMessageHistory,
		setOnlineUsers,
	} = useContext(ChatContext);

	const connect = (
		url: string,
		username: string,
		password: string,
		onSuccess: () => void
	) => {
		const socketId = ++currentSocketId.current;
		ws.current = new WebSocket(url);

		ws.current.addEventListener('close', () => {
			if (socketId === currentSocketId.current) setUsername('');
		});

		ws.current.addEventListener('error', (error: Event) =>
			console.error(`closed socketId: ${socketId}; error: ${error}`)
		);

		ws.current.addEventListener('open', () => {
			if (socketId !== currentSocketId.current) return;

			// TODO hash password
			const login_msg: LoginMessage = { msg_type: 'login', username, password };
			ws.current!.send(JSON.stringify(login_msg));
			setUsername(username);
			onSuccess();
		});

		ws.current.addEventListener('message', (event: MessageEvent) => {
			const parsed: ServerToClientMessage = JSON.parse(event.data);

			function assertUnreachable(x: never): never {
				throw new Error(`Didn't expect to get here: ${JSON.stringify(x)}`);
			}

			switch (parsed.msg_type) {
				case 'message':
				case 'broadcast':
					setMessageHistory((prev) => [...prev, event.data]);
					break;
				case 'user_list':
					setOnlineUsers(() => parsed.users);
					break;
				case 'user_login':
					setOnlineUsers((prev) => [...prev, parsed.username]);
					break;
				case 'user_logout':
					setOnlineUsers((prev) => prev.filter((u) => u !== parsed.username));
					break;
				case 'error':
					console.error(`error: ${parsed.message}`);
					break;
				default:
					return assertUnreachable(parsed);
			}
		});
	};

	const sendMessage = (messageContent: string, target: string) => {
		const message: UnicastMessage = {
			msg_type: 'message',
			sender: username,
			target,
			message: messageContent,
		};
		const jsonMessage = JSON.stringify(message);
		ws.current?.send(jsonMessage);
		setMessageHistory((prev) => [...prev, jsonMessage]);
	};

	const sendLogin = (
		username: string,
		password: string,
		onSuccess: () => void
	) => {
		ws.current?.close();
		connect(import.meta.env.VITE_WS_URL, username, password, onSuccess);
	};

	return { messageHistory, sendMessage, sendLogin };
}

export default useWebSocket;
