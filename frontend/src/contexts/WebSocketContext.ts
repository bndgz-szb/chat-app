import { createContext } from 'react';

export interface WebSocketContextInterface {
	sendMessage: (messageContent: string, chat_id: number) => void;
	sendHello: (chat_id: number) => void;
}

export const WebSocketContext = createContext<WebSocketContextInterface>({
	sendMessage: function (): void {
		throw new Error('Function not implemented.');
	},
	sendHello: function (): void {
		throw new Error('Function not implemented.');
	},
});
