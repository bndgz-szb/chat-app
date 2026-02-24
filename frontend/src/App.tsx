import Layout from '@/components/layout/Layout';
import Login from '@/components/auth/Login';
import Register from '@/components/auth/Register';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Dashboard from '@/components/dashboard/Dashboard';
import Topics from '@/components/dashboard/Topics';
import TaskForm from '@/components/dashboard/TaskForm';
import Chat from '@/components/chat/Chat';

function App() {
	return (
		<Layout>
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<Chat />} />
					<Route path="/dashboard" element={<Dashboard />} />
					<Route path="/login" element={<Login />} />
					<Route path="/register" element={<Register />} />
					<Route path="/dashboard/topics" element={<Topics />} />
					<Route path="/dashboard/create_task" element={<TaskForm />} />
				</Routes>
			</BrowserRouter>
		</Layout>
	);
}

export default App;
