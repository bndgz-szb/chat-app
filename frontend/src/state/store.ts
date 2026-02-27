import { configureStore } from '@reduxjs/toolkit';
import { chatReducer } from '@/state/chatSlice';
import { authReducer } from '@/state/authSlice';
import { apiSlice } from '@/state/apiSlice';

export const store = configureStore({
	reducer: {
		chat: chatReducer,
		auth: authReducer,
		[apiSlice.reducerPath]: apiSlice.reducer,
	},
	middleware: (getDefaultMiddleware) =>
		getDefaultMiddleware().concat(apiSlice.middleware),
});

export type AppStore = typeof store;
export type RootState = ReturnType<AppStore['getState']>;
export type AppDispatch = AppStore['dispatch'];
