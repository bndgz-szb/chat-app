import type { WebSocketContextInterface } from '@/contexts/WebSocketContext';
import type {
	HelloMessage,
	ServerToClientMessage,
	UnicastMessage,
} from '@/resources/ServerMessages';
import { logout, selectToken, selectUserId } from '@/state/authSlice';
import { appendMessage } from '@/state/chatSlice';
import { useAppDispatch, useAppSelector } from '@/state/hooks';
import { useRef } from 'react';
import { setMessageHistory } from '@/state/chatSlice';

function useWebSocket(): WebSocketContextInterface {
	const ws = useRef<WebSocket | null>(null);

	const user_id = useAppSelector(selectUserId);
	const token = useAppSelector(selectToken);
	const dispatch = useAppDispatch();

	const connect = (url: string, helloMessage: HelloMessage) => {
		if (ws.current) {
			return;
		}
		console.log('new WebSocket connection');

		ws.current = new WebSocket(url);

		ws.current.addEventListener('error', (error: Event) =>
			console.error(`Closed WebSocket connection; error: ${error}`)
		);

		ws.current.addEventListener('open', () => {
			ws.current!.send(JSON.stringify(helloMessage));
		});

		ws.current.addEventListener('message', (event: MessageEvent) => {
			const parsed: ServerToClientMessage = JSON.parse(event.data);

			function assertUnreachable(x: never): never {
				throw new Error(`Didn't expect to get here: ${JSON.stringify(x)}`);
			}

			switch (parsed.msg_type) {
				case 'message':
					dispatch(
						appendMessage({
							message: parsed.message,
						})
					);
					break;
				case 'error':
					console.error(`error: ${parsed.error}`);
					if (parsed.error === 'Could not validate credentials') {
						dispatch(logout());
					}
					break;
				case 'history':
					dispatch(setMessageHistory({ messageHistory: parsed.messages }));
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
			sender_id: user_id,
			chat_id,
			content: messageContent,
		};
		ws.current?.send(JSON.stringify(message));
	};

	const sendHello = (chat_id: number) => {
		const message: HelloMessage = {
			msg_type: 'hello',
			token,
			chat_id,
		};
		ws.current?.send(JSON.stringify(message));
	};

	return { connect, sendMessage, sendHello };
}

export default useWebSocket;
