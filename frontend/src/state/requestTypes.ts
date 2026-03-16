import type { TaskParticipant, Topic } from '@/state/responseTypes';

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

export type CreateTaskRequest = {
	name: string;
	done: boolean;
	topics: Topic[];
	participants: TaskParticipant[];
};

export type DeleteTaskRequest = {
	task_id: number;
};
