import Layout from '@/components/layout/Layout';
import Login from '@/components/auth/Login';
import Register from '@/components/auth/Register';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Dashboard from '@/components/dashboard/Dashboard';
import Topics from '@/components/dashboard/Topics';
import TaskForm from '@/components/dashboard/TaskForm';
import Chat from '@/components/chat/Chat';
import Logout from '@/components/auth/Logout';

function App() {
	return (
		<BrowserRouter>
			<Layout>
				<Routes>
					<Route path="/chat" element={<Chat />} />
					<Route path="/dashboard" element={<Dashboard />} />
					<Route path="/login" element={<Login />} />
					<Route path="/logout" element={<Logout />} />
					<Route path="/register" element={<Register />} />
					<Route path="/dashboard/topics" element={<Topics />} />
					<Route path="/dashboard/create_task" element={<TaskForm />} />
				</Routes>
			</Layout>
		</BrowserRouter>
	);
}

export default App;
