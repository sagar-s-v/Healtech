import React from 'react';

// Now accepts onCancel prop
function ResultsDisplay({ results, isLoading, error, onCancel }) {
    if (isLoading) {
        return (
            <div className="message loading">
                Searching for answers...
                <button onClick={onCancel} style={{ marginLeft: '20px', backgroundColor: '#e74c3c' }}>
                    Cancel Query
                </button>
            </div>
        );
    }

    if (error) {
        return <div className="message error">Error: {error}</div>;
    }

    if (!results) {
        return null;
    }

    return (
        <div className="results-display">
            <h2>4. Answer</h2>
            
            <h3>Direct Answer</h3>
            <div className="answer">{results.answer}</div>

            {results.conditions && results.conditions.length > 0 && (
                <>
                    <h3>Conditions & Limitations</h3>
                    <ul>
                        {results.conditions.map((condition, index) => (
                            <li key={index}>{condition}</li>
                        ))}
                    </ul>
                </>
            )}

            <h3>Decision Rationale</h3>
            <p>{results.rationale}</p>

            <h3>Retrieved Clauses</h3>
            <ul>
                {results.retrieved_clauses.map((clause, index) => (
                    <li key={index}>{clause}</li>
                ))}
            </ul>
        </div>
    );
}

export default ResultsDisplay;