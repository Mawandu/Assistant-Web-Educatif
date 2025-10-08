// frontend/src/Admin.jsx
import React, { useState } from 'react';
import { useAuth } from './context/AuthContext';

function Admin() {
    const [file, setFile] = useState(null);
    const [subject, setSubject] = useState('');
    const [level, setLevel] = useState('');
    const [message, setMessage] = useState('');
    const { token } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('Téléversement en cours...');

        // ✅ Simplifié : le token du contexte devrait suffire
        if (!token) {
            setMessage("Erreur : Vous devez être connecté pour effectuer cette action.");
            return;
        }

        const formData = new FormData();
        formData.append('subject', subject);
        formData.append('level', level);
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/api/v1/documents', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,  // ✅ Utiliser directement token du contexte
                },
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Une erreur est survenue.");
            }

            setMessage(`Succès ! Document "${data.document_details.file_name}" ajouté.`);
            
            // ✅ BONUS : Réinitialiser le formulaire après succès
            setFile(null);
            setSubject('');
            setLevel('');
            
        } catch (error) {
            setMessage(`Erreur : ${error.message}`);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Panneau d'Administration</h2>
            <p>Téléversez un nouveau manuel PDF.</p>
            
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Sujet: </label>
                    <input 
                        type="text" 
                        value={subject} 
                        onChange={(e) => setSubject(e.target.value)} 
                        required 
                    />
                </div>
                
                <div style={{ margin: '10px 0' }}>
                    <label>Niveau: </label>
                    <input 
                        type="text" 
                        value={level} 
                        onChange={(e) => setLevel(e.target.value)} 
                        required 
                    />
                </div>
                
                <div>
                    <label>Fichier PDF: </label>
                    <input 
                        type="file" 
                        onChange={(e) => setFile(e.target.files[0])} 
                        accept="application/pdf" 
                        required 
                    />
                </div>
                
                <button type="submit" style={{ marginTop: '20px' }}>
                    Téléverser
                </button>
            </form>
            
            {message && <p style={{ marginTop: '20px', fontWeight: 'bold' }}>{message}</p>}
        </div>
    );
}

export default Admin;