import { logout } from '@/state/authSlice';
import { useAppDispatch } from '@/state/hooks';
import { useEffect } from 'react';
import { Navigate } from 'react-router-dom';

function Logout() {
	const dispatch = useAppDispatch();
	useEffect(() => {
		dispatch(logout());
	}, []);
	return <Navigate to={'/login'} />;
}

export default Logout;
