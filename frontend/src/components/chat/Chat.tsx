import { useContext, useEffect, useState } from 'react';
import SideBar from '@/components/chat/SideBar';
import ChatScreen from './ChatScreen';
import { useChatQuery } from '@/state/apiSlice';
import { logout } from '@/state/authSlice';
import { useAppDispatch } from '@/state/hooks';
import { useNavigate } from 'react-router-dom';
import { WebSocketContext } from '@/contexts/WebSocketContext';

function Chat() {
	const [selectedChatId, setSelectedChatId] = useState<number>(-1);
	const { isError, isSuccess, data } = useChatQuery();
	const dispatch = useAppDispatch();
	const navigate = useNavigate();
	const { sendHello } = useContext(WebSocketContext);

	useEffect(() => {
		if (isError) {
			dispatch(logout());
			navigate('/login');
		}
	}, [isError, dispatch, logout, navigate]);

	useEffect(() => {
		if (isSuccess && selectedChatId !== -1) {
			sendHello(selectedChatId);
		}
	}, [isSuccess, selectedChatId]);

	return data ? (
		<div className="flex grow w-full justify-between gap-1">
			<SideBar
				setSelectedChatId={setSelectedChatId}
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
