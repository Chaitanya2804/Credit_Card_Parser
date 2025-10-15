const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Upload failed');
  }

  return await response.json();
};

export const getResult = async (sessionId) => {
  const response = await fetch(`${API_URL}/results/${sessionId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch result');
  }

  return await response.json();
};

export const getHistory = async () => {
  const response = await fetch(`${API_URL}/history`);

  if (!response.ok) {
    throw new Error('Failed to fetch history');
  }

  return await response.json();
};