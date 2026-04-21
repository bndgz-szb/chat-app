import Message from '@/components/chat/Message';
import { WebSocketContext } from '@/contexts/WebSocketContext';
import { selectUser } from '@/state/authSlice';
import { selectMessageHistory } from '@/state/chatSlice';
import { useAppSelector } from '@/state/hooks';
import { useContext, useState } from 'react';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';

type Props = {
	selectedChatId: number;
	unSelectChat: () => void;
};

function ChatScreen({ selectedChatId, unSelectChat }: Props) {
	const [message, setMessage] = useState<string>('');
	const username = useAppSelector(selectUser);
	const { sendMessage } = useContext(WebSocketContext);
	const messageHistory = useAppSelector(selectMessageHistory);

	const onType = (e: React.KeyboardEvent<HTMLInputElement>): void => {
		if (e.key === 'Enter') {
			sendMessage(message, selectedChatId);
			setMessage('');
		}
	};

	return (
		<div className="flex flex-col-reverse w-screen lg:max-w-4/5 bg-stone-800 p-8 overflow-y-scroll">
			<ArrowBackIosIcon
				fontSize="large"
				className="fixed top-1/5 left-5 lg:hidden"
				onClick={unSelectChat}
			/>
			<input
				className="fixed bottom-5 right-5 lg:right-12 border rounded-xl px-4 py-2 w-9/10 lg:w-15/20"
				type="text"
				placeholder="Aa"
				value={message}
				onChange={(e) => setMessage(e.target.value)}
				onKeyDown={onType}
			/>
			<div className="flex flex-col-reverse gap-4 overflow-y-scroll p-8 mb-13">
				{messageHistory?.toReversed().map((message) => {
					return (
						<Message
							key={message.id}
							message={message}
							mine={username === message.sender_username}
						/>
					);
				})}
			</div>
		</div>
	);
}

export default ChatScreen;
