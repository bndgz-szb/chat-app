import Layout from '@/components/layout/Layout';
import Login from '@/components/auth/Login';
import Register from '@/components/auth/Register';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Dashboard from '@/components/dashboard/Dashboard';
import Topics from '@/components/dashboard/Topics';
import Chat from '@/components/chat/Chat';
import Logout from '@/components/auth/Logout';
import RequireLogin from '@/components/auth/RequireLogin';

function App() {
	return (
		<BrowserRouter>
			<Layout>
				<Routes>
					<Route path="/dashboard" element={<Dashboard />} />
					<Route path="/login" element={<Login />} />
					<Route path="/logout" element={<Logout />} />
					<Route path="/register" element={<Register />} />
					<Route
						path="/chat"
						element={
							<RequireLogin>
								<Chat />
							</RequireLogin>
						}
					/>
					<Route
						path="/dashboard/topics"
						element={
							<RequireLogin>
								<Topics />
							</RequireLogin>
						}
					/>
				</Routes>
			</Layout>
		</BrowserRouter>
	);
}

export default App;
