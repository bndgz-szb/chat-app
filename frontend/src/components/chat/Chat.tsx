import { useContext, useEffect, useState } from 'react';
import SideBar from '@/components/chat/SideBar';
import ChatScreen from '@/components/chat/ChatScreen';
import { useChatQuery } from '@/state/apiSlice';
import { logout, selectToken } from '@/state/authSlice';
import { useAppDispatch, useAppSelector } from '@/state/hooks';
import { useNavigate } from 'react-router-dom';
import { WebSocketContext } from '@/contexts/WebSocketContext';

function Chat() {
	const [selectedChatId, setSelectedChatId] = useState<number>(-1);
	const { isError, isSuccess, data } = useChatQuery();
	const dispatch = useAppDispatch();
	const navigate = useNavigate();
	const { sendHello, connect } = useContext(WebSocketContext);
	const token = useAppSelector(selectToken);

	useEffect(() => {
		if (isError) {
			dispatch(logout());
			navigate('/login');
		}
	}, [isError, dispatch, logout, navigate]);

	useEffect(() => {
		if (isSuccess) {
			connect(import.meta.env.VITE_WS_URL, {
				msg_type: 'hello',
				token,
				chat_id: -1,
			});
		}
	}, [isSuccess]);

	function handleChatSelect(chat_id: number): void {
		setSelectedChatId(chat_id);
		sendHello(chat_id);
	}

	return data ? (
		<div className="flex grow w-full justify-between gap-1">
			<SideBar
				onChatSelect={handleChatSelect}
				selectedChatId={selectedChatId}
				listOfChats={data}
			/>
			<ChatScreen selectedChatId={selectedChatId} />
		</div>
	) : (
		<div>Loading...</div>
	);
}

export default Chat;
