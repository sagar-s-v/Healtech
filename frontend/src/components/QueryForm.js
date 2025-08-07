import React, { useState } from 'react';

// Simplified to just handle UI and pass the query up
function QueryForm({ selectedDocId, onQuerySubmit }) {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onQuerySubmit(query);
    };

    return (
        <div>
            <h2>3. Ask a Question</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="query">Your Question</label>
                    <textarea
                        id="query"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="e.g., Does this policy cover knee surgery, and what are the conditions?"
                    />
                </div>
                <button type="submit" disabled={!selectedDocId}>
                    Submit Query
                </button>
            </form>
        </div>
    );
}

export default QueryForm;