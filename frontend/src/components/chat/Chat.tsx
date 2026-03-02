import { useContext, useEffect, useState } from 'react';
import SideBar from '@/components/chat/SideBar';
import ChatScreen from '@/components/chat/ChatScreen';
import { useChatQuery } from '@/state/apiSlice';
import { selectToken } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { WebSocketContext } from '@/contexts/WebSocketContext';

function Chat() {
	const [selectedChatId, setSelectedChatId] = useState<number>(-1);
	const { isSuccess, data } = useChatQuery();
	const { sendHello, connect } = useContext(WebSocketContext);
	const token = useAppSelector(selectToken);

	useEffect(() => {
		if (isSuccess) {
			connect(import.meta.env.VITE_WS_URL, {
				msg_type: 'hello',
				token,
				chat_id: -1,
			});
		}
	}, [isSuccess, connect]);

	function handleChatSelect(chat_id: number): void {
		setSelectedChatId(chat_id);
		sendHello(chat_id);
	}

	return data ? (
		<div className="flex grow w-full h-5/6 justify-between gap-1">
			<SideBar
				onChatSelect={handleChatSelect}
				selectedChatId={selectedChatId}
				listOfChats={data}
			/>
			<ChatScreen selectedChatId={selectedChatId} />
		</div>
	) : (
		<div>Loading chats...</div>
	);
}

export default Chat;
