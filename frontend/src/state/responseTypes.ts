import type { Message } from '@/resources/ServerMessages';

export type Topic = {
	id: number;
	name: string;
};

export type Participant = {
	id: number;
	name: string;
};

export const ChatRole = {
	owner: 'owner',
	member: 'member',
	guest: 'guest',
} as const;

export type ChatRole = keyof typeof ChatRole;

export type TaskParticipant = {
	id: number;
	name: string;
	role: ChatRole;
};

export type TaskWithTopic = {
	id: number;
	name: string;
	created_by: number | null;
	done: boolean;
	topics: Topic[];
	chat_id: number | null;
};

export type Chat = {
	id: number;
	name: string;
};

export type LoginResponse = {
	access_token: string;
	user_id: number;
	username: string;
	is_admin: boolean;
};

export type TaskWithAnalytics = {
	name: string;
	messagesByDays: MessagesByDay[];
	messagesPerUsers: MessagesPerUser[];
};

type MessagesByDay = {
	day: string;
	messages: number;
};

type MessagesPerUser = {
	username: string;
	total_messages: number;
};

export interface MessageWithUsername extends Message {
	sender_username: string;
}
