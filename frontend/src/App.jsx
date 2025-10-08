// frontend/src/App.jsx
import React, { useState } from 'react';
import './App.css';
import { useAuth } from './context/AuthContext';

function App() {
  const [messages, setMessages] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { token } = useAuth();

  const handleFeedback = async (message, rating) => {
    if (!token) {
      alert("Vous devez être connecté pour noter une réponse.");
      return;
    }
    try {
      await fetch('http://localhost:8000/api/v1/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          question: messages[messages.indexOf(message) - 1].text, // Trouve la question précédente
          answer: message.text,
          rating: rating
        })
      });
      alert("Merci pour votre retour !");
    } catch (error) {
      console.error("Erreur lors de l'envoi du feedback:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || isLoading) return;

    const newUserMessage = { sender: 'user', text: prompt };
    setMessages(prev => [...prev, newUserMessage]);

    const currentPrompt = prompt;
    setPrompt('');
    setIsLoading(true);

    // --- NOUVEAU : Appel à l'API Backend ---
    try {
      const response = await fetch('http://localhost:8000/api/v1/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: currentPrompt }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();

      const apiResponse = { 
        sender: 'bot', 
        text: data.answer,
        sources: data.sources // On sauvegarde les sources
      };
      setMessages(prev => [...prev, apiResponse]);

    } catch (error) {
      console.error("Erreur lors de l'appel à l'API:", error);
      const errorResponse = {
        sender: 'bot',
        text: "Désolé, une erreur est survenue. Veuillez réessayer."
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
    // --- FIN DU NOUVEAU BLOC ---
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Assistant Web Educatif</h1>
      </header>

      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
            {/* Affiche les sources si elles existent */}
            {msg.sender === 'bot' && msg.sources && (
              <div className="sources">
                <strong>Sources:</strong>
                <ul>
                  {msg.sources.map((source, i) => (
                    <li key={i}>
                      Document ID: {source.document_id}, Page: {source.page}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {/* boutons de feedback pour les messages du bot */}
            {msg.sender === 'bot' && !msg.sources && (
              <div className="feedback-buttons">
                <button onClick={() => handleFeedback(msg, 1)}>👍</button>
                <button onClick={() => handleFeedback(msg, -1)}>👎</button>
              </div>
            )}
          </div>
        ))}
        {isLoading && <div className="loading-indicator">Réflexion en cours...</div>}
      </div>

      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Posez votre question ..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>Envoyer</button>
      </form>
    </div>
  );
}

export default App;