import ErrorDiv from '@/components/auth/ErrorDiv';
import InputField from '@/components/auth/InputField';
import { useRegisterMutation } from '@/state/apiSlice';
import { selectUser } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { Button } from '@mui/material';
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Register() {
	const [inputUsername, setInputUsername] = useState<string>('');
	const [inputEmail, setInputEmail] = useState<string>('');
	const [inputPassword, setInputPassword] = useState<string>('');
	const [serverError, setServerError] = useState<string>('');
	const [confirmInputPassword, setConfirmInputPassword] = useState<string>('');
	const username = useAppSelector(selectUser);
	const [sendRegister] = useRegisterMutation();
	const navigate = useNavigate();

	useEffect(() => {
		if (username !== '') navigate('/dashboard', { replace: true });
	}, [username, navigate]);

	const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (inputPassword !== confirmInputPassword) {
			setServerError('Passwords have to match!');
			return;
		}
		if (inputUsername === '') {
			setServerError('Username field is required!');
			return;
		}
		if (inputEmail === '') {
			setServerError('Email field is required!');
			return;
		}
		if (inputPassword === '') {
			setServerError('Password field is required!');
			return;
		}

		sendRegister({
			username: inputUsername,
			email: inputEmail,
			password: inputPassword,
		})
			.unwrap()
			.then(() => navigate('/login'))
			.catch((error) => setServerError(error.data.detail));
	};

	return (
		<div className="grow flex items-center justify-center p-4 flex-col w-full">
			<div className="bg-gray-800/60 rounded-lg border border-white/20 p-10 w-full max-w-md text-white">
				<h2 className="text-2xl font-bold text-center mb-6">Register</h2>

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
						type={'text'}
						name={'email'}
						label={'Email'}
						placeholder={'boti123@boti.boti'}
						value={inputEmail}
						onChange={setInputEmail}
					/>
					<InputField
						type="password"
						name={'password'}
						label={'Password'}
						placeholder={'********'}
						value={inputPassword}
						onChange={setInputPassword}
					/>
					<InputField
						type="password"
						name={'confirm_password'}
						label={'Confirm Password'}
						placeholder={'********'}
						value={confirmInputPassword}
						onChange={setConfirmInputPassword}
					/>

					<Button
						variant="contained"
						type="submit"
						className="w-full py-2 rounded-lg border-1 border-solid border-[transparent] px-5 py-3 font-medium [font-family:inherit] bg-zinc-900 cursor-pointer [transition:border-color_0.25s] hover:border-sky-300 outline-[4px_auto_-webkit-focus-ring-color]"
					>
						Register
					</Button>
				</form>
			</div>

			<Link to={'/login'} className="mt-1 text-center">
				Login
			</Link>
		</div>
	);
}

export default Register;
