export type RegisterRequest = {
	username: string;
	email: string;
	password: string;
};

export type LoginRequest = {
	username: string;
	password: string;
};

export type TaskParticipantRequest = {
	task_id: number;
};
