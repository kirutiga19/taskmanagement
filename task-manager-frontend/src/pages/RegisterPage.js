// src/pages/RegisterPage.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './LoginRegister.css'; // Using same style as login

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/api/register/', {
        username,
        email,
        password
      });
      alert('Registration successful. Please login.');
      navigate('/login');
    } catch (err) {
      alert('Registration failed');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Register</h2>
        <form onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Register</button>
        </form>
        <p>
          Already have an account?{' '}
          <Link to="/login" className="register-link">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
