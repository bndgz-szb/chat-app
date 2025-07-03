import { createContext } from 'react';

export interface UsernameContextInterface {
  login: (newName: string) => void;
  username: string;
}

export const UsernameContext = createContext<UsernameContextInterface>({
  login: function (): void {
    throw new Error('Function not implemented.');
  },
  username: '',
});
