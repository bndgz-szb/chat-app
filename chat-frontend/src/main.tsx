import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@/index.css';
import App from '@/App';
import UsernameContextProvider from '@/contexts/ChatContextProvider';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <UsernameContextProvider>
      <App />
    </UsernameContextProvider>
  </StrictMode>
);
