import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@/index.css';
import App from '@/App';
import WebSocketContextProvider from '@/contexts/WebSocketProvider';
import { Provider } from 'react-redux';
import { store } from './state/store';
import { StyledEngineProvider } from '@mui/material/styles';
import GlobalStyles from '@mui/material/GlobalStyles';

createRoot(document.getElementById('root')!).render(
	<StrictMode>
		<StyledEngineProvider enableCssLayer>
			<GlobalStyles styles="@layer theme, base, mui, components, utilities;" />
			<Provider store={store}>
				<WebSocketContextProvider>
					<App />
				</WebSocketContextProvider>
			</Provider>
		</StyledEngineProvider>
	</StrictMode>
);
