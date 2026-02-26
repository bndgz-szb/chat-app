import type { MessageWithUsername } from '@/state/responseTypes';
import { ChatContext, type ChatContextInterface } from '@/contexts/ChatContext';
import { useState, type ReactNode } from 'react';

type Props = {
	children: ReactNode;
};

const ChatContextProvider = ({ children }: Props) => {
	const [messageHistory, setMessageHistory] = useState<MessageWithUsername[]>(
		[]
	);

	const ctx: ChatContextInterface = {
		messageHistory,
		setMessageHistory,
	};

	return <ChatContext value={ctx}>{children}</ChatContext>;
};

export default ChatContextProvider;
