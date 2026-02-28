import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '@/state/store';

const authFromStorage = localStorage.getItem('auth');
let parsedAuth: AuthState = {
	username: '',
	user_id: -1,
	token: '',
	is_admin: false,
};

try {
	parsedAuth = authFromStorage
		? JSON.parse(authFromStorage)
		: { username: '', user_id: -1, token: '' };
} catch {
	parsedAuth = { username: '', user_id: -1, token: '', is_admin: false };
}

interface AuthState {
	user_id: number;
	username: string;
	token: string;
	is_admin: boolean;
}

const initialState: AuthState = {
	user_id: parsedAuth?.user_id || -1,
	username: parsedAuth?.username || '',
	token: parsedAuth?.token || '',
	is_admin: parsedAuth?.is_admin || false,
};

const authSlice = createSlice({
	name: 'auth',
	initialState,
	reducers: {
		login: (state, action: PayloadAction<AuthState>) => {
			state.user_id = action.payload.user_id;
			state.username = action.payload.username;
			state.token = action.payload.token;
			state.is_admin = action.payload.is_admin;
			localStorage.setItem('auth', JSON.stringify(state));
		},
		logout: (state) => {
			state.user_id = -1;
			state.token = '';
			state.username = '';
			state.is_admin = false;
			localStorage.removeItem('auth');
		},
	},
});

export const authReducer = authSlice.reducer;

export const { login, logout } = authSlice.actions;

export const selectUser = (state: RootState) => state.auth.username;
export const selectUserId = (state: RootState) => state.auth.user_id;
export const selectToken = (state: RootState) => state.auth.token;
export const selectIsAdmin = (state: RootState) => state.auth.is_admin;
