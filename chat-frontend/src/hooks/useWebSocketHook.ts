import { UsernameContext } from '@/contexts/UsernameContext';
import { useContext, useRef, useState } from 'react';

function useWebSocket() {
  const ws = useRef<WebSocket | null>(null);
  const currentSocketId = useRef<number>(0);

  const [messages, setMessages] = useState<string[]>([]);
  const { setUsername } = useContext(UsernameContext);

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
      // TODO
      setMessages((prev) => [...prev, event.data]);
    });
  };

  const sendMessage = (msg: string) => {
    ws.current?.send(msg);
    setMessages((prev) => [...prev, msg]);
  };

  const sendLogin = (username: string) => {
    ws.current?.close();
    connect(import.meta.env.VITE_WS_URL, username);
  };

  return { messages, sendMessage, sendLogin };
}

export default useWebSocket;
