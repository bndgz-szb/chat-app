import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import type { RootState } from '@/state/store';
import type { LoginRequest, RegisterRequest } from '@/state/requestTypes';
import type { Chat, Token } from '@/state/responseTypes';

const API_BASE_URL = 'http://localhost:8000'; // TODO read from env

export const apiSlice = createApi({
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
		chat: build.query<Chat[], void>({
			query: () => ({
				url: 'chat',
				method: 'GET',
			}),
		}),
		login: build.mutation<Token, LoginRequest>({
			query: (body) => ({
				url: 'login',
				method: 'POST',
				body,
			}),
		}),
		register: build.mutation<String, RegisterRequest>({
			query: (body) => ({
				url: 'register',
				method: 'POST',
				body,
			}),
		}),
	}),
});

export const { useChatQuery, useLoginMutation, useRegisterMutation } = apiSlice;
