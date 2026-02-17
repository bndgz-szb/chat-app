import ErrorDiv from '@/components/auth/ErrorDiv';
import InputField from '@/components/auth/InputField';
import { ChatContext } from '@/contexts/ChatContext';
import { useContext, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useLoginMutation } from '@/app/apiSlice';
import { type FetchBaseQueryError } from '@reduxjs/toolkit/query';
import type { SerializedError } from '@reduxjs/toolkit';

function Login() {
	const [inputUsername, setInputUsername] = useState<string>('');
	const [inputPassword, setInputPassword] = useState<string>('');
	const { username } = useContext(ChatContext);
	const [login, { error }] = useLoginMutation();
	const navigate = useNavigate();

	useEffect(() => {
		if (username !== '') navigate('/', { replace: true });
	}, [username, navigate]);

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		const result = await login({
			username: inputUsername,
			password: inputPassword,
		}).unwrap();

		console.log(result); // TODO save in store
	};

	return (
		<div className="grow flex items-center justify-center p-4 flex-col">
			<div className="bg-gray-800/60 rounded-lg border border-white/20 p-10 w-full max-w-md text-white">
				<h2 className="text-2xl font-bold text-center mb-6">Login</h2>

				{error && (
					<ErrorDiv
						error={
							(error as FetchBaseQueryError).status !== undefined
								? JSON.stringify((error as FetchBaseQueryError).data)
								: (error as SerializedError).message
						}
					/>
				)}

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

					<button type="submit" className="w-full py-2">
						Login
					</button>
				</form>
			</div>

			<Link to={'/register'} className="mt-1 text-center">
				Sign up
			</Link>
		</div>
	);
}

export default Login;
