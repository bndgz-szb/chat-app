import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const API_BASE_URL = 'http://localhost:8000'; // TODO read from env

type Token = {
	token_type: string;
	access_token: string;
};

type OAuth2PasswordRequestForm = {
	grant_type?: string;
	username: string;
	password: string;
	scope?: string;
	client_id?: string;
	client_secret?: string;
};

type RegisterRequest = {
	username: string;
	email: string;
	password: string;
};

const convertObjectToFormDataString = (obj: Object): string =>
	Object.entries(obj)
		.reduce((prev, curr) => {
			return `${prev}&${curr[0]}=${curr[1]}`;
		}, '')
		.slice(1);

export const apiSlice = createApi({
	baseQuery: fetchBaseQuery({ baseUrl: API_BASE_URL }),
	endpoints: (build) => ({
		login: build.mutation<Token, OAuth2PasswordRequestForm>({
			query: (formData) => ({
				url: 'login',
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
				body: convertObjectToFormDataString(formData),
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
