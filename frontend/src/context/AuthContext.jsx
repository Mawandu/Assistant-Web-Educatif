import React, { createContext, useState, useContext, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    // ✅ Changé : utiliser 'authToken' au lieu de 'token'
    const [token, setToken] = useState(localStorage.getItem('authToken'));
    const [user, setUser] = useState(null);

    useEffect(() => {
        if (token) {
            try {
                const decoded = jwtDecode(token);
                
                // Check expiration (exp is in seconds, Date.now() is in ms)
                if (decoded.exp * 1000 < Date.now()) {
                    console.log("Token expired, forcing logout.");
                    setToken(null);
                    return;
                }
                
                setUser({ email: decoded.sub, role: decoded.role });
                
                // ✅ Changé : utiliser 'authToken' au lieu de 'token'
                localStorage.setItem('authToken', token);
            } catch (error) {
                console.error("Invalid token, forcing logout:", error);
                setToken(null);
            }
        } else {
            // ✅ Changé : utiliser 'authToken' au lieu de 'token'
            localStorage.removeItem('authToken');
            setUser(null);
        }
    }, [token]);

    const login = async (email, password) => {
        const response = await fetch('http://localhost:8000/api/v1/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username: email, password: password })
        });

        if (!response.ok) {
            throw new Error("Échec de la connexion");
        }

        const data = await response.json();
        setToken(data.access_token);
    };

    const logout = () => {
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};