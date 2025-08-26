import { createContext } from 'react';

export interface WebSocketContextInterface {
	messageHistory: string[];
	sendMessage: (messageContent: string, to: string) => void;
	sendLogin: (
		username: string,
		password: string,
		onSuccess: () => void
	) => void;
}

export const WebSocketContext = createContext<WebSocketContextInterface>({
	messageHistory: [],
	sendMessage: function (): void {
		throw new Error('Function not implemented.');
	},
	sendLogin: function (): void {
		throw new Error('Function not implemented.');
	},
});
