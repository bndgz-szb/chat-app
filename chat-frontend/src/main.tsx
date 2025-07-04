import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@/index.css';
import App from '@/App';
import UsernameContextProvider from '@/contexts/ChatContextProvider';
import WebSocketContextProvider from '@/contexts/WebSocketProvider';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <UsernameContextProvider>
      <WebSocketContextProvider>
        <App />
      </WebSocketContextProvider>
    </UsernameContextProvider>
  </StrictMode>
);
