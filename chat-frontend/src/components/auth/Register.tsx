import ErrorDiv from '@/components/auth/ErrorDiv';
import InputField from '@/components/auth/InputField';
import { ChatContext } from '@/contexts/ChatContext';
import { WebSocketContext } from '@/contexts/WebSocketContext';
import { useContext, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Register() {
	const [inputUsername, setInputUsername] = useState<string>('');
	const [inputPassword, setInputPassword] = useState<string>('');
	const [serverError, setServerError] = useState<string>('');
	const [confirmInputPassword, setConfirmInputPassword] = useState<string>('');
	const { username } = useContext(ChatContext);
	const { sendRegister } = useContext(WebSocketContext);
	const navigate = useNavigate();

	useEffect(() => {
		if (username !== '') navigate('/', { replace: true });
	}, [username, navigate]);

	const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		if (inputPassword === confirmInputPassword) {
			sendRegister(
				inputUsername,
				inputPassword,
				() => navigate('/'),
				(error) => setServerError(error)
			);
		} else {
			setServerError('Passwords have to match!');
		}
	};

	return (
		<div className="grow flex items-center justify-center p-4 flex-col">
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

					<button type="submit" className="w-full py-2">
						Register
					</button>
				</form>
			</div>

			<Link to={'/login'} className="mt-1 text-center">
				Log in
			</Link>
		</div>
	);
}

export default Register;
