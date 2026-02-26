import type { Message } from '@/resources/ServerMessages';

export type Chat = {
	id: number;
	name: string;
};

export type LoginResponse = {
	access_token: string;
	user_id: number;
	username: string;
};

export interface MessageWithUsername extends Message {
	sender_username: string;
}
