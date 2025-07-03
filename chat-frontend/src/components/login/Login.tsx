import InputField from '@/components/login/InputField';
import { useState } from 'react';

function Login() {
  const [username, setUsername] = useState<string>('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // TODO try login
    // const { login } = useContext(UsernameContext);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 flex-col">
      <div className="bg-gray-800/60 rounded-lg border border-white/20 p-10 w-full max-w-md text-white">
        <h2 className="text-2xl font-bold text-center mb-6">Login</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <InputField
            name={'username'}
            label={'Username'}
            placeholder={'boti123'}
            value={username}
            onChange={setUsername}
          />

          <button type="submit" className="w-full py-2">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
