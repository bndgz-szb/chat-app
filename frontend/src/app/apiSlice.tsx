import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const API_BASE_URL = 'http://localhost:8000'; // TODO read from env

type Token = {
	token_type: String;
	access_token: String;
};

type OAuth2PasswordRequestForm = {
	grant_type?: String;
	username: String;
	password: String;
	scope?: String;
	client_id?: String;
	client_secret?: String;
};

const convertObjectToFormDataString = (obj: Object): String =>
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
	}),
});

export const { useLoginMutation } = apiSlice;
