import React from 'react';
import { MessageSquare, Tag, Hash } from 'lucide-react';

const QuestionCard = ({ question, questionNumber }) => {
  const getCategoryIcon = (category) => {
    const icons = {
      personal: '🎯',
      problem_solving: '🧩',
      values: '💎',
      learning: '📚',
      reflection: '🤔',
      future: '🚀'
    };
    return icons[category] || '💬';
  };

  const getCategoryColor = (category) => {
    const colors = {
      personal: 'bg-blue-100 text-blue-800',
      problem_solving: 'bg-green-100 text-green-800',
      values: 'bg-purple-100 text-purple-800',
      learning: 'bg-yellow-100 text-yellow-800',
      reflection: 'bg-pink-100 text-pink-800',
      future: 'bg-indigo-100 text-indigo-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg border-l-4 border-purple-500 slide-up">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
            <MessageSquare className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-800">
              Question {questionNumber}
            </h3>
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(question.category)}`}>
                {getCategoryIcon(question.category)} {question.category?.replace('_', ' ').toUpperCase()}
              </span>
              {question.type && (
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                  <Tag className="w-3 h-3 inline mr-1" />
                  {question.type.replace('_', ' ')}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Question Text */}
      <div className="mb-6">
        <p className="text-lg text-gray-800 leading-relaxed font-medium">
          {question.text}
        </p>
      </div>

      {/* Multiple Choice Options */}
      {question.type === 'multiple_choice' && question.options && (
        <div className="mb-4">
          <p className="text-sm font-medium text-gray-600 mb-3">Options:</p>
          <div className="grid gap-2">
            {question.options.map((option, index) => (
              <div
                key={index}
                className="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-200"
              >
                <span className="w-6 h-6 bg-purple-100 text-purple-800 rounded-full flex items-center justify-center text-sm font-medium mr-3">
                  {index + 1}
                </span>
                <span className="text-gray-700">{option}</span>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-2">
            💡 You can respond with a number, or explain your choice in detail
          </p>
        </div>
      )}

      {/* Ranking Options */}
      {question.type === 'ranking' && question.options && (
        <div className="mb-4">
          <p className="text-sm font-medium text-gray-600 mb-3">
            Please rank these options or discuss their importance:
          </p>
          <div className="grid gap-2">
            {question.options.map((option, index) => (
              <div
                key={index}
                className="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-200"
              >
                <Hash className="w-4 h-4 text-gray-400 mr-3" />
                <span className="text-gray-700">{option}</span>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-2">
            💡 Feel free to explain your reasoning and priorities
          </p>
        </div>
      )}

      {/* Tips for better responses */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-100">
        <p className="text-sm text-gray-600">
          <span className="font-medium">💡 For better insights:</span> Be specific, share examples, and explain your reasoning. There are no wrong answers!
        </p>
      </div>
    </div>
  );
};

export default QuestionCard;