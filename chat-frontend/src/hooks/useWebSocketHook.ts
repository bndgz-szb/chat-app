import { ChatContext } from '@/contexts/ChatContext';
import { useContext, useRef } from 'react';

function useWebSocket() {
  const ws = useRef<WebSocket | null>(null);
  const currentSocketId = useRef<number>(0);

  const { setUsername, messageHistory, setMessageHistory } =
    useContext(ChatContext);

  const connect = (url: string, username: string) => {
    const socketId = ++currentSocketId.current;
    ws.current = new WebSocket(url);

    ws.current.addEventListener('close', () => {
      if (socketId === currentSocketId.current) setUsername('');
    });

    ws.current.addEventListener('error', (error: Event) =>
      console.error(`socketId: ${socketId}; error: ${error}`)
    );

    ws.current.addEventListener('open', () => {
      if (socketId !== currentSocketId.current) return;
      ws.current!.send(JSON.stringify({ type: 'login', username }));
      setUsername(username);
    });

    ws.current.addEventListener('message', (event: MessageEvent) => {
      const data = JSON.parse(event.data);
      if (data.type === 'message') setMessageHistory((prev) => [...prev, data]);
    });
  };

  const sendMessage = (msg: string) => {
    // TODO
    ws.current?.send(msg);
    setMessageHistory((prev) => [...prev, msg]);
  };

  const sendLogin = (username: string) => {
    ws.current?.close();
    connect(import.meta.env.VITE_WS_URL, username);
  };

  return { messageHistory, sendMessage, sendLogin };
}

export default useWebSocket;
