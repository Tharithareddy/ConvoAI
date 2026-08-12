import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Brain, Heart, Target, RefreshCw, Download } from 'lucide-react';
import { apiService } from '../services/api';

const AnalysisScreen = ({ sessionData, onStartNew }) => {
  const [finalAnalysis, setFinalAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (sessionData.sessionId && sessionData.responses.length > 0) {
      loadFinalAnalysis();
    } else {
      setLoading(false);
    }
  }, [sessionData.sessionId]);

  const loadFinalAnalysis = async () => {
    try {
      const analysis = await apiService.getFinalAnalysis(sessionData.sessionId);
      setFinalAnalysis(analysis);
    } catch (error) {
      console.error('Failed to load final analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentDistribution = () => {
    if (!finalAnalysis?.session_summary?.sentiment_distribution) return [];
    
    const dist = finalAnalysis.session_summary.sentiment_distribution;
    return [
      { name: 'Positive', value: dist.positive || 0, color: '#10b981' },
      { name: 'Neutral', value: dist.neutral || 0, color: '#6b7280' },
      { name: 'Negative', value: dist.negative || 0, color: '#ef4444' }
    ];
  };

  const getEngagementDistribution = () => {
    if (!finalAnalysis?.session_summary?.engagement_distribution) return [];
    
    const dist = finalAnalysis.session_summary.engagement_distribution;
    return [
      { name: 'High', value: dist.high || 0, color: '#3b82f6' },
      { name: 'Medium', value: dist.medium || 0, color: '#f59e0b' },
      { name: 'Low', value: dist.low || 0, color: '#6b7280' }
    ];
  };

  const downloadAnalysis = () => {
    const dataStr = JSON.stringify({
      session_data: sessionData,
      final_analysis: finalAnalysis
    }, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `convoai-analysis-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800 flex items-center justify-center">
        <div className="text-center">
          <Brain className="w-16 h-16 text-white mx-auto mb-4 animate-pulse" />
          <h2 className="text-2xl font-bold text-white mb-2">Analyzing Your Responses</h2>
          <p className="text-blue-100">Generating comprehensive insights...</p>
        </div>
      </div>
    );
  }

  if (!sessionData.responses || sessionData.responses.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800 flex items-center justify-center p-4">
        <div className="max-w-md text-center">
          <div className="glass-effect rounded-2xl p-8">
            <Brain className="w-16 h-16 text-white mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-white mb-2">No Responses to Analyze</h2>
            <p className="text-blue-100 mb-6">
              Start a conversation to see your personalized analysis.
            </p>
            <button onClick={onStartNew} className="btn-primary">
              Start New Conversation
            </button>
          </div>
        </div>
      </div>
    );
  }

  const summary = finalAnalysis?.session_summary || {};
  const insights = finalAnalysis?.key_insights || [];
  const recommendations = finalAnalysis?.recommendations || [];
  const patterns = finalAnalysis?.patterns_identified || {};

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800">
      {/* Header */}
      <div className="bg-white bg-opacity-10 backdrop-blur-sm border-b border-white border-opacity-20 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">Your ConvoAI Analysis</h1>
              <p className="text-blue-100">
                Comprehensive insights from {sessionData.responses.length} responses
              </p>
            </div>
            
            <div className="flex space-x-4">
              <button
                onClick={downloadAnalysis}
                className="btn-secondary inline-flex items-center"
              >
                <Download className="w-4 h-4 mr-2" />
                Download
              </button>
              <button
                onClick={onStartNew}
                className="btn-primary inline-flex items-center"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                New Session
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-6xl mx-auto p-6">
        <div className="flex space-x-1 mb-8">
          {[
            { id: 'overview', label: 'Overview', icon: BarChart3 },
            { id: 'patterns', label: 'Patterns', icon: TrendingUp },
            { id: 'insights', label: 'Insights', icon: Brain },
            { id: 'responses', label: 'Responses', icon: Heart }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-4 py-2 rounded-lg transition-all duration-200 ${
                activeTab === tab.id
                  ? 'bg-white text-purple-600 shadow-lg'
                  : 'text-white hover:bg-white hover:bg-opacity-10'
              }`}
            >
              <tab.icon className="w-4 h-4 mr-2" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Session Stats */}
              <div className="lg:col-span-1">
                <div className="bg-white rounded-2xl p-6 shadow-lg">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                    <BarChart3 className="w-5 h-5 text-blue-600 mr-2" />
                    Session Overview
                  </h3>
                  
                  <div className="space-y-4">
                    <div className="flex justify-between items-center py-2 border-b border-gray-100">
                      <span className="text-gray-600">Total Responses</span>
                      <span className="font-semibold text-lg">{summary.total_responses || 0}</span>
                    </div>
                    
                    <div className="flex justify-between items-center py-2 border-b border-gray-100">
                      <span className="text-gray-600">Avg. Word Count</span>
                      <span className="font-semibold">{Math.round(summary.average_word_count || 0)} words</span>
                    </div>
                    
                    <div className="flex justify-between items-center py-2 border-b border-gray-100">
                      <span className="text-gray-600">Complexity Score</span>
                      <span className="font-semibold">{((summary.average_complexity || 0) * 100).toFixed(0)}%</span>
                    </div>
                    
                    <div className="flex justify-between items-center py-2">
                      <span className="text-gray-600">Dominant Sentiment</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        summary.dominant_sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                        summary.dominant_sentiment === 'negative' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {summary.dominant_sentiment?.charAt(0).toUpperCase() + summary.dominant_sentiment?.slice(1) || 'Neutral'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Sentiment & Engagement Charts */}
              <div className="lg:col-span-2">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  
                  {/* Sentiment Distribution */}
                  <div className="bg-white rounded-2xl p-6 shadow-lg">
                    <h4 className="font-semibold text-gray-800 mb-4">Sentiment Distribution</h4>
                    <div className="space-y-3">
                      {getSentimentDistribution().map((item) => (
                        <div key={item.name} className="flex items-center">
                          <div className="w-4 h-4 rounded-full mr-3" style={{ backgroundColor: item.color }}></div>
                          <span className="text-gray-600 flex-1">{item.name}</span>
                          <span className="font-semibold">{item.value}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Engagement Distribution */}
                  <div className="bg-white rounded-2xl p-6 shadow-lg">
                    <h4 className="font-semibold text-gray-800 mb-4">Engagement Levels</h4>
                    <div className="space-y-3">
                      {getEngagementDistribution().map((item) => (
                        <div key={item.name} className="flex items-center">
                          <div className="w-4 h-4 rounded-full mr-3" style={{ backgroundColor: item.color }}></div>
                          <span className="text-gray-600 flex-1">{item.name}</span>
                          <span className="font-semibold">{item.value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Top Themes */}
                {summary.top_themes && summary.top_themes.length > 0 && (
                  <div className="bg-white rounded-2xl p-6 shadow-lg mt-6">
                    <h4 className="font-semibold text-gray-800 mb-4 flex items-center">
                      <Target className="w-5 h-5 text-purple-600 mr-2" />
                      Key Themes
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {summary.top_themes.map((theme, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium"
                        >
                          {theme}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Patterns Tab */}
          {activeTab === 'patterns' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Sentiment Trend */}
              {patterns.sentiment_trend && patterns.sentiment_trend.length > 0 && (
                <div className="bg-white rounded-2xl p-6 shadow-lg">
                  <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
                    <TrendingUp className="w-5 h-5 text-blue-600 mr-2" />
                    Sentiment Progression
                  </h3>
                  <div className="flex items-center space-x-2">
                    {patterns.sentiment_trend.map((sentiment, index) => (
                      <React.Fragment key={index}>
                        <div className={`px-2 py-1 rounded text-xs font-medium ${
                          sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                          sentiment === 'negative' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {sentiment}
                        </div>
                        {index < patterns.sentiment_trend.length - 1 && (
                          <span className="text-gray-400">→</span>
                        )}
                      </React.Fragment>
                    ))}
                  </div>
                </div>
              )}

              {/* Common Emotions */}
              {patterns.common_emotions && patterns.common_emotions.length > 0 && (
                <div className="bg-white rounded-2xl p-6 shadow-lg">
                  <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
                    <Heart className="w-5 h-5 text-pink-600 mr-2" />
                    Frequent Emotions
                  </h3>
                  <div className="space-y-2">
                    {patterns.common_emotions.map((emotion, index) => (
                      <div key={index} className="flex items-center">
                        <span className="w-2 h-2 bg-pink-400 rounded-full mr-3"></span>
                        <span className="text-gray-700 capitalize">{emotion}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Recurring Themes */}
              {patterns.recurring_themes && patterns.recurring_themes.length > 0 && (
                <div className="bg-white rounded-2xl p-6 shadow-lg md:col-span-2">
                  <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
                    <Target className="w-5 h-5 text-purple-600 mr-2" />
                    Recurring Themes Across Responses
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {patterns.recurring_themes.map((theme, index) => (
                      <span
                        key={index}
                        className="px-3 py-2 bg-gradient-to-r from-purple-100 to-blue-100 text-purple-800 rounded-lg font-medium"
                      >
                        {theme}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Insights Tab */}
          {activeTab === 'insights' && (
            <div className="space-y-6">
              
              {/* Key Insights */}
              {insights.length > 0 && (
                <div className="bg-white rounded-2xl p-6 shadow-lg">
                  <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                    <Brain className="w-6 h-6 text-purple-600 mr-3" />
                    Key Insights About Your Communication Style
                  </h3>
                  <div className="space-y-4">
                    {insights.map((insight, index) => (
                      <div key={index} className="flex items-start p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-100">
                        <div className="w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-4 flex-shrink-0 mt-0.5">
                          {index + 1}
                        </div>
                        <p className="text-gray-700 leading-relaxed">{insight}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Recommendations */}
              {recommendations.length > 0 && (
                <div className="bg-white rounded-2xl p-6 shadow-lg">
                  <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                    <Target className="w-6 h-6 text-green-600 mr-3" />
                    Personalized Recommendations
                  </h3>
                  <div className="space-y-4">
                    {recommendations.map((recommendation, index) => (
                      <div key={index} className="flex items-start p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-100">
                        <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-4 flex-shrink-0 mt-0.5">
                          💡
                        </div>
                        <p className="text-gray-700 leading-relaxed">{recommendation}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Responses Tab */}
          {activeTab === 'responses' && (
            <div className="space-y-4">
              {sessionData.responses.map((item, index) => (
                <div key={index} className="bg-white rounded-2xl p-6 shadow-lg">
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-gray-800">
                        Question {index + 1}
                      </h4>
                      <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                        {item.question.category?.replace('_', ' ').toUpperCase()}
                      </span>
                    </div>
                    <p className="text-gray-600 italic">{item.question.text}</p>
                  </div>
                  
                  <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                    <p className="text-gray-800">{item.response}</p>
                  </div>
                  
                  {item.analysis && (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
                      <div className="text-center">
                        <div className="font-medium text-gray-600">Sentiment</div>
                        <div className={`mt-1 px-2 py-1 rounded text-xs ${
                          item.analysis.sentiment?.overall === 'positive' ? 'bg-green-100 text-green-800' :
                          item.analysis.sentiment?.overall === 'negative' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {item.analysis.sentiment?.overall || 'neutral'}
                        </div>
                      </div>
                      
                      <div className="text-center">
                        <div className="font-medium text-gray-600">Engagement</div>
                        <div className={`mt-1 px-2 py-1 rounded text-xs ${
                          item.analysis.engagement_level?.level === 'high' ? 'bg-blue-100 text-blue-800' :
                          item.analysis.engagement_level?.level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {item.analysis.engagement_level?.level || 'medium'}
                        </div>
                      </div>
                      
                      <div className="text-center">
                        <div className="font-medium text-gray-600">Word Count</div>
                        <div className="mt-1 font-semibold">{item.analysis.response_length || 0}</div>
                      </div>
                      
                      <div className="text-center">
                        <div className="font-medium text-gray-600">Complexity</div>
                        <div className="mt-1 font-semibold">
                          {((item.analysis.complexity_score || 0) * 100).toFixed(0)}%
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <div className="glass-effect rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-white mb-2">
              Thank you for using ConvoAI!
            </h3>
            <p className="text-blue-100 mb-4">
              Your conversation data has been analyzed and saved locally.
            </p>
            <button
              onClick={onStartNew}
              className="btn-primary"
            >
              Start Another Conversation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisScreen;