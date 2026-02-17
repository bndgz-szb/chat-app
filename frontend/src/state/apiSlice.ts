import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const API_BASE_URL = 'http://localhost:8000'; // TODO read from env

type Token = {
	token_type: string;
	access_token: string;
};

type RegisterRequest = {
	username: string;
	email: string;
	password: string;
};

type LoginRequest = {
	username: string;
	password: string;
};

export const apiSlice = createApi({
	baseQuery: fetchBaseQuery({ baseUrl: API_BASE_URL }),
	endpoints: (build) => ({
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

export const { useLoginMutation, useRegisterMutation } = apiSlice;
