import UserChat from '@/components/chat/UserChat';
import type { Chat } from '@/state/responseTypes';

type Props = {
	setSelectedChatId: (receiver: number) => void;
	selectedChatId: number;
	listOfChats: Chat[];
};

function SideBar({ setSelectedChatId, selectedChatId, listOfChats }: Props) {
	return (
		<div className="w-1/5 bg-gray-800 outline-1 outline-solid outline-gray-900 overflow-y-scroll p-4">
			{listOfChats.map((chat) => (
				<UserChat
					key={chat.id}
					chatId={chat.id}
					name={chat.name}
					onClick={setSelectedChatId}
					selected={chat.id === selectedChatId}
				/>
			))}
		</div>
	);
}

export default SideBar;
