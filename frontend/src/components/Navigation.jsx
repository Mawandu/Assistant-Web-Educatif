import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Navigation() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav style={{ padding: '10px', background: '#eee', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
                <Link to="/" style={{ marginRight: '20px' }}>Assistant</Link>
                {user && (user.role === 'admin' || user.role === 'enseignant') && (
                    <Link to="/admin">Administration</Link>
                )}
            </div>
            <div>
                {user ? (
                    <>
                        <span style={{ marginRight: '15px' }}>Bonjour, {user.email}</span>
                        <button onClick={handleLogout}>Déconnexion</button>
                    </>
                ) : (
                    <Link to="/login">Connexion</Link>
                )}
            </div>
        </nav>
    );
}

export default Navigation;