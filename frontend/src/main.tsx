import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@/index.css';
import App from '@/App';
import UsernameContextProvider from '@/contexts/ChatContextProvider';
import WebSocketContextProvider from '@/contexts/WebSocketProvider';
import { ApiProvider } from '@reduxjs/toolkit/query/react';
import { apiSlice } from './app/apiSlice';

createRoot(document.getElementById('root')!).render(
	<StrictMode>
		<UsernameContextProvider>
			<WebSocketContextProvider>
				<ApiProvider api={apiSlice}>
					<App />
				</ApiProvider>
			</WebSocketContextProvider>
		</UsernameContextProvider>
	</StrictMode>
);
