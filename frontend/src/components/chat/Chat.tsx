import { useEffect, useState } from 'react';
import SideBar from '@/components/chat/SideBar';
import ChatScreen from './ChatScreen';
import { useChatQuery } from '@/state/apiSlice';
import { logout } from '@/state/authSlice';
import { useAppDispatch } from '@/state/hooks';
import { useNavigate } from 'react-router-dom';

function Chat() {
	const [selectedChatId, setSelectedChatId] = useState<number>(-1);
	const { isError, data } = useChatQuery();
	const dispatch = useAppDispatch();
	const navigate = useNavigate();

	useEffect(() => {
		if (isError) {
			dispatch(logout());
			navigate('/login');
		}
	}, [isError, dispatch, logout, navigate]);

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
