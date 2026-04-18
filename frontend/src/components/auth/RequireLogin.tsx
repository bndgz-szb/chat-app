import { useValidateTokenQuery } from '@/state/apiSlice';
import { logout } from '@/state/authSlice';
import { useAppDispatch } from '@/state/hooks';
import { useEffect, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

type Props = {
	children: ReactNode;
};

function RequireLogin({ children }: Props) {
	const { data, isError } = useValidateTokenQuery();
	const dispatch = useAppDispatch();
	const navigate = useNavigate();
	const { t } = useTranslation();

	useEffect(() => {
		if (isError) {
			dispatch(logout());
			navigate('/login');
		}
	}, [isError, dispatch, logout, navigate]);

	return data ? children : <div>{t('validating')}</div>;
}

export default RequireLogin;
