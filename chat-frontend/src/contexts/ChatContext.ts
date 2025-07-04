import { createContext } from 'react';

export interface ChatContextInterface {
  username: string;
  setUsername: (newName: string) => void;
  messageHistory: string[];
  setMessageHistory: (callback: (messages: string[]) => string[]) => void;
  onlineUsers: string[];
  setOnlineUsers: (callback: (users: string[]) => string[]) => void;
}

export const ChatContext = createContext<ChatContextInterface>({
  username: '',
  setUsername: function (): void {
    throw new Error('Function not implemented.');
  },
  messageHistory: [],
  setMessageHistory: function (): void {
    throw new Error('Function not implemented.');
  },
  onlineUsers: [],
  setOnlineUsers: function (): void {
    throw new Error('Function not implemented.');
  },
});
