import React from 'react';

const ProgressIndicator = ({ current, total }) => {
  const percentage = Math.min(100, (current / total) * 100);
  
  return (
    <div className="flex items-center space-x-3">
      <div className="w-20 bg-white bg-opacity-20 rounded-full h-2">
        <div 
          className="bg-gradient-to-r from-yellow-300 to-green-300 h-2 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-white text-sm font-medium">
        {current}/{total}
      </span>
    </div>
  );
};

export default ProgressIndicator;