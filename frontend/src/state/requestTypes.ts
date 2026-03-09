export type RegisterRequest = {
	username: string;
	email: string;
	password: string;
};

export type LoginRequest = {
	username: string;
	password: string;
};

export type TaskParticipant = {
	id: number;
	name: string;
	role: 'admin' | 'user' | 'guest';
};
