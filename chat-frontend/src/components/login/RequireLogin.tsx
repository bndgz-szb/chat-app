import { UsernameContext } from '@/context/UsernameContext';
import { useContext, type ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

type Props = {
  children: ReactNode;
};

function RequireLogin({ children }: Props) {
  const { username } = useContext(UsernameContext);
  return username === '' ? <Navigate to="/login" /> : children;
}

export default RequireLogin;
