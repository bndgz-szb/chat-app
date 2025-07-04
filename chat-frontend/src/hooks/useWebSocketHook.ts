import { ChatContext } from '@/contexts/ChatContext';
import type { WebSocketContextInterface } from '@/contexts/WebSocketContext';
import { useContext, useRef } from 'react';

function useWebSocket(): WebSocketContextInterface {
  const ws = useRef<WebSocket | null>(null);
  const currentSocketId = useRef<number>(0);

  const {
    username,
    setUsername,
    messageHistory,
    setMessageHistory,
    setOnlineUsers,
  } = useContext(ChatContext);

  const connect = (url: string, username: string, onSuccess: () => void) => {
    const socketId = ++currentSocketId.current;
    ws.current = new WebSocket(url);

    ws.current.addEventListener('close', () => {
      if (socketId === currentSocketId.current) setUsername('');
    });

    ws.current.addEventListener('error', (error: Event) =>
      console.error(`closed socketId: ${socketId}; error: ${error}`)
    );

    ws.current.addEventListener('open', () => {
      if (socketId !== currentSocketId.current) return;
      ws.current!.send(JSON.stringify({ type: 'login', username }));
      setUsername(username);
      onSuccess();
    });

    ws.current.addEventListener('message', (event: MessageEvent) => {
      const data = JSON.parse(event.data);
      if (data.type === 'message' || data.type === 'broadcast')
        setMessageHistory((prev) => [...prev, event.data]);
      else if (data.type === 'user_list') setOnlineUsers(() => data.users);
      else if (data.type === 'user_login')
        setOnlineUsers((prev) => [...prev, data.username]);
      else if (data.type === 'user_logout')
        setOnlineUsers((prev) => prev.filter((u) => u !== data.username));
      else if (data.type === 'error') console.error(`error: ${data.message}`);
    });
  };

  const sendMessage = (messageContent: string, to: string) => {
    const message = JSON.stringify({
      type: 'message',
      from: username,
      to,
      message: messageContent,
    });
    ws.current?.send(message);
    setMessageHistory((prev) => [...prev, message]);
  };

  const sendLogin = (username: string, onSuccess: () => void) => {
    ws.current?.close();
    connect(import.meta.env.VITE_WS_URL, username, onSuccess);
  };

  return { messageHistory, sendMessage, sendLogin };
}

export default useWebSocket;
