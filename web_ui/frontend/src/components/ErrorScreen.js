import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

const ErrorScreen = ({ error, onRetry }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="glass-effect rounded-2xl p-8 text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertCircle className="w-8 h-8 text-red-600" />
          </div>
          
          <h2 className="text-2xl font-bold text-white mb-2">
            {error?.title || 'Something went wrong'}
          </h2>
          
          <p className="text-blue-100 mb-6">
            {error?.message || 'An unexpected error occurred. Please try again.'}
          </p>
          
          {onRetry && (
            <button
              onClick={onRetry}
              className="btn-primary inline-flex items-center"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              {error?.action || 'Try Again'}
            </button>
          )}
          
          <div className="mt-6 text-sm text-blue-200">
            <p>
              If the problem persists, please ensure:
            </p>
            <ul className="mt-2 space-y-1 text-left">
              <li>• The Flask backend is running on port 5000</li>
              <li>• Your internet connection is stable</li>
              <li>• No firewall is blocking the connection</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorScreen;