import type { MessageWithUsername } from '@/state/responseTypes';

interface BaseMessage {
	msg_type: string;
	token: string;
	chat_id: number;
}

export interface Message {
	id: number;
	chat_id: number;
	sender_id: number;
	content: string;
	sent_at: string;
}

export interface HelloMessage extends BaseMessage {
	msg_type: 'hello';
}

export interface UnicastMessage extends BaseMessage {
	msg_type: 'message';
	sender_id: number;
	content: string;
}

export interface ErrorMessage {
	msg_type: 'error';
	error: string;
}

export interface HistoryMessage {
	msg_type: 'history';
	messages: MessageWithUsername[];
}

export interface UnicastMessageWithUsername {
	msg_type: 'message';
	message: MessageWithUsername;
}

export type ServerToClientMessage =
	| UnicastMessageWithUsername
	| ErrorMessage
	| HistoryMessage;
