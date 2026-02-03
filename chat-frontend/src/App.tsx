import Layout from '@/components/layout/Layout';
import Login from '@/components/auth/Login';
import RequireLogin from '@/components/auth/RequireLogin';
import Register from '@/components/auth/Register';
import ChatScreen from '@/components/chat-screen/ChatScreen';
import SideBar from '@/components/sidebar/SideBar';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { useState } from 'react';

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
					<Route path="/login" element={<Login />} />
					<Route path="/register" element={<Register />} />
				</Routes>
			</BrowserRouter>
		</Layout>
	);
}

export default App;
