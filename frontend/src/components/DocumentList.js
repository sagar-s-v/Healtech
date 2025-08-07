import React from 'react';

function DocumentList({ documents, selectedDocId, onSelectDoc }) {
    return (
        <div className="document-list">
            <h2>2. Select Document to Query</h2>
            {documents.length === 0 ? (
                <p>No documents uploaded yet. Please upload a document to begin.</p>
            ) : (
                <ul>
                    {documents.map((doc) => (
                        <li
                            key={doc.id}
                            className={doc.id === selectedDocId ? 'selected' : ''}
                            onClick={() => onSelectDoc(doc.id)}
                        >
                            <span>{doc.file_name} ({doc.document_type})</span>
                            <span className={`status ${doc.status}`}>{doc.status}</span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default DocumentList;