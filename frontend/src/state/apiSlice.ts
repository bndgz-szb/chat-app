import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import type { RootState } from '@/state/store';
import {
	type CreateTaskRequest,
	type DeleteTaskRequest,
	type LoginRequest,
	type RegisterRequest,
	type TaskParticipantRequest,
} from '@/state/requestTypes';
import type {
	Chat,
	LoginResponse,
	Participant,
	TaskParticipant,
	TaskWithTopic,
	Topic,
} from '@/state/responseTypes';

const API_BASE_URL = import.meta.env.VITE_API_URL;

export const apiSlice = createApi({
	tagTypes: ['Dashboard', 'Auth', 'Chat', 'Topics'],
	baseQuery: fetchBaseQuery({
		baseUrl: API_BASE_URL,
		prepareHeaders(headers, { getState }) {
			const token = (getState() as RootState).auth.token;
			if (token) {
				headers.set('Authorization', `Bearer ${token}`);
			}
			return headers;
		},
	}),
	endpoints: (build) => ({
		dashboard: build.query<TaskWithTopic[], void>({
			query: () => ({
				url: 'dashboard',
				method: 'GET',
			}),
			providesTags: ['Dashboard', 'Auth'],
		}),
		allUsers: build.query<Participant[], void>({
			query: () => ({
				url: 'users',
				method: 'GET',
			}),
		}),
		chat: build.query<Chat[], void>({
			query: () => ({
				url: 'chat',
				method: 'GET',
			}),
			providesTags: ['Chat', 'Auth'],
		}),
		topics: build.query<Topic[], void>({
			query: () => ({
				url: 'topics',
				method: 'GET',
			}),
			providesTags: ['Topics', 'Auth'],
		}),
		validateToken: build.query<void, void>({
			query: () => ({
				url: 'token',
				method: 'GET',
			}),
			providesTags: ['Auth'],
		}),
		taskParticipants: build.query<TaskParticipant[], TaskParticipantRequest>({
			query: (body) => ({
				url: 'task-participants',
				method: 'GET',
				params: body,
			}),
		}),
		login: build.mutation<LoginResponse, LoginRequest>({
			query: (body) => ({
				url: 'login',
				method: 'POST',
				body,
			}),
			invalidatesTags: ['Auth'],
		}),
		register: build.mutation<String, RegisterRequest>({
			query: (body) => ({
				url: 'register',
				method: 'POST',
				body,
			}),
		}),
		createTask: build.mutation<string, CreateTaskRequest>({
			query: (body) => ({
				url: 'create-task',
				method: 'POST',
				body,
			}),
			invalidatesTags: ['Dashboard'],
		}),
		deleteTask: build.mutation<string, DeleteTaskRequest>({
			query: (body) => ({
				url: 'delete-task',
				method: 'DELETE',
				body,
			}),
			invalidatesTags: ['Dashboard', 'Chat'],
		}),
	}),
});

export const {
	useDashboardQuery,
	useAllUsersQuery,
	useChatQuery,
	useTopicsQuery,
	useValidateTokenQuery,
	useLazyTaskParticipantsQuery,
	useLoginMutation,
	useRegisterMutation,
	useCreateTaskMutation,
	useDeleteTaskMutation,
} = apiSlice;
