import { useValidateTokenQuery } from '@/state/apiSlice';
import { logout, selectIsAdmin } from '@/state/authSlice';
import { useAppDispatch, useAppSelector } from '@/state/hooks';
import { useEffect, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';

type Props = {
	children: ReactNode;
};

function RequireAdmin({ children }: Props) {
	const { data, isError } = useValidateTokenQuery();
	const dispatch = useAppDispatch();
	const navigate = useNavigate();
	const isAdmin = useAppSelector(selectIsAdmin);

	useEffect(() => {
		if (isError) {
			dispatch(logout());
			navigate('/login');
		} else if (!isAdmin) {
			navigate('/dashboard');
		}
	}, [isError, dispatch, logout, navigate, isAdmin]);

	return data ? children : <div>Validating token...</div>;
}

export default RequireAdmin;
