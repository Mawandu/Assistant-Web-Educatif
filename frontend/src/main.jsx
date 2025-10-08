import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import App from './App.jsx';
import Admin from './Admin.jsx';
import LoginPage from './pages/LoginPage.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';
import Navigation from './components/Navigation.jsx';
import { AuthProvider } from './context/AuthContext.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
          <Navigation />
          <Routes>
            <Route path="/" element={<App />} />
            <Route path="/login" element={<LoginPage />} />
            <Route 
                path="/admin" 
                element={
                    <ProtectedRoute roles={['admin', 'enseignant']}>
                        <Admin />
                    </ProtectedRoute>
                } 
            />
          </Routes>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
);