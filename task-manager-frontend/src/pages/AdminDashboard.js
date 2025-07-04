import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css'; // use same styling

function AdminDashboard() {
  const [admin, setAdmin] = useState('');
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    axios.get('http://127.0.0.1:8000/api/admin-dashboard/', {
      headers: { Authorization: `Token ${token}` }
    })
    .then(res => {
      setAdmin(res.data.admin);
      setTasks(res.data.tasks);
      setUsers(res.data.users);
    })
    .catch(() => {
      alert('Unauthorized or session expired.');
      localStorage.removeItem('token');
      window.location.href = '/login';
    });
  }, []);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Admin Dashboard - {admin}</h1>
        <button className="logout-btn" onClick={() => {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }}>
          Logout
        </button>
      </div>

      <h2>All Tasks</h2>
      <div className="task-list">
        {tasks.map(task => (
          <div className="task-card" key={task.id}>
            <h3>{task.title}</h3>
            <p><b>Assigned to:</b> {task.assignee}</p>
            <p><b>Status:</b> {task.status}</p>
            <p><b>Priority:</b> {task.priority}</p>
          </div>
        ))}
      </div>

      <h2 style={{ marginTop: "40px" }}>All Users</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.username} ({user.email})</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDashboard;
