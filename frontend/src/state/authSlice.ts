import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from './store';

const authFromStorage = localStorage.getItem('auth');
let parsedAuth: AuthState = { username: '', token: '' };

try {
	parsedAuth = authFromStorage
		? JSON.parse(authFromStorage)
		: { username: '', token: '' };
} catch {
	parsedAuth = { username: '', token: '' };
}

interface AuthState {
	username: string;
	token: string;
}

const initialState: AuthState = {
	username: parsedAuth?.username || '',
	token: parsedAuth?.token || '',
};

const authSlice = createSlice({
	name: 'auth',
	initialState,
	reducers: {
		login: (state, action: PayloadAction<AuthState>) => {
			state.username = action.payload.username;
			state.token = action.payload.token;
			localStorage.setItem('auth', JSON.stringify(state));
		},
		logout: (state) => {
			state.token = '';
			state.username = '';
			localStorage.removeItem('auth');
		},
	},
});

export const authReducer = authSlice.reducer;

export const { login, logout } = authSlice.actions;

export const selectUser = (state: RootState) => state.auth.username;
