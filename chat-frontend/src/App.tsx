import Layout from '@/components/layout/Layout';
import Login from '@/components/login/Login';
import RequireLogin from '@/components/login/RequireLogin';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

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
      </Routes>
    </BrowserRouter>
  );
}

export default App;
