import type { MessageWithUsername } from '@/state/responseTypes';
import { createContext } from 'react';

export interface ChatContextInterface {
	messageHistory: MessageWithUsername[];
	setMessageHistory: (
		callback: (messages: MessageWithUsername[]) => MessageWithUsername[]
	) => void;
}

export const ChatContext = createContext<ChatContextInterface>({
	messageHistory: [],
	setMessageHistory: function (): void {
		throw new Error('Function not implemented.');
	},
});
