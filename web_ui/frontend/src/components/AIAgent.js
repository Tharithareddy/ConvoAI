import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX, Mic, MicOff } from 'lucide-react';

const AIAgent = ({ 
  isVisible = true, 
  isSpeaking = false, 
  onSpeechComplete = null,
  currentMessage = '',
  enableVoice = true
}) => {
  const [voiceEnabled, setVoiceEnabled] = useState(enableVoice);
  const [isListening, setIsListening] = useState(false);
  const [currentUtterance, setCurrentUtterance] = useState(null);
  const [animationState, setAnimationState] = useState('idle'); // idle, speaking, listening

  // Speech synthesis setup
  useEffect(() => {
    if ('speechSynthesis' in window) {
      console.log('Speech synthesis is supported');
    } else {
      console.log('Speech synthesis not supported');
      setVoiceEnabled(false);
    }
  }, []);

  // Handle speaking state changes
  useEffect(() => {
    if (isSpeaking) {
      setAnimationState('speaking');
    } else {
      setAnimationState('idle');
    }
  }, [isSpeaking]);

  // Speak message function
  const speakMessage = (message) => {
    if (!voiceEnabled || !message || !window.speechSynthesis) return;

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(message);
    
    // Configure voice settings
    utterance.rate = 0.9; // Slightly slower for clarity
    utterance.pitch = 1.1; // Slightly higher pitch for friendliness
    utterance.volume = 0.8;
    
    // Try to get a pleasant voice
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(voice => 
      voice.name.includes('Female') || 
      voice.name.includes('Zira') || 
      voice.name.includes('Samantha') ||
      voice.lang.includes('en-US')
    );
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    // Event handlers
    utterance.onstart = () => {
      setAnimationState('speaking');
    };

    utterance.onend = () => {
      setAnimationState('idle');
      setCurrentUtterance(null);
      if (onSpeechComplete) {
        onSpeechComplete();
      }
    };

    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setAnimationState('idle');
      setCurrentUtterance(null);
    };

    setCurrentUtterance(utterance);
    window.speechSynthesis.speak(utterance);
  };

  // Auto-speak current message
  useEffect(() => {
    if (currentMessage && voiceEnabled && isVisible) {
      // Add a small delay for natural feel
      setTimeout(() => {
        speakMessage(currentMessage);
      }, 500);
    }
  }, [currentMessage, voiceEnabled, isVisible]);

  const toggleVoice = () => {
    if (currentUtterance) {
      window.speechSynthesis.cancel();
      setCurrentUtterance(null);
      setAnimationState('idle');
    }
    setVoiceEnabled(!voiceEnabled);
  };

  const stopSpeaking = () => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setCurrentUtterance(null);
      setAnimationState('idle');
    }
  };

  if (!isVisible) return null;

  return (
    <div className="ai-agent-container flex flex-col items-center">
      {/* AI Avatar */}
      <div className="relative mb-4">
        {/* Outer ring - animated when speaking */}
        <div className={`
          absolute inset-0 rounded-full border-4 border-blue-300 
          ${animationState === 'speaking' ? 'animate-ping' : ''}
        `} />
        
        {/* Middle ring - pulse animation */}
        <div className={`
          absolute inset-2 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 opacity-30
          ${animationState === 'speaking' ? 'animate-pulse' : ''}
        `} />
        
        {/* AI Avatar Face */}
        <div className="relative w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
          
          {/* Eyes */}
          <div className="flex space-x-3 mb-2">
            <div className={`
              w-3 h-3 bg-white rounded-full transition-all duration-200
              ${animationState === 'speaking' ? 'animate-bounce' : ''}
            `}>
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-0.5 ml-0.5" />
            </div>
            <div className={`
              w-3 h-3 bg-white rounded-full transition-all duration-200
              ${animationState === 'speaking' ? 'animate-bounce' : ''}
              ${animationState === 'speaking' ? 'animation-delay-100' : ''}
            `}>
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-0.5 ml-0.5" />
            </div>
          </div>
          
          {/* Mouth - changes based on state */}
          <div className="absolute bottom-6">
            {animationState === 'speaking' ? (
              <div className="w-4 h-2 bg-white rounded-full animate-pulse" />
            ) : (
              <div className="w-3 h-1 bg-white rounded-full" />
            )}
          </div>
          
          {/* Speaking indicator */}
          {animationState === 'speaking' && (
            <div className="absolute -bottom-2 -right-2">
              <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center animate-pulse">
                <Volume2 className="w-3 h-3 text-white" />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Agent Name */}
      <div className="text-center mb-3">
        <h3 className="text-white font-semibold text-lg">Aria</h3>
        <p className="text-blue-100 text-sm">
          {animationState === 'speaking' ? 'Speaking...' : 
           animationState === 'listening' ? 'Listening...' : 'AI Assistant'}
        </p>
      </div>

      {/* Voice Controls */}
      <div className="flex space-x-2">
        <button
          onClick={toggleVoice}
          className={`
            p-2 rounded-full transition-all duration-200 
            ${voiceEnabled 
              ? 'bg-green-500 hover:bg-green-600 text-white' 
              : 'bg-gray-500 hover:bg-gray-600 text-white'
            }
          `}
          title={voiceEnabled ? 'Disable Voice' : 'Enable Voice'}
        >
          {voiceEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
        </button>

        {animationState === 'speaking' && (
          <button
            onClick={stopSpeaking}
            className="p-2 rounded-full bg-red-500 hover:bg-red-600 text-white transition-all duration-200"
            title="Stop Speaking"
          >
            <VolumeX className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Speech Status */}
      {currentMessage && (
        <div className="mt-4 max-w-xs text-center">
          <div className="glass-effect rounded-lg p-3">
            <p className="text-white text-sm">
              {animationState === 'speaking' ? '🗣️ ' : '💭 '}
              {currentMessage.length > 80 
                ? currentMessage.substring(0, 80) + '...' 
                : currentMessage}
            </p>
          </div>
        </div>
      )}

      <style jsx>{`
        .ai-agent-container {
          animation: fadeIn 0.5s ease-in-out;
        }
        
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .animation-delay-100 {
          animation-delay: 0.1s;
        }
      `}</style>
    </div>
  );
};

export default AIAgent;