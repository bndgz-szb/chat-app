import ErrorDiv from '@/components/utils/ErrorDiv';
import InputField from '@/components/auth/InputField';
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useLoginMutation } from '@/state/apiSlice';
import { useAppDispatch, useAppSelector } from '@/state/hooks';
import { login, selectUser } from '@/state/authSlice';
import { Button } from '@mui/material';

function Login() {
	const [inputUsername, setInputUsername] = useState<string>('');
	const [inputPassword, setInputPassword] = useState<string>('');
	const [serverError, setServerError] = useState<string>('');
	const username = useAppSelector(selectUser);
	const [sendLogin] = useLoginMutation();
	const navigate = useNavigate();
	const dispatch = useAppDispatch();

	useEffect(() => {
		if (username !== '') navigate('/dashboard', { replace: true }); // TODO validate token against api
	}, [username, navigate]);

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (inputUsername === '') {
			setServerError('Username field is required!');
			return;
		}
		if (inputPassword === '') {
			setServerError('Password field is required!');
			return;
		}

		sendLogin({
			username: inputUsername,
			password: inputPassword,
		})
			.unwrap()
			.then((result) =>
				dispatch(
					login({
						user_id: result.user_id,
						token: result.access_token,
						username: result.username,
						is_admin: result.is_admin,
					})
				)
			)
			.catch((error) => setServerError(error.data?.detail));
	};

	return (
		<div className="grow flex items-center justify-center p-4 flex-col w-full">
			<div className="bg-gray-800/60 rounded-lg border border-white/20 p-10 w-full max-w-md text-white">
				<h2 className="text-2xl font-bold text-center mb-6">Login</h2>

				{serverError && <ErrorDiv error={serverError} />}

				<form onSubmit={handleSubmit} className="space-y-4">
					<InputField
						type={'text'}
						name={'username'}
						label={'Username'}
						placeholder={'boti123'}
						value={inputUsername}
						onChange={setInputUsername}
					/>
					<InputField
						type={'password'}
						name={'password'}
						label={'Password'}
						placeholder={'********'}
						value={inputPassword}
						onChange={setInputPassword}
					/>

					<Button
						variant="contained"
						type="submit"
						className="w-full py-2 rounded-lg border-1 border-solid border-[transparent] px-5 py-3 font-medium [font-family:inherit] bg-zinc-900 cursor-pointer [transition:border-color_0.25s] hover:border-sky-300 outline-[4px_auto_-webkit-focus-ring-color]"
					>
						Log in
					</Button>
				</form>
			</div>

			<Link to={'/register'} className="mt-1 text-center">
				Sign up
			</Link>
		</div>
	);
}

export default Login;
