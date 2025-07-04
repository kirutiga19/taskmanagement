import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  const token = localStorage.getItem('token');
  const isAdmin = localStorage.getItem('is_admin') === 'true'; // assumes backend sets this

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={token && !isAdmin ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/admin-dashboard" element={token && isAdmin ? <AdminDashboard /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
