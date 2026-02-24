type Props = {
	chatId: number;
	name: string;
	onClick: (receiver: number) => void;
	selected: boolean;
};

function UserChat({ chatId, name, onClick, selected }: Props) {
	return (
		<div
			onClick={() => onClick(chatId)}
			className={`${
				selected
					? 'rounded-md bg-teal-800'
					: 'hover:rounded-md hover:bg-gray-700'
			} p-8 font-bold`}
		>
			{name === '' ? 'Broadcast' : name}
		</div>
	);
}

export default UserChat;
