import { useState } from 'react';
import UploadForm from './components/UploadForm';
import ResultsView from './components/ResultsView';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const handleFileChange = (selectedFile) => {
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
      setResult(null);
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-3 tracking-tight">
            💳 Credit Card Statement Parser
          </h1>
          <p className="text-lg text-gray-600">
            Extract key details from your credit card statements instantly
          </p>
          <div className="mt-4 flex justify-center gap-3 flex-wrap">
            <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
              HDFC Bank
            </span>
            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
              SBI Card
            </span>
            <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
              ICICI Bank
            </span>
            <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm font-medium">
              Axis Bank
            </span>
            <span className="px-3 py-1 bg-pink-100 text-pink-700 rounded-full text-sm font-medium">
              Kotak Mahindra
            </span>
          </div>
        </header>

        {/* Upload Form */}
        <UploadForm
          file={file}
          loading={loading}
          error={error}
          onFileChange={handleFileChange}
          onUpload={handleUpload}
          onReset={handleReset}
        />

        {/* Loading Spinner */}
        {loading && <LoadingSpinner />}

        {/* Results */}
        {result && !loading && <ResultsView result={result} />}

        {/* Footer */}
        <footer className="text-center mt-16 text-gray-600 text-sm">
          <div className="mb-2">
            <p className="font-medium">Built with FastAPI + React + PostgreSQL + Docker</p>
          </div>
          <p>© 2025 Credit Card Parser | Sure Assignment - SAKEC</p>
        </footer>
      </div>
    </div>
  );
}

export default App;