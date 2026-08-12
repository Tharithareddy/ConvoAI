import React, { useState, useEffect, useCallback, useRef, forwardRef, useImperativeHandle } from 'react';
import { Mic, MicOff, Volume2 } from 'lucide-react';

const VoiceInput = forwardRef(({ 
  onTranscript, 
  isDisabled = false,
  language = 'en-US',
  className = '' 
}, ref) => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordingTimer, setRecordingTimer] = useState(0);
  const manualStopRef = useRef(false);
  const isListeningRef = useRef(false);
  const restartTimeoutRef = useRef(null);
  const silenceTimeoutRef = useRef(null);
  const sessionStartTimeRef = useRef(null);
  const lastSpeechTimeRef = useRef(null);
  const minRecordingTimeRef = useRef(2 * 60 * 1000); // 2 minutes in milliseconds
  const silenceDelayRef = useRef(5 * 1000); // 5 seconds in milliseconds
  const timerIntervalRef = useRef(null);
  const minimumTimerRef = useRef(null);
  const microphonePermissionRef = useRef(null); // Cache microphone permission status

  // Initialize speech recognition
  useEffect(() => {
    // Check for both speech recognition and microphone support
    if (('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) && 
        ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices)) {
      
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = language;
      recognitionInstance.maxAlternatives = 1;
      
      // Set longer timeouts to prevent auto-stopping - aggressive settings
      try {
        // Some browsers support these settings to extend recording time
        if ('grammars' in recognitionInstance) {
          recognitionInstance.serviceURI = 'builtin:speech/dictation';
        }
        // Force continuous mode settings
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
      } catch (e) {
        console.log('Advanced recognition settings not supported:', e);
      }
      
      recognitionInstance.onstart = () => {
        console.log('🎤 Speech recognition started - session timer reset');
        setIsListening(true);
        setIsProcessing(false);
        manualStopRef.current = false;
        isListeningRef.current = true;
        sessionStartTimeRef.current = Date.now(); // Reset session timer on every start
        lastSpeechTimeRef.current = Date.now();
        
        // Start the visual timer
        setRecordingTimer(0);
        timerIntervalRef.current = setInterval(() => {
          const elapsed = Date.now() - sessionStartTimeRef.current;
          setRecordingTimer(Math.floor(elapsed / 1000));
        }, 1000);
        
        // Set a timer to enforce minimum recording time
        minimumTimerRef.current = setTimeout(() => {
          console.log('Minimum 2-minute recording period completed - enabling silence detection');
          // After 2 minutes, silence detection will be handled by separate monitoring
        }, minRecordingTimeRef.current);
      };
      
      recognitionInstance.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        // Update last speech time when we get any speech result
        lastSpeechTimeRef.current = Date.now();
        
        // Also update session time to indicate activity
        if (!sessionStartTimeRef.current) {
          sessionStartTimeRef.current = Date.now();
        }
        
        // Process all results
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        
        setTranscript(interimTranscript);
        
        if (finalTranscript && onTranscript) {
          onTranscript(finalTranscript);
        }
        
        // DO NOT set silence timeout here - let the onend handler manage restarts
        // The speech API will stop after final results, but we'll force restart
      };
      
      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        
        // Handle specific errors
        if (event.error === 'not-allowed') {
          alert('Microphone access denied. Please allow microphone access and try again.');
          setIsListening(false);
          setIsProcessing(false);
          setTranscript('');
          manualStopRef.current = true;
          isListeningRef.current = false;
          // Clear timers
          if (silenceTimeoutRef.current) {
            clearTimeout(silenceTimeoutRef.current);
            silenceTimeoutRef.current = null;
          }
        } else if (event.error === 'no-speech') {
          // Update last speech time even for no-speech events
          lastSpeechTimeRef.current = Date.now();
          console.log('No speech detected, but continuing to listen...');
        } else if (event.error === 'aborted') {
          console.log('Recognition was aborted');
          setIsListening(false);
          setIsProcessing(false);
          setTranscript('');
          isListeningRef.current = false;
          // Clear timers
          if (silenceTimeoutRef.current) {
            clearTimeout(silenceTimeoutRef.current);
            silenceTimeoutRef.current = null;
          }
        } else if (event.error === 'audio-capture') {
          console.error('Audio capture error - microphone might be in use');
        } else if (event.error === 'network') {
          console.error('Network error - will try to restart');
        } else {
          console.log('Recognition error, will attempt restart:', event.error);
        }
      };
      
      recognitionInstance.onend = () => {
        const now = Date.now();
        const sessionDuration = now - (sessionStartTimeRef.current || now);
        const stillInMinimumPeriod = sessionDuration < minRecordingTimeRef.current;
        
        console.log(`Recognition ended. Manual stop: ${manualStopRef.current}, Should listen: ${isListeningRef.current}, Session: ${Math.round(sessionDuration/1000)}s, In min period: ${stillInMinimumPeriod}`);
        
        // Clear any existing restart timeout
        if (restartTimeoutRef.current) {
          clearTimeout(restartTimeoutRef.current);
          restartTimeoutRef.current = null;
        }
        
        // During minimum period: ALWAYS restart immediately, no questions asked
        if (!manualStopRef.current && isListeningRef.current && stillInMinimumPeriod) {
          console.log('🔄 FORCE RESTART: Still in minimum period, restarting immediately');
          restartTimeoutRef.current = setTimeout(() => {
            if (!manualStopRef.current && isListeningRef.current) {
              try {
                console.log('💪 Aggressive restart - forcing continuation');
                recognitionInstance.start();
              } catch (e) {
                console.error('❌ Primary restart failed:', e.message);
                // Immediate retry with different approach
                setTimeout(() => {
                  if (!manualStopRef.current && isListeningRef.current) {
                    try {
                      console.log('🔄 Secondary restart attempt');
                      recognitionInstance.start();
                    } catch (e2) {
                      console.error('❌ Secondary restart failed:', e2.message);
                      // One more try
                      setTimeout(() => {
                        if (!manualStopRef.current && isListeningRef.current) {
                          try {
                            recognitionInstance.start();
                          } catch (e3) {
                            console.error('❌ All restart attempts failed, giving up');
                          }
                        }
                      }, 50); // Reduced from 500ms to 50ms
                    }
                  }
                }, 10); // Reduced from 100ms to 10ms
              }
            }
          }, 1); // Ultra-fast restart - 1ms
        }
        // After minimum period: use normal restart logic  
        else if (!manualStopRef.current && isListeningRef.current) {
          console.log('Normal restart after minimum period');
          restartTimeoutRef.current = setTimeout(() => {
            if (!manualStopRef.current && isListeningRef.current && document.visibilityState === 'visible') {
              try {
                recognitionInstance.start();
              } catch (e) {
                console.log('Normal restart failed:', e);
                setIsListening(false);
                setIsProcessing(false);
                setTranscript('');
                isListeningRef.current = false;
                manualStopRef.current = true;
              }
            }
          }, 10); // Reduced for normal restart
        } else {
          console.log('Stopping recognition session');
          setIsListening(false);
          setIsProcessing(false);
          setTranscript('');
          isListeningRef.current = false;
        }
      };
      
      setRecognition(recognitionInstance);
      setSpeechSupported(true);
    } else {
      console.log('Speech recognition or microphone not supported in this browser');
      setSpeechSupported(false);
      if (!('mediaDevices' in navigator)) {
        console.log('Navigator.mediaDevices not supported');
      }
      if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        console.log('Speech recognition not supported');
      }
    }
    
    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, [language, onTranscript]);

  // Handle visibility changes to prevent issues when tab is not active
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden && isListeningRef.current && recognition) {
        console.log('Tab became hidden, pausing recognition');
        try {
          recognition.stop();
        } catch (e) {
          console.log('Error stopping recognition on visibility change:', e);
        }
      } else if (!document.hidden && isListeningRef.current && !manualStopRef.current) {
        console.log('Tab became visible, resuming recognition');
        setTimeout(() => {
          if (isListeningRef.current && !manualStopRef.current && recognition) {
            try {
              recognition.start();
            } catch (e) {
              console.log('Error restarting recognition on visibility change:', e);
            }
          }
        }, 500);
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [recognition]);

  const startListening = useCallback(() => {
    if (!recognition || !speechSupported || isDisabled) return;
    
    console.log('Starting voice recognition...');
    
    try {
      manualStopRef.current = false;
      isListeningRef.current = true;
      setIsProcessing(true);
      setTranscript('');
      
      // Check cached microphone permission or request once
      const startRecognition = () => {
        console.log('🎤 Starting recognition with cached permission');
        recognition.start();
      };
      
      if (microphonePermissionRef.current === 'granted') {
        // Permission already granted, start immediately
        startRecognition();
      } else if (microphonePermissionRef.current === 'denied') {
        // Permission was denied before
        alert('Microphone access is required. Please enable it in browser settings.');
        setIsProcessing(false);
        setIsListening(false);
        isListeningRef.current = false;
        manualStopRef.current = true;
      } else {
        // First time - request permission and cache result
        console.log('🎤 Requesting microphone permission (first time)');
        navigator.mediaDevices.getUserMedia({ audio: true })
          .then(() => {
            console.log('✅ Microphone permission granted and cached');
            microphonePermissionRef.current = 'granted';
            startRecognition();
          })
          .catch((error) => {
            console.error('❌ Microphone permission denied:', error);
            microphonePermissionRef.current = 'denied';
            alert('Please allow microphone access to use voice input.');
            setIsProcessing(false);
            setIsListening(false);
            isListeningRef.current = false;
            manualStopRef.current = true;
          });
      }
    } catch (error) {
      console.error('Error starting speech recognition:', error);
      setIsProcessing(false);
      setIsListening(false);
      isListeningRef.current = false;
      manualStopRef.current = true;
    }
  }, [recognition, speechSupported, isDisabled]);

  const stopListening = useCallback(() => {
    console.log('Manually stopping recognition');
    
    // Clear all timers
    if (restartTimeoutRef.current) {
      clearTimeout(restartTimeoutRef.current);
      restartTimeoutRef.current = null;
    }
    
    if (silenceTimeoutRef.current) {
      clearTimeout(silenceTimeoutRef.current);
      silenceTimeoutRef.current = null;
    }
    
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = null;
    }
    
    if (minimumTimerRef.current) {
      clearTimeout(minimumTimerRef.current);
      minimumTimerRef.current = null;
    }
    
    // Set flags to prevent restart
    manualStopRef.current = true;
    isListeningRef.current = false;
    
    // Reset all refs and state
    sessionStartTimeRef.current = null;
    lastSpeechTimeRef.current = null;
    setRecordingTimer(0);
    
    // Update UI immediately
    setIsListening(false);
    setIsProcessing(false);
    setTranscript('');
    
    // Stop the recognition
    if (recognition) {
      try {
        recognition.stop();
      } catch (error) {
        console.log('Error stopping recognition:', error);
      }
    }
  }, [recognition]);

  const toggleListening = () => {
    console.log('Toggle listening, current state:', isListening);
    if (isListening || isProcessing) {
      stopListening();
    } else {
      startListening();
    }
  };

  // Expose methods via ref for programmatic control
  useImperativeHandle(ref, () => ({
    startRecording: startListening,
    stopRecording: stopListening,
    isRecording: () => isListening || isProcessing,
    toggleRecording: toggleListening
  }), [startListening, stopListening, isListening, isProcessing, toggleListening]);

  // Cleanup on unmount or when recognition changes
  useEffect(() => {
    return () => {
      console.log('Cleaning up VoiceInput component');
      
      // Clear all timers
      if (restartTimeoutRef.current) {
        clearTimeout(restartTimeoutRef.current);
        restartTimeoutRef.current = null;
      }
      
      if (silenceTimeoutRef.current) {
        clearTimeout(silenceTimeoutRef.current);
        silenceTimeoutRef.current = null;
      }
      
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
        timerIntervalRef.current = null;
      }
      
      if (minimumTimerRef.current) {
        clearTimeout(minimumTimerRef.current);
        minimumTimerRef.current = null;
      }
      
      // Set flags to prevent any further restarts
      manualStopRef.current = true;
      isListeningRef.current = false;
      
      // Reset timing refs
      sessionStartTimeRef.current = null;
      lastSpeechTimeRef.current = null;
      
      if (recognition) {
        try {
          recognition.stop();
        } catch (error) {
          console.log('Error during cleanup:', error);
        }
      }
    };
  }, [recognition]);

  // Separate effect for silence monitoring after minimum recording period
  useEffect(() => {
    if (!isListening) return;

    const silenceMonitorInterval = setInterval(() => {
      if (!isListeningRef.current || manualStopRef.current) return;
      
      const now = Date.now();
      const sessionDuration = now - (sessionStartTimeRef.current || now);
      const timeSinceLastSpeech = now - (lastSpeechTimeRef.current || now);
      
      // Only auto-stop if we've been recording for at least 2 minutes AND 5+ seconds of silence
      if (sessionDuration >= minRecordingTimeRef.current && timeSinceLastSpeech >= silenceDelayRef.current) {
        console.log(`Auto-stopping due to silence: session=${Math.round(sessionDuration/1000)}s, silence=${Math.round(timeSinceLastSpeech/1000)}s`);
        stopListening();
      }
    }, 1000); // Check every second

    return () => {
      clearInterval(silenceMonitorInterval);
    };
  }, [isListening, stopListening]);

  // Proactive restart monitoring - checks every 100ms if recognition is still active
  useEffect(() => {
    if (!isListening || !recognition) return;

    const proactiveMonitor = setInterval(() => {
      if (!isListeningRef.current || manualStopRef.current) return;

      // Check if recognition might have stopped unexpectedly
      // We use a combination of timing and state checks
      const now = Date.now();
      const timeSinceStart = now - (sessionStartTimeRef.current || now);
      
      // If we've been "listening" for more than 2 seconds without any events,
      // the recognition might have died silently
      if (timeSinceStart > 2000) {
        try {
          // Attempt to restart proactively
          console.log('🔄 Proactive restart - ensuring continuous recording');
          recognition.start();
        } catch (e) {
          // If start() throws "already started", that's actually good - recognition is active
          if (e.message && e.message.includes('already started')) {
            console.log('✅ Recognition confirmed active');
          } else {
            console.log('⚠️ Proactive restart failed:', e.message);
          }
        }
      }
    }, 100); // Check every 100ms for maximum responsiveness

    return () => {
      clearInterval(proactiveMonitor);
    };
  }, [isListening, recognition]);

  // Handle tab visibility changes - immediately restart when tab becomes active
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (!document.hidden && isListeningRef.current && !manualStopRef.current && recognition) {
        console.log('🔄 Tab became active - ensuring recognition is running');
        setTimeout(() => {
          try {
            recognition.start();
          } catch (e) {
            if (!e.message?.includes('already started')) {
              console.log('⚠️ Visibility restart failed:', e.message);
            }
          }
        }, 1); // Immediate restart
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [recognition]);

  if (!speechSupported) {
    return null; // Don't render if speech recognition is not supported
  }

  return (
    <div className={`voice-input-container ${className}`}>
      <button
        type="button"
        onClick={toggleListening}
        disabled={isDisabled || isProcessing}
        className={`voice-input-button p-3 rounded-full transition-all duration-300 text-white relative overflow-hidden
          ${isListening 
            ? 'bg-red-500 hover:bg-red-600 shadow-lg' 
            : isProcessing
            ? 'bg-yellow-500 hover:bg-yellow-600' 
            : 'bg-blue-500 hover:bg-blue-600 hover:shadow-lg'
          }
          ${isProcessing ? 'opacity-75 cursor-wait' : 'hover:scale-105'}
        `}
        title={
          isProcessing
            ? 'Requesting microphone access...'
            : isListening 
            ? 'Recording continuously... (min 2 minutes, auto-stop after 5 seconds of silence)' 
            : 'Start intelligent voice recording'
        }
      >
        {isProcessing ? (
          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
        ) : isListening ? (
          <MicOff className="w-5 h-5" />
        ) : (
          <Mic className="w-5 h-5" />
        )}
        
        {/* Visual feedback ring */}
        {isListening && (
          <div className="absolute inset-0 border-2 border-white opacity-50 rounded-full animate-ping" />
        )}
      </button>
      
      {/* Real-time transcript display */}
      {transcript && isListening && (
        <div className="voice-transcript absolute bottom-full mb-2 left-0 right-0 z-10">
          <div className="bg-black bg-opacity-90 text-white px-3 py-2 rounded-lg text-sm shadow-lg">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
              <Volume2 className="w-4 h-4 text-blue-400" />
              <span className="italic">"{transcript}"</span>
            </div>
          </div>
        </div>
      )}
      
      {/* Recording status when no speech detected */}
      {isListening && !transcript && (
        <div className="voice-transcript absolute bottom-full mb-2 left-0 right-0 z-10">
          <div className="bg-red-600 bg-opacity-90 text-white px-3 py-2 rounded-lg text-sm shadow-lg">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
              <Mic className="w-4 h-4 text-white" />
              <div className="flex flex-col">
                <span className="text-sm font-medium">
                  🎙️ Force Recording Active
                </span>
                <div className="text-xs opacity-75 flex items-center space-x-2">
                  <span>⏱️ {Math.floor(recordingTimer / 60)}:{(recordingTimer % 60).toString().padStart(2, '0')}</span>
                  <span>•</span>
                  <span>{recordingTimer >= 120 ? 'Auto-stop after 5s silence' : `Forced: ${120 - recordingTimer}s left`}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Status indicator */}
      {isListening && (
        <div className="voice-status absolute -top-2 -right-2">
          <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center animate-pulse">
            <div className="w-2 h-2 bg-white rounded-full" />
          </div>
        </div>
      )}
    </div>
  );
});

VoiceInput.displayName = 'VoiceInput';

export default VoiceInput;