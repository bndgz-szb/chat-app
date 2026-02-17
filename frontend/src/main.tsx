import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@/index.css';
import App from '@/App';
import UsernameContextProvider from '@/contexts/ChatContextProvider';
import WebSocketContextProvider from '@/contexts/WebSocketProvider';
import { Provider } from 'react-redux';
import { store } from './state/store';

createRoot(document.getElementById('root')!).render(
	<StrictMode>
		<UsernameContextProvider>
			<WebSocketContextProvider>
				<Provider store={store}>
					<App />
				</Provider>
			</WebSocketContextProvider>
		</UsernameContextProvider>
	</StrictMode>
);
