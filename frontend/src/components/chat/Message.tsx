import type { MessageWithUsername } from '@/state/responseTypes';

type Props = {
	message: MessageWithUsername;
	mine: boolean;
};

function Message({ message, mine }: Props) {
	return mine ? (
		<div className="ml-auto w-auto bg-blue-400 rounded-lg justify-self-end py-2 px-3 wrap-normal">
			<p className="text-gray-950">You</p>
			{message.content}
			<p className="text-right text-gray-600">
				{message.sent_at.split('.')[0].replace('T', ' ')}
			</p>
		</div>
	) : (
		<div className="mr-auto w-auto bg-stone-400 rounded-lg justify-self-end py-2 px-3 wrap-normal">
			<p className="text-gray-950">{message.sender_username}</p>
			{message.content}
			<p className="text-right text-gray-600">
				{message.sent_at.split('.')[0].replace('T', ' ')}
			</p>
		</div>
	);
}

export default Message;
