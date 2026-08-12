import React from 'react';
import { MessageCircle, Brain, BarChart3, Sparkles } from 'lucide-react';

const WelcomeScreen = ({ onStartConversation }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        {/* Header */}
        <div className="text-center mb-12 fade-in">
          <div className="flex items-center justify-center mb-6">
            <MessageCircle className="w-16 h-16 text-white mr-4" />
            <h1 className="text-6xl font-bold text-white">
              Convo<span className="text-yellow-300">AI</span>
            </h1>
          </div>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Intelligent Conversational AI with Advanced Response Analysis
          </p>
        </div>

        {/* Main Card */}
        <div className="glass-effect rounded-2xl p-8 mb-8 slide-up">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-semibold text-white mb-4">
              Welcome to Your Personal AI Conversation Partner
            </h2>
            <p className="text-blue-100 text-lg">
              I'll ask you thoughtful questions and analyze your responses to provide
              insights about your thinking patterns, values, and perspectives.
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center p-6 rounded-xl bg-white bg-opacity-10">
              <Brain className="w-12 h-12 text-yellow-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">
                Smart Questions
              </h3>
              <p className="text-blue-100 text-sm">
                Adaptive questions that adjust based on your response patterns
              </p>
            </div>

            <div className="text-center p-6 rounded-xl bg-white bg-opacity-10">
              <BarChart3 className="w-12 h-12 text-green-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">
                Real-time Analysis
              </h3>
              <p className="text-blue-100 text-sm">
                Instant feedback on sentiment, emotions, and key themes
              </p>
            </div>

            <div className="text-center p-6 rounded-xl bg-white bg-opacity-10">
              <Sparkles className="w-12 h-12 text-pink-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">
                Personal Insights
              </h3>
              <p className="text-blue-100 text-sm">
                Personalized recommendations and deep insights about yourself
              </p>
            </div>
          </div>

          {/* How it Works */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold text-white mb-4 text-center">
              How It Works
            </h3>
            <div className="space-y-3">
              <div className="flex items-center text-blue-100">
                <div className="w-8 h-8 bg-yellow-300 text-purple-800 rounded-full flex items-center justify-center font-bold mr-4 flex-shrink-0">
                  1
                </div>
                <p>I'll ask you questions from different categories: personal goals, values, problem-solving, and more</p>
              </div>
              <div className="flex items-center text-blue-100">
                <div className="w-8 h-8 bg-green-300 text-purple-800 rounded-full flex items-center justify-center font-bold mr-4 flex-shrink-0">
                  2
                </div>
                <p>You respond naturally - there are no right or wrong answers</p>
              </div>
              <div className="flex items-center text-blue-100">
                <div className="w-8 h-8 bg-pink-300 text-purple-800 rounded-full flex items-center justify-center font-bold mr-4 flex-shrink-0">
                  3
                </div>
                <p>I analyze your responses and provide real-time insights</p>
              </div>
              <div className="flex items-center text-blue-100">
                <div className="w-8 h-8 bg-blue-300 text-purple-800 rounded-full flex items-center justify-center font-bold mr-4 flex-shrink-0">
                  4
                </div>
                <p>Get comprehensive analysis and personalized recommendations</p>
              </div>
            </div>
          </div>

          {/* Start Button */}
          <div className="text-center">
            <button
              onClick={onStartConversation}
              className="btn-primary text-xl px-12 py-4 transform hover:scale-105 transition-all duration-300"
            >
              Start Conversation
            </button>
            <p className="text-blue-100 text-sm mt-4">
              No registration required • Completely private • Takes 10-15 minutes
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-blue-200 text-sm">
          <p>
            🔒 All conversations are processed locally and privately
          </p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;