import { ChatContext } from '@/contexts/ChatContext';
import type { WebSocketContextInterface } from '@/contexts/WebSocketContext';
import type {
	HelloMessage,
	ServerToClientMessage,
	UnicastMessage,
} from '@/resources/ServerMessages';
import { selectToken, selectUser, selectUserId } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { useContext, useRef } from 'react';

function useWebSocket(): WebSocketContextInterface {
	const ws = useRef<WebSocket | null>(null);
	const currentSocketId = useRef<number>(0);

	const username = useAppSelector(selectUser);
	const user_id = useAppSelector(selectUserId);
	const { messageHistory, setMessageHistory } = useContext(ChatContext);
	const token = useAppSelector(selectToken);

	const connect = (
		url: string,
		helloMessage: HelloMessage,
		onError: (error: string) => void
	) => {
		ws.current?.close();
		const socketId = ++currentSocketId.current;
		ws.current = new WebSocket(url);

		ws.current.addEventListener('error', (error: Event) =>
			console.error(`closed socketId: ${socketId}; error: ${error}`)
		);

		ws.current.addEventListener('open', () => {
			if (socketId !== currentSocketId.current) return;

			ws.current!.send(JSON.stringify(helloMessage));
		});

		ws.current.addEventListener('message', (event: MessageEvent) => {
			const parsed: ServerToClientMessage = JSON.parse(event.data);

			function assertUnreachable(x: never): never {
				throw new Error(`Didn't expect to get here: ${JSON.stringify(x)}`);
			}

			switch (parsed.msg_type) {
				case 'message':
					// setMessageHistory((prev) => [...prev, parsed.content]);
					break;
				case 'error':
					console.error(`error: ${parsed.error}`);
					onError(parsed.error);
					break;
				case 'history':
					setMessageHistory(() => parsed.messages);
					break;
				default:
					return assertUnreachable(parsed);
			}
		});
	};

	const sendMessage = (messageContent: string, chat_id: number) => {
		const message: UnicastMessage = {
			token,
			msg_type: 'message',
			sender: username,
			chat_id,
			content: messageContent,
		};
		const jsonMessage = JSON.stringify(message);
		ws.current?.send(jsonMessage);
	};

	const sendHello = (chat_id: number) => {
		const message: HelloMessage = {
			msg_type: 'hello',
			token,
			chat_id,
		};
		connect(import.meta.env.VITE_WS_URL, message, (error) =>
			console.log(error)
		);
	};

	return { sendMessage, sendHello };
}

export default useWebSocket;
