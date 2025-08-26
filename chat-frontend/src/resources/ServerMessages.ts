interface BaseMessage {
	msg_type: string;
	message: string;
}

interface UserPresenceMessage {
	msg_type: string;
	username: string;
}

export interface UnicastMessage extends BaseMessage {
	msg_type: 'message';
	sender: string;
	target: string;
}

export interface BroadcastMessage extends BaseMessage {
	msg_type: 'broadcast';
	sender: string;
}

export interface ErrorMessage extends BaseMessage {
	msg_type: 'error';
}

export interface UserListMessage {
	msg_type: 'user_list';
	users: string[];
}

export interface UserLoginMessage extends UserPresenceMessage {
	msg_type: 'user_login';
}

export interface UserLogoutMessage extends UserPresenceMessage {
	msg_type: 'user_logout';
}

export interface LoginMessage extends UserPresenceMessage {
	msg_type: 'login';
	password: string;
}

export interface RegisterMessage extends UserPresenceMessage {
	msg_type: 'regiser';
	password: string;
}

export type ServerToClientMessage =
	| UnicastMessage
	| BroadcastMessage
	| ErrorMessage
	| UserListMessage
	| UserLoginMessage
	| UserLogoutMessage;

export type ChatMessage = UnicastMessage | BroadcastMessage;
