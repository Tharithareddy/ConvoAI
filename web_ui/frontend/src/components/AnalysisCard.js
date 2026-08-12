import React from 'react';
import { TrendingUp, TrendingDown, Minus, Heart, Brain, MessageSquare, Target } from 'lucide-react';

const AnalysisCard = ({ analysis }) => {
  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case 'positive': return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'negative': return <TrendingDown className="w-4 h-4 text-red-600" />;
      default: return <Minus className="w-4 h-4 text-gray-600" />;
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return 'bg-green-50 text-green-800 border-green-200';
      case 'negative': return 'bg-red-50 text-red-800 border-red-200';
      default: return 'bg-gray-50 text-gray-800 border-gray-200';
    }
  };

  const getEngagementColor = (level) => {
    switch (level) {
      case 'high': return 'bg-blue-50 text-blue-800 border-blue-200';
      case 'medium': return 'bg-yellow-50 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-gray-50 text-gray-800 border-gray-200';
      default: return 'bg-gray-50 text-gray-800 border-gray-200';
    }
  };

  const getComplexityWidth = (score) => {
    return Math.max(10, score * 100); // Minimum 10% width
  };

  if (!analysis) return null;

  return (
    <div className="bg-gradient-to-r from-white to-blue-50 rounded-xl p-4 border border-blue-100 shadow-sm slide-up">
      <div className="flex items-center mb-3">
        <Brain className="w-5 h-5 text-purple-600 mr-2" />
        <h4 className="font-medium text-gray-800">Response Analysis</h4>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        {/* Sentiment */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-600">Sentiment</span>
            <div className={`flex items-center px-2 py-1 rounded-full text-xs border ${getSentimentColor(analysis.sentiment?.overall)}`}>
              {getSentimentIcon(analysis.sentiment?.overall)}
              <span className="ml-1 capitalize">{analysis.sentiment?.overall || 'neutral'}</span>
            </div>
          </div>
          {analysis.sentiment?.confidence && (
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-purple-400 to-blue-400 h-2 rounded-full transition-all duration-500"
                style={{ width: `${(analysis.sentiment.confidence * 100)}%` }}
              />
            </div>
          )}
        </div>

        {/* Engagement */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-600">Engagement</span>
            <div className={`flex items-center px-2 py-1 rounded-full text-xs border ${getEngagementColor(analysis.engagement_level?.level)}`}>
              <MessageSquare className="w-3 h-3 mr-1" />
              <span className="capitalize">{analysis.engagement_level?.level || 'medium'}</span>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            {analysis.response_length} words • {analysis.engagement_level?.word_count} chars
          </div>
        </div>

        {/* Complexity */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-600">Complexity</span>
            <span className="text-xs font-medium text-purple-600">
              {((analysis.complexity_score || 0) * 100).toFixed(0)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-green-400 to-blue-400 h-2 rounded-full transition-all duration-500"
              style={{ width: `${getComplexityWidth(analysis.complexity_score || 0)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Key Themes */}
      {analysis.key_themes && analysis.key_themes.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center mb-2">
            <Target className="w-4 h-4 text-blue-600 mr-2" />
            <span className="text-sm font-medium text-gray-600">Key Themes</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {analysis.key_themes.slice(0, 5).map((theme, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full border border-blue-200"
              >
                {theme}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Emotions */}
      {analysis.emotions && analysis.emotions.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center mb-2">
            <Heart className="w-4 h-4 text-pink-600 mr-2" />
            <span className="text-sm font-medium text-gray-600">Emotions Detected</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {analysis.emotions.slice(0, 3).map((emotion, index) => (
              <div
                key={index}
                className="flex items-center px-2 py-1 bg-pink-50 text-pink-800 text-xs rounded-full border border-pink-200"
              >
                <span>{emotion.emotion}</span>
                {emotion.strength > 1 && (
                  <span className="ml-1 text-xs font-bold">×{emotion.strength}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Goals and Values */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {analysis.goals_mentioned && analysis.goals_mentioned.length > 0 && (
          <div>
            <span className="text-xs font-medium text-gray-600 mb-1 block">Goals Mentioned</span>
            <div className="space-y-1">
              {analysis.goals_mentioned.slice(0, 2).map((goal, index) => (
                <div key={index} className="text-xs text-gray-600 bg-green-50 px-2 py-1 rounded border border-green-200">
                  🎯 {goal.length > 50 ? goal.substring(0, 50) + '...' : goal}
                </div>
              ))}
            </div>
          </div>
        )}

        {analysis.values_expressed && analysis.values_expressed.length > 0 && (
          <div>
            <span className="text-xs font-medium text-gray-600 mb-1 block">Values Expressed</span>
            <div className="space-y-1">
              {analysis.values_expressed.slice(0, 2).map((value, index) => (
                <div key={index} className="text-xs text-gray-600 bg-purple-50 px-2 py-1 rounded border border-purple-200">
                  💎 {value.length > 50 ? value.substring(0, 50) + '...' : value}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Quick Insights */}
      <div className="mt-4 pt-3 border-t border-gray-200">
        <div className="text-xs text-gray-600">
          <span className="font-medium">Quick Insight:</span>{' '}
          {analysis.sentiment?.overall === 'positive' && analysis.engagement_level?.level === 'high' 
            ? 'You seem enthusiastic and engaged with this topic!'
            : analysis.engagement_level?.level === 'high'
            ? 'Great detail in your response - this shows deep thinking.'
            : analysis.sentiment?.overall === 'positive'
            ? 'Positive outlook detected in your response.'
            : analysis.complexity_score > 0.7
            ? 'Complex and nuanced thinking demonstrated.'
            : 'Thank you for sharing your thoughts on this topic.'}
        </div>
      </div>
    </div>
  );
};

export default AnalysisCard;