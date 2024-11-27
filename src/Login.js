
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css'; 
import './Login.css'; 

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:5000/login', {
                username,
                password,
            });

            const token = response.data.access_token;

            if (token) {
                localStorage.setItem('jwt', token);
                navigate('/app');
            } else {
                setError('Login failed: No token received.');
            }
        } catch (err) {
            if (err.response && err.response.data) {
                setError(err.response.data.error || 'Invalid credentials. Please try again.');
            } else {
                setError('An error occurred while logging in. Please try again later.');
            }
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h3 className="login-title">Welcome Back!</h3>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username" className="login-label">Username</label>
                        <input
                            type="text"
                            className="form-control login-input"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password" className="login-label">Password</label>
                        <input
                            type="password"
                            className="form-control login-input"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                        />
                    </div>
                    {error && <div className="alert alert-danger" role="alert">{error}</div>}
                    <button type="submit" className="btn login-button">Login</button>
                </form>
            </div>
        </div>
    );
};

export default Login;
