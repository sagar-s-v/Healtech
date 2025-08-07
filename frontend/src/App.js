import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import DocumentList from './components/DocumentList';
import QueryForm from './components/QueryForm';
import ResultsDisplay from './components/ResultsDisplay';
import { getDocuments, postQuery } from './api/apiService';
import axios from 'axios'; // Import axios to check for cancel error

function App() {
    const [documents, setDocuments] = useState([]);
    const [selectedDocId, setSelectedDocId] = useState(null);
    const [queryResults, setQueryResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    // State to hold the controller for the active query
    const [queryController, setQueryController] = useState(null);


    const fetchDocuments = useCallback(async () => {
        try {
            const response = await getDocuments();
            setDocuments(response.data);
        } catch (err) {
            setError('Failed to fetch documents.');
        }
    }, []);

    useEffect(() => {
        fetchDocuments();
        const interval = setInterval(fetchDocuments, 5000);
        return () => clearInterval(interval);
    }, [fetchDocuments]);
    
    // NEW FUNCTION to handle query cancellation
    const handleCancelQuery = () => {
        if (queryController) {
            queryController.abort();
            setError("Query canceled by user.");
        }
    };

    const handleQueryStart = async (query) => { // Modified to receive query directly
        if (!query.trim() || !selectedDocId) {
            setError("Please select a document and enter a query.");
            return;
        }

        // Create a new AbortController for this request
        const controller = new AbortController();
        setQueryController(controller);

        setIsLoading(true);
        setError('');
        setQueryResults(null);

        try {
            const response = await postQuery(query, selectedDocId, controller.signal);
            setQueryResults(response.data);
        } catch (error) {
            // Check if the error is from cancellation
            if (axios.isCancel(error)) {
                console.log('Request canceled:', error.message);
                setError("Query canceled by user.");
            } else {
                const errorMsg = error.response?.data?.detail || 'An error occurred while querying.';
                setError(errorMsg);
            }
        } finally {
            setIsLoading(false);
            setQueryController(null);
        }
    };

    const handleUploadSuccess = () => {
        fetchDocuments();
    };


    return (
        <div className="App">
            <h1>📄 Intelligent Query-Retrieval System</h1>
            <div className="container">
                <div className="left-panel">
                    <FileUpload onUploadSuccess={handleUploadSuccess} />
                    <hr />
                    <DocumentList
                        documents={documents}
                        selectedDocId={selectedDocId}
                        onSelectDoc={setSelectedDocId}
                    />
                </div>
                <div className="right-panel">
                    {/* Simplified QueryForm call */}
                    <QueryForm
                        selectedDocId={selectedDocId}
                        onQuerySubmit={handleQueryStart}
                    />
                    <hr />
                    {/* Pass the cancel handler to the results display */}
                    <ResultsDisplay
                        results={queryResults}
                        isLoading={isLoading}
                        error={error}
                        onCancel={handleCancelQuery}
                    />
                </div>
            </div>
        </div>
    );
}

export default App;