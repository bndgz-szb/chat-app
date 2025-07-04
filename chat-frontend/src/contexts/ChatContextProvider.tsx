import { ChatContext, type ChatContextInterface } from '@/contexts/ChatContext';
import { useState, type ReactNode } from 'react';

type Props = {
  children: ReactNode;
};

const ChatContextProvider = ({ children }: Props) => {
  const [username, setUsername] = useState<string>('');
  const [messageHistory, setMessageHistory] = useState<string[]>([]);

  const ctx: ChatContextInterface = {
    username,
    setUsername,
    messageHistory,
    setMessageHistory,
  };

  return <ChatContext value={ctx}>{children}</ChatContext>;
};

export default ChatContextProvider;
