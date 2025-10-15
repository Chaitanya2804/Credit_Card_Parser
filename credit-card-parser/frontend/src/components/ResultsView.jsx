import React from 'react';

function ResultsView({ result }) {
  const getConfidenceColor = (score) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceBadge = (score) => {
    if (score >= 0.8) return 'bg-green-100 text-green-800 border-green-200';
    if (score >= 0.6) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-red-100 text-red-800 border-red-200';
  };

  const getConfidenceLabel = (score) => {
    if (score >= 0.8) return 'High Confidence';
    if (score >= 0.6) return 'Medium Confidence';
    return 'Low Confidence';
  };

  const downloadJSON = () => {
    const dataStr = JSON.stringify(result, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = `statement_${result.id}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <div className="max-w-4xl mx-auto mb-8 animate-fadeIn">
      <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-100">
        {/* Header */}
        <div className="flex justify-between items-center mb-8 pb-6 border-b border-gray-200">
          <div>
            <h2 className="text-3xl font-bold text-gray-800 flex items-center mb-2">
              <span className="mr-3">✅</span>
              Extraction Results
            </h2>
            <p className="text-sm text-gray-500">
              File: <span className="font-medium text-gray-700">{result.filename}</span>
            </p>
          </div>
          <div className="text-right">
            <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold border-2 ${getConfidenceBadge(result.confidence_score)}`}>
              {getConfidenceLabel(result.confidence_score)}
            </span>
            <p className="text-2xl font-bold text-gray-800 mt-2">
              {(result.confidence_score * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        {/* Fields Grid */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Issuer */}
          <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-5 rounded-lg border-l-4 border-indigo-500 hover:shadow-md transition-shadow">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-2">🏦</span>
              <p className="text-sm font-medium text-gray-600">Issuer</p>
            </div>
            <p className="text-xl font-bold text-gray-800 mb-1">
              {result.extracted_fields.issuer?.value || 'N/A'}
            </p>
            <p className={`text-xs font-semibold ${getConfidenceColor(result.extracted_fields.issuer?.confidence || 0)}`}>
              {((result.extracted_fields.issuer?.confidence || 0) * 100).toFixed(0)}% confidence
            </p>
          </div>

          {/* Card Last 4 */}
          <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-5 rounded-lg border-l-4 border-purple-500 hover:shadow-md transition-shadow">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-2">💳</span>
              <p className="text-sm font-medium text-gray-600">Card Last 4 Digits</p>
            </div>
            <p className="text-xl font-bold text-gray-800 mb-1">
              •••• {result.extracted_fields.card_last_four?.value || 'N/A'}
            </p>
            <p className={`text-xs font-semibold ${getConfidenceColor(result.extracted_fields.card_last_four?.confidence || 0)}`}>
              {((result.extracted_fields.card_last_four?.confidence || 0) * 100).toFixed(0)}% confidence
            </p>
          </div>

          {/* Billing Cycle */}
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-5 rounded-lg border-l-4 border-blue-500 hover:shadow-md transition-shadow">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-2">📅</span>
              <p className="text-sm font-medium text-gray-600">Billing Cycle</p>
            </div>
            <p className="text-lg font-bold text-gray-800 mb-1">
              {result.extracted_fields.billing_cycle?.value || 'N/A'}
            </p>
            <p className={`text-xs font-semibold ${getConfidenceColor(result.extracted_fields.billing_cycle?.confidence || 0)}`}>
              {((result.extracted_fields.billing_cycle?.confidence || 0) * 100).toFixed(0)}% confidence
            </p>
          </div>

          {/* Due Date */}
          <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-5 rounded-lg border-l-4 border-green-500 hover:shadow-md transition-shadow">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-2">⏰</span>
              <p className="text-sm font-medium text-gray-600">Payment Due Date</p>
            </div>
            <p className="text-xl font-bold text-gray-800 mb-1">
              {result.extracted_fields.due_date?.value || 'N/A'}
            </p>
            <p className={`text-xs font-semibold ${getConfidenceColor(result.extracted_fields.due_date?.confidence || 0)}`}>
              {((result.extracted_fields.due_date?.confidence || 0) * 100).toFixed(0)}% confidence
            </p>
          </div>

          {/* Total Amount */}
          <div className="md:col-span-2 bg-gradient-to-br from-orange-50 to-red-50 p-6 rounded-lg border-l-4 border-red-500 hover:shadow-md transition-shadow">
            <div className="flex items-center mb-2">
              <span className="text-3xl mr-2">💰</span>
              <p className="text-sm font-medium text-gray-600">Total Amount Due</p>
            </div>
            <p className="text-3xl font-bold text-gray-800 mb-1">
              {result.extracted_fields.total_amount_due?.value || 'N/A'}
            </p>
            <p className={`text-xs font-semibold ${getConfidenceColor(result.extracted_fields.total_amount_due?.confidence || 0)}`}>
              {((result.extracted_fields.total_amount_due?.confidence || 0) * 100).toFixed(0)}% confidence
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-4 pt-6 border-t border-gray-200">
          <button
            onClick={downloadJSON}
            className="flex-1 bg-gray-800 text-white py-3 px-6 rounded-lg font-semibold
              hover:bg-gray-900 transition-colors duration-200 flex items-center justify-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download JSON
          </button>
        </div>

        {/* Footer Info */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-xs text-gray-500">
            <div>
              <p className="font-medium text-gray-600">Session ID</p>
              <p className="font-mono mt-1">{result.id}</p>
            </div>
            <div>
              <p className="font-medium text-gray-600">Status</p>
              <p className="mt-1">
                <span className="inline-block px-2 py-1 bg-green-100 text-green-800 rounded font-medium">
                  {result.status}
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsView;