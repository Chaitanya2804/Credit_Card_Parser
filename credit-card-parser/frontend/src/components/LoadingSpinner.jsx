import React from 'react';

function LoadingSpinner() {
  return (
    <div className="flex flex-col justify-center items-center py-16">
      <div className="relative">
        <div className="animate-spin rounded-full h-20 w-20 border-b-4 border-indigo-600"></div>
        <div className="absolute top-0 left-0 animate-ping rounded-full h-20 w-20 border-4 border-indigo-400 opacity-20"></div>
      </div>
      <p className="mt-6 text-lg font-semibold text-gray-700 animate-pulse">
        Processing your statement...
      </p>
      <p className="mt-2 text-sm text-gray-500">
        This may take a few seconds
      </p>
    </div>
  );
}

export default LoadingSpinner;