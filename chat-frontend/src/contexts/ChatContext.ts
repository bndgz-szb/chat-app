import { createContext } from 'react';

export interface ChatContextInterface {
  username: string;
  setUsername: (newName: string) => void;
  messageHistory: string[];
  setMessageHistory: (callback: (messages: string[]) => string[]) => void;
}

export const ChatContext = createContext<ChatContextInterface>({
  username: '',
  setUsername: function (): void {
    throw new Error('Function not implemented.');
  },
  messageHistory: [],
  setMessageHistory: function (): string[] {
    throw new Error('Function not implemented.');
  },
});
