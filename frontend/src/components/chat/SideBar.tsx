import UserChat from '@/components/chat/UserChat';
import type { Chat } from '@/state/responseTypes';

type Props = {
	onChatSelect: (receiver: number) => void;
	selectedChatId: number;
	listOfChats: Chat[];
};

function SideBar({ onChatSelect, selectedChatId, listOfChats }: Props) {
	return (
		<div
			className={`${selectedChatId !== -1 ? 'hidden' : ''} w-screen max-h-screen fixed lg:block lg:static z-10 lg:z-0 lg:w-1/5 bg-gray-800 outline-1 outline-solid outline-gray-900 overflow-y-scroll p-4 text-center lg:text-left`}
		>
			{listOfChats.map((chat) => (
				<UserChat
					key={chat.id}
					chatId={chat.id}
					name={chat.name}
					onClick={onChatSelect}
					selected={chat.id === selectedChatId}
				/>
			))}
		</div>
	);
}

export default SideBar;
