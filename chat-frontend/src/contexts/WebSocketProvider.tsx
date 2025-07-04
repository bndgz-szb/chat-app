import { WebSocketContext } from '@/contexts/WebSocketContext';
import useWebSocket from '@/hooks/useWebSocketHook';
import { type ReactNode } from 'react';

type Props = {
  children: ReactNode;
};

const WebSocketContextProvider = ({ children }: Props) => {
  const service = useWebSocket();

  return <WebSocketContext value={service}>{children}</WebSocketContext>;
};

export default WebSocketContextProvider;
