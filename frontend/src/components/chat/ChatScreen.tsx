import Message from '@/components/chat/Message';
import { ChatContext } from '@/contexts/ChatContext';
import { WebSocketContext } from '@/contexts/WebSocketContext';
import { selectUser } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { useContext, useState } from 'react';

type Props = {
	selectedChatId: number;
};

function ChatScreen({ selectedChatId }: Props) {
	const [message, setMessage] = useState<string>('');
	const username = useAppSelector(selectUser);
	const { sendMessage } = useContext(WebSocketContext);
	const { messageHistory } = useContext(ChatContext);

	const onType = (e: React.KeyboardEvent<HTMLInputElement>): void => {
		if (e.key === 'Enter') {
			sendMessage(message, selectedChatId);
			setMessage('');
		}
	};

	return (
		<div className="flex flex-col-reverse w-4/5 bg-stone-800 p-8">
			<input
				className="fixed bottom-5 right-12 border rounded-xl px-4 py-2 w-15/20"
				type="text"
				placeholder="Aa"
				value={message}
				onChange={(e) => setMessage(e.target.value)}
				onKeyDown={onType}
			/>
			<div className="flex flex-col gap-4 overflow-y-scroll p-8 mb-13">
				{messageHistory?.map((message) => {
					return (
						<Message
							key={message.id}
							message={message.content}
							mine={username === message.sender_username}
						/>
					);
				})}
			</div>
		</div>
	);
}

export default ChatScreen;
