import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css';

function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    axios.get('http://127.0.0.1:8000/api/my-tasks/', {
      headers: { Authorization: `Token ${token}` },
    })
      .then(response => {
        setTasks(response.data.tasks);
        setUsername(response.data.username);
      })
      .catch(() => {
        alert('Session expired or failed to load tasks. Please login again.');
        localStorage.removeItem('token');
        window.location.href = '/login';
      });
  }, []);

  const handleStatusChange = (taskId, newStatus) => {
    const token = localStorage.getItem('token');
    axios.patch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, { status: newStatus }, {
      headers: { Authorization: `Token ${token}` },
    })
    .then(() => {
      setTasks(prev =>
        prev.map(task => (task.id === taskId ? { ...task, status: newStatus } : task))
      );
    });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {username}</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>
      <div className="task-list">
        {tasks.length === 0 ? (
          <p>No tasks assigned.</p>
        ) : (
          tasks.map(task => (
            <div className="task-card" key={task.id}>
              <h3>{task.title}</h3>
              <p>{task.description}</p>
              <label>Status:</label>
              <select value={task.status} onChange={(e) => handleStatusChange(task.id, e.target.value)}>
                <option value="not_started">Not Started</option>
                <option value="start">Start</option>
                <option value="on_process">On Process</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Dashboard;
