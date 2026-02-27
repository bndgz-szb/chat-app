import type { MessageWithUsername } from '@/state/responseTypes';
import type { RootState } from '@/state/store';
import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

interface ChatState {
	messageHistory: MessageWithUsername[];
}

interface MessageHistoryPayload {
	messageHistory: MessageWithUsername[];
}

const initialState: ChatState = {
	messageHistory: [],
};

const chatSlice = createSlice({
	name: 'chat',
	initialState,
	reducers: {
		setMessageHistory: (
			state,
			{ payload: { messageHistory } }: PayloadAction<MessageHistoryPayload>
		) => {
			state.messageHistory = messageHistory;
		},
	},
});

export const chatReducer = chatSlice.reducer;

export const { setMessageHistory } = chatSlice.actions;

export const selectMessageHistory = (state: RootState) =>
	state.chat.messageHistory;
