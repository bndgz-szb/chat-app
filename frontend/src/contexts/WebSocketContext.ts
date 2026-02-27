import type { HelloMessage } from '@/resources/ServerMessages';
import { createContext } from 'react';

export interface WebSocketContextInterface {
	connect: (url: string, helloMessage: HelloMessage) => void;
	sendMessage: (messageContent: string, chat_id: number) => void;
	sendHello: (chat_id: number) => void;
}

export const WebSocketContext = createContext<WebSocketContextInterface>({
	connect: function (): void {
		throw new Error('Function not implemented.');
	},
	sendMessage: function (): void {
		throw new Error('Function not implemented.');
	},
	sendHello: function (): void {
		throw new Error('Function not implemented.');
	},
});
