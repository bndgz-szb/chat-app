import type { Message } from '@/resources/ServerMessages';

export type Topic = {
	id: number;
	name: string;
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

export interface MessageWithUsername extends Message {
	sender_username: string;
}
