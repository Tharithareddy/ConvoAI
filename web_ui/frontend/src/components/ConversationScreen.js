import React, { useState, useRef, useEffect } from 'react';
import { Send, SkipForward, BarChart3, MessageCircle, Mic, MicOff } from 'lucide-react';
import QuestionCard from './QuestionCard';
import AnalysisCard from './AnalysisCard';
import ProgressIndicator from './ProgressIndicator';
import AIAgent from './AIAgent';
import VoiceInput from './VoiceInput';

const ConversationScreen = ({
  sessionData,
  onSubmitResponse,
  onSkipQuestion,
  onEndConversation,
  onShowSummary
}) => {
  const [currentResponse, setCurrentResponse] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [autoRecordingActive, setAutoRecordingActive] = useState(false);
  const messagesEndRef = useRef(null);
  const voiceInputRef = useRef(null);
  const autoRecordTimeoutRef = useRef(null);
  const forceRecordIntervalRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [sessionData.responses]);

  // Auto-recording when new question arrives
  useEffect(() => {
    if (sessionData.currentQuestion) {
      console.log('New question detected, starting auto-recording in 3 seconds...');
      
      // Clear any existing auto-record timeout
      if (autoRecordTimeoutRef.current) {
        clearTimeout(autoRecordTimeoutRef.current);
      }
      
      // Start auto-recording after 3 seconds
      autoRecordTimeoutRef.current = setTimeout(() => {
        console.log('Starting 5-minute forced recording session');
        setAutoRecordingActive(true);
        
        // Force recording to start
        if (voiceInputRef.current && voiceInputRef.current.startRecording) {
          voiceInputRef.current.startRecording();
        }
        
        // Set up interval to ensure recording stays active for 5 minutes
        forceRecordIntervalRef.current = setInterval(() => {
          if (voiceInputRef.current && !voiceInputRef.current.isRecording()) {
            console.log('Recording stopped, forcing restart...');
            voiceInputRef.current.startRecording();
          }
        }, 1000); // Check every second
        
        // Stop auto-recording after 5 minutes
        setTimeout(() => {
          console.log('5-minute auto-recording session complete');
          setAutoRecordingActive(false);
          
          // Clear force interval
          if (forceRecordIntervalRef.current) {
            clearInterval(forceRecordIntervalRef.current);
            forceRecordIntervalRef.current = null;
          }
          
          // Stop recording
          if (voiceInputRef.current && voiceInputRef.current.stopRecording) {
            voiceInputRef.current.stopRecording();
          }
        }, 5 * 60 * 1000); // 5 minutes
        
      }, 3000); // 3 seconds delay
    }
    
    return () => {
      // Cleanup timeouts when component unmounts or question changes
      if (autoRecordTimeoutRef.current) {
        clearTimeout(autoRecordTimeoutRef.current);
        autoRecordTimeoutRef.current = null;
      }
      if (forceRecordIntervalRef.current) {
        clearInterval(forceRecordIntervalRef.current);
        forceRecordIntervalRef.current = null;
      }
    };
  }, [sessionData.currentQuestion]);

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'en-US';
      
      recognitionInstance.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        
        if (finalTranscript) {
          setCurrentResponse(prev => prev + finalTranscript + ' ');
        }
      };
      
      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };
      
      recognitionInstance.onend = () => {
        setIsListening(false);
      };
      
      setRecognition(recognitionInstance);
      setSpeechSupported(true);
    } else {
      console.log('Speech recognition not supported');
      setSpeechSupported(false);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!currentResponse.trim() || isSubmitting) return;

    setIsSubmitting(true);
    await onSubmitResponse(currentResponse.trim());
    setCurrentResponse('');
    setIsSubmitting(false);
  };

  const toggleListening = () => {
    if (!recognition || !speechSupported) return;
    
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);
    }
  };

  const handleVoiceTranscript = (transcript) => {
    // Add the voice transcript to the current response
    setCurrentResponse(prev => {
      const newResponse = prev + (prev ? ' ' : '') + transcript;
      return newResponse;
    });
  };

  const clearResponse = () => {
    setCurrentResponse('');
  };

  const questionsAnswered = sessionData.responses.length;
  const totalEstimated = 8; // Estimated total questions

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800">
      {/* Header */}
      <div className="bg-white bg-opacity-10 backdrop-blur-sm border-b border-white border-opacity-20 p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <MessageCircle className="w-8 h-8 text-white mr-3" />
            <div>
              <h1 className="text-xl font-bold text-white">ConvoAI Session</h1>
              <p className="text-blue-100 text-sm">
                Question {questionsAnswered + 1} • {questionsAnswered} completed
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <ProgressIndicator current={questionsAnswered} total={totalEstimated} />
            <button
              onClick={onShowSummary}
              className="btn-secondary text-sm px-4 py-2"
              disabled={sessionData.responses.length === 0}
            >
              <BarChart3 className="w-4 h-4 mr-2 inline" />
              Summary
            </button>
            <button
              onClick={onEndConversation}
              className="text-white hover:text-red-200 transition-colors"
            >
              End Session
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto p-4 pb-32">
        {/* Conversation History */}
        <div className="space-y-6 mb-8">
          {sessionData.responses.map((item, index) => (
            <div key={index} className="space-y-4">
              {/* Question */}
              <div className="chat-bubble-ai fade-in">
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-3 flex-shrink-0 relative overflow-hidden">
                    {/* Mini AI Agent Face */}
                    <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                      <div className="flex space-x-1">
                        <div className="w-1 h-1 bg-white rounded-full"></div>
                        <div className="w-1 h-1 bg-white rounded-full"></div>
                      </div>
                    </div>
                    {/* Subtle glow effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 opacity-30 animate-pulse"></div>
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-sm text-gray-600 mb-1">
                      {item.question.category?.replace('_', ' ').toUpperCase()} QUESTION
                    </p>
                    <p className="text-gray-800">{item.question.text}</p>
                    
                    {/* Question options if multiple choice */}
                    {item.question.type === 'multiple_choice' && item.question.options && (
                      <div className="mt-3 space-y-1">
                        {item.question.options.map((option, optIndex) => (
                          <div key={optIndex} className="text-sm text-gray-600">
                            {optIndex + 1}. {option}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* User Response */}
              <div className="chat-bubble-user slide-up">
                <p>{item.response}</p>
              </div>

              {/* Analysis */}
              {item.analysis && (
                <AnalysisCard analysis={item.analysis} />
              )}
            </div>
          ))}
        </div>

        {/* Current Question */}
        {sessionData.currentQuestion && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
            {/* AI Agent */}
            <div className="lg:col-span-1">
              <AIAgent 
                isVisible={true}
                currentMessage={sessionData.currentQuestion.text}
                enableVoice={true}
                onSpeechComplete={() => {
                  // Speech completed, ready for voice input
                  console.log('AI finished speaking, ready for voice input');
                }}
              />
            </div>
            
            {/* Question Card */}
            <div className="lg:col-span-2">
              <QuestionCard 
                question={sessionData.currentQuestion}
                questionNumber={questionsAnswered + 1}
              />
            </div>
          </div>
        )}

        {/* Conversation Complete Message */}
        {sessionData.conversationComplete && !sessionData.currentQuestion && (
          <div className="text-center p-8">
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageCircle className="w-8 h-8 text-green-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                Conversation Complete!
              </h2>
              <p className="text-gray-600 mb-6">
                Thank you for sharing your thoughts. Let's analyze your responses.
              </p>
              <button
                onClick={onEndConversation}
                className="btn-primary"
              >
                View Analysis
              </button>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - Fixed at bottom */}
      {sessionData.currentQuestion && (
        <div className="fixed bottom-0 left-0 right-0 bg-white bg-opacity-10 backdrop-blur-sm border-t border-white border-opacity-20 p-4">
          <div className="max-w-4xl mx-auto">
            <form onSubmit={handleSubmit} className="flex items-end space-x-4">
              <div className="flex-1">
                {/* Non-editable voice input display */}
                <div 
                  className="w-full px-4 py-3 rounded-2xl border-2 border-white border-opacity-30 
                           bg-white bg-opacity-90 backdrop-blur-sm min-h-[50px] max-h-32 overflow-y-auto
                           text-gray-800"
                >
                  {currentResponse ? (
                    <div className="whitespace-pre-wrap">
                      {currentResponse}
                    </div>
                  ) : (
                    <div className="text-gray-500 italic">
                      🎤 Click the microphone button to start voice recording...
                    </div>
                  )}
                </div>
                
                {/* Character count and tips */}
                <div className="flex justify-between items-center mt-2 px-2">
                  <div className="flex items-center space-x-4">
                    <p className="text-xs text-blue-100">
                      🎤 Voice-only input • No manual editing
                    </p>
                    <p className="text-xs text-blue-200">
                      🗣️ AI speaks questions aloud
                    </p>
                  </div>
                  <p className="text-xs text-blue-200">
                    {currentResponse.length} characters
                  </p>
                </div>
              </div>

              <div className="flex space-x-2">
                {/* Enhanced Voice Input */}
                <div className="relative">
                  <VoiceInput
                    ref={voiceInputRef}
                    onTranscript={handleVoiceTranscript}
                    isDisabled={isSubmitting}
                    className="voice-input-enhanced"
                  />
                </div>

                {/* Clear Response Button */}
                {currentResponse.trim() && (
                  <button
                    type="button"
                    onClick={clearResponse}
                    className="p-3 bg-gray-500 bg-opacity-50 hover:bg-opacity-70 rounded-full 
                             transition-all duration-200 text-white text-xs border border-white border-opacity-20"
                    title="Clear Response"
                    disabled={isSubmitting}
                  >
                    Clear
                  </button>
                )}
                <button
                  type="button"
                  onClick={onSkipQuestion}
                  className="p-3 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full 
                           transition-all duration-200 text-white"
                  title="Skip Question"
                  disabled={isSubmitting}
                >
                  <SkipForward className="w-5 h-5" />
                </button>

                <button
                  type="submit"
                  className="p-3 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 
                           rounded-full transition-all duration-200 text-white shadow-lg
                           disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={!currentResponse.trim() || isSubmitting}
                >
                  {isSubmitting ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConversationScreen;