import { selectUser } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { type ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

type Props = {
	children: ReactNode;
};

function RequireLogin({ children }: Props) {
	const username = useAppSelector(selectUser);
	return username === '' ? <Navigate to="/login" replace /> : children;
}

export default RequireLogin;
