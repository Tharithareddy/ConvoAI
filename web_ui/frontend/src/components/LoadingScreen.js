import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingScreen = ({ message = "Processing your conversation..." }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800 flex items-center justify-center">
      <div className="text-center">
        <div className="glass-effect rounded-2xl p-8 max-w-md">
          <Loader2 className="w-12 h-12 text-white mx-auto mb-4 animate-spin" />
          <h2 className="text-xl font-semibold text-white mb-2">
            Please wait
          </h2>
          <p className="text-blue-100">
            {message}
          </p>
          <div className="mt-6">
            <div className="flex justify-center space-x-2">
              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingScreen;