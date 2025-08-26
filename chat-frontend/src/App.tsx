import Layout from '@/components/layout/Layout';
import Login from '@/components/auth/Login';
import RequireLogin from '@/components/auth/RequireLogin';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Register from '@/components/auth/Register';

function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route
					path="/"
					element={
						<RequireLogin>
							<Layout />
						</RequireLogin>
					}
				/>
				<Route path="/login" element={<Login />} />
				<Route path="/register" element={<Register />} />
			</Routes>
		</BrowserRouter>
	);
}

export default App;
