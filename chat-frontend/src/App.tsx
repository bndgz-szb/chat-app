import Layout from '@/components/layout/Layout';
import Login from '@/components/auth/Login';
import RequireLogin from '@/components/auth/RequireLogin';
import Register from '@/components/auth/Register';
import ChatScreen from '@/components/chat-screen/ChatScreen';
import SideBar from '@/components/sidebar/SideBar';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { useState } from 'react';
import Dashboard from '@/components/dashboard/Dashboard';
import Topics from '@/components/dashboard/Topics';
import TaskForm from '@/components/dashboard/TaskForm';

function App() {
	const [receiver, setReceiver] = useState<string>('');
	return (
		<Layout>
			<BrowserRouter>
				<Routes>
					<Route
						path="/"
						element={
							<RequireLogin>
								<div className="flex grow w-full justify-between gap-1">
									<SideBar selectChat={setReceiver} selectedChat={receiver} />
									<ChatScreen receiver={receiver} />
								</div>
							</RequireLogin>
						}
					/>
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
