import type { WebSocketContextInterface } from '@/contexts/WebSocketContext';
import type {
	HelloMessage,
	ServerToClientMessage,
	UnicastMessage,
} from '@/resources/ServerMessages';
import { selectToken, selectUser, selectUserId } from '@/state/authSlice';
import { selectMessageHistory } from '@/state/chatSlice';
import { useAppDispatch, useAppSelector } from '@/state/hooks';
import { useRef } from 'react';
import { setMessageHistory } from '@/state/chatSlice';

function useWebSocket(): WebSocketContextInterface {
	const ws = useRef<WebSocket | null>(null);

	const username = useAppSelector(selectUser);
	const user_id = useAppSelector(selectUserId);
	const messageHistory = useAppSelector(selectMessageHistory);
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
					// dispatch(
					// 	setMessageHistory({
					// 		messageHistory: [...messageHistory, parsed.content],
					// 	})
					// );
					break;
				case 'error':
					console.error(`error: ${parsed.error}`);
					// TODO logout if credentials are invalid
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
			sender: username,
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
