
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import App from './App';

const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('jwt');
    return token ? children : <Navigate to="/" />;
};

const Main = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route
                    path="/app"
                    element={
                        <PrivateRoute>
                            <App />
                        </PrivateRoute>
                    }
                />
            </Routes>
        </Router>
    );
};

ReactDOM.render(<Main />, document.getElementById('root'));
