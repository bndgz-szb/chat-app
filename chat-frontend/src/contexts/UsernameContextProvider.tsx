import {
  UsernameContext,
  type UsernameContextInterface,
} from '@/contexts/UsernameContext';
import { useState, type ReactNode } from 'react';

type Props = {
  children: ReactNode;
};

const UsernameContextProvider = ({ children }: Props) => {
  const [username, setUsername] = useState<string>('');
  const ctx: UsernameContextInterface = {
    login: setUsername,
    username,
  };

  return <UsernameContext value={ctx}>{children}</UsernameContext>;
};

export default UsernameContextProvider;
