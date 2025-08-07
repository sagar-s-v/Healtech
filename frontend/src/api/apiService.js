import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
    baseURL: `${API_BASE_URL}/api/v1`,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadDocument = (file, docType) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('doc_type', docType);

    return apiClient.post('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

export const getDocuments = () => {
    return apiClient.get('/documents/');
};

// MODIFIED FUNCTION
export const postQuery = (query, documentId, signal) => {
    return apiClient.post('/query/', {
        query: query,
        document_id: documentId,
    }, {
        signal: signal // Pass the signal to axios
    });
};