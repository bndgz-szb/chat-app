import { useContext, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import SideBar from '@/components/chat/SideBar';
import ChatScreen from '@/components/chat/ChatScreen';
import { useChatQuery } from '@/state/apiSlice';
import { selectToken } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { WebSocketContext } from '@/contexts/WebSocketContext';
import LoadingDiv from '@/components/utils/LoadingDiv';

interface LocationState {
	chat_id: number;
}

function Chat() {
	const [selectedChatId, setSelectedChatId] = useState<number>(-1);
	const { isSuccess, data } = useChatQuery();
	const { sendHello, connect } = useContext(WebSocketContext);
	const token = useAppSelector(selectToken);
	const locationState = useLocation().state as LocationState;

	useEffect(() => {
		if (locationState) {
			handleChatSelect(locationState.chat_id);
		}
	}, []);

	useEffect(() => {
		if (isSuccess) {
			connect(import.meta.env.VITE_WS_URL, {
				msg_type: 'hello',
				token,
				chat_id: selectedChatId,
			});
		}
	}, [isSuccess, connect]);

	function handleChatSelect(chat_id: number): void {
		setSelectedChatId(chat_id);
		sendHello(chat_id);
	}

	return data ? (
		<div className="flex grow w-full h-5/6 max-h-5/6 justify-between gap-1">
			<SideBar
				onChatSelect={handleChatSelect}
				selectedChatId={selectedChatId}
				listOfChats={data}
			/>
			<ChatScreen selectedChatId={selectedChatId} />
		</div>
	) : (
		<LoadingDiv />
	);
}

export default Chat;
