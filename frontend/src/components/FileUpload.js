import React, { useState } from 'react';
import { uploadDocument } from '../api/apiService';

function FileUpload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [docType, setDocType] = useState('pdf');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setMessage('Please select a file to upload.');
            return;
        }

        setIsLoading(true);
        setMessage('Uploading and processing document... Please wait.');

        try {
            await uploadDocument(file, docType);
            setMessage('Document uploaded successfully! It is now being processed.');
            onUploadSuccess(); // Refresh document list
            setFile(null); // Clear file input
            e.target.reset();
        } catch (error) {
            const errorMsg = error.response?.data?.detail || 'An error occurred during upload.';
            setMessage(`Error: ${errorMsg}`);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h2>1. Upload Document</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="file">Choose File</label>
                    <input type="file" id="file" onChange={handleFileChange} accept=".pdf,.docx,.eml" />
                </div>
                <div className="form-group">
                    <label htmlFor="docType">Document Type</label>
                    <select id="docType" value={docType} onChange={(e) => setDocType(e.target.value)}>
                        <option value="pdf">PDF</option>
                        <option value="docx">DOCX</option>
                        <option value="eml">Email (.eml)</option>
                    </select>
                </div>
                <button type="submit" disabled={isLoading || !file}>
                    {isLoading ? 'Processing...' : 'Upload'}
                </button>
            </form>
            {message && <div className={`message ${isLoading ? 'loading' : (message.startsWith('Error') ? 'error' : 'success')}`}>{message}</div>}
        </div>
    );
}

export default FileUpload;