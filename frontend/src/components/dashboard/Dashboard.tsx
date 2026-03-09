import ButtonRow from '@/components/dashboard/ButtonRow';
import Tasks from '@/components/dashboard/Tasks';
import { useValidateTokenQuery } from '@/state/apiSlice';
import { logout } from '@/state/authSlice';
import { useAppDispatch } from '@/state/hooks';
import { useEffect } from 'react';

function Dashboard() {
	const { isError, isLoading } = useValidateTokenQuery();
	const dispatch = useAppDispatch();

	useEffect(() => {
		if (isError) {
			dispatch(logout());
		}
	}, [isError, dispatch, logout]);

	return (
		<div className="bg-gray-700 grow">
			{!isLoading && !isError && <ButtonRow />}
			<Tasks />
		</div>
	);
}

export default Dashboard;
