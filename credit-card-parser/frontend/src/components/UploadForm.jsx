import React from 'react';

function UploadForm({ file, loading, error, onFileChange, onUpload, onReset }) {
  return (
    <div className="max-w-2xl mx-auto mb-8">
      <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-100">
        <h2 className="text-2xl font-semibold mb-6 text-gray-800 flex items-center">
          <span className="mr-2">📤</span>
          Upload Statement
        </h2>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Select PDF File
          </label>
          <div className="relative">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => onFileChange(e.target.files[0])}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-3 file:px-6
                file:rounded-lg file:border-0
                file:text-sm file:font-semibold
                file:bg-indigo-50 file:text-indigo-700
                hover:file:bg-indigo-100 
                cursor-pointer transition-all duration-200
                border border-gray-200 rounded-lg p-2"
              disabled={loading}
            />
          </div>
        </div>

        {file && (
          <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <svg className="w-8 h-8 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                <div>
                  <p className="text-sm font-medium text-blue-900">{file.name}</p>
                  <p className="text-xs text-blue-600">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              </div>
              <button
                onClick={onReset}
                className="text-red-600 hover:text-red-800 text-sm font-medium"
                disabled={loading}
              >
                Remove
              </button>
            </div>
          </div>
        )}

        <button
          onClick={onUpload}
          disabled={!file || loading}
          className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 px-6 rounded-lg
            font-semibold hover:from-indigo-700 hover:to-purple-700 
            disabled:from-gray-400 disabled:to-gray-400
            disabled:cursor-not-allowed transition-all duration-200
            transform hover:scale-105 active:scale-95
            shadow-lg hover:shadow-xl"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </span>
          ) : (
            '🚀 Parse Statement'
          )}
        </button>

        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-red-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="text-red-800 text-sm font-medium">{error}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadForm;