import { createContext } from 'react';

export interface UsernameContextInterface {
  setUsername: (newName: string) => void;
  username: string;
}

export const UsernameContext = createContext<UsernameContextInterface>({
  setUsername: function (): void {
    throw new Error('Function not implemented.');
  },
  username: '',
});
