import React, { useState, useEffect } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import ConversationScreen from './components/ConversationScreen';
import AnalysisScreen from './components/AnalysisScreen';
import LoadingScreen from './components/LoadingScreen';
import ErrorScreen from './components/ErrorScreen';
import { apiService } from './services/api';

function App() {
  const [currentScreen, setCurrentScreen] = useState('welcome');
  const [sessionData, setSessionData] = useState({
    sessionId: null,
    currentQuestion: null,
    responses: [],
    analysisResults: [],
    conversationComplete: false
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Check API health on component mount
  useEffect(() => {
    checkAPIHealth();
  }, []);

  const checkAPIHealth = async () => {
    try {
      await apiService.healthCheck();
    } catch (error) {
      setError({
        title: 'API Connection Error',
        message: 'Could not connect to ConvoAI backend. Please make sure the Flask server is running on port 5000.',
        action: 'Retry',
        onAction: checkAPIHealth
      });
    }
  };

  const handleStartConversation = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiService.startSession();
      setSessionData({
        sessionId: response.session_id,
        currentQuestion: response.question,
        responses: [],
        analysisResults: [],
        conversationComplete: false
      });
      setCurrentScreen('conversation');
    } catch (error) {
      setError({
        title: 'Failed to Start Conversation',
        message: 'Could not start a new conversation session. Please try again.',
        action: 'Retry',
        onAction: handleStartConversation
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitResponse = async (responseText) => {
    setLoading(true);
    
    try {
      const response = await apiService.submitResponse(sessionData.sessionId, responseText);
      
      // Update session data
      setSessionData(prev => ({
        ...prev,
        currentQuestion: response.next_question,
        responses: [...prev.responses, {
          question: prev.currentQuestion,
          response: responseText,
          analysis: response.analysis
        }],
        analysisResults: [...prev.analysisResults, response.analysis],
        conversationComplete: response.conversation_complete
      }));

      // If conversation is complete, move to analysis screen
      if (response.conversation_complete) {
        setCurrentScreen('analysis');
      }
    } catch (error) {
      setError({
        title: 'Response Submission Failed',
        message: 'Could not submit your response. Please try again.',
        action: 'Retry',
        onAction: () => handleSubmitResponse(responseText)
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSkipQuestion = async () => {
    setLoading(true);
    
    try {
      const response = await apiService.skipQuestion(sessionData.sessionId);
      setSessionData(prev => ({
        ...prev,
        currentQuestion: response.next_question,
        conversationComplete: response.conversation_complete
      }));

      if (response.conversation_complete) {
        setCurrentScreen('analysis');
      }
    } catch (error) {
      setError({
        title: 'Skip Question Failed',
        message: 'Could not skip the current question. Please try again.',
        action: 'Retry',
        onAction: handleSkipQuestion
      });
    } finally {
      setLoading(false);
    }
  };

  const handleEndConversation = async () => {
    setLoading(true);
    
    try {
      await apiService.endSession(sessionData.sessionId);
      setCurrentScreen('analysis');
    } catch (error) {
      // Even if ending fails, go to analysis screen
      setCurrentScreen('analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleStartNew = () => {
    setSessionData({
      sessionId: null,
      currentQuestion: null,
      responses: [],
      analysisResults: [],
      conversationComplete: false
    });
    setCurrentScreen('welcome');
    setError(null);
  };

  const handleShowSummary = async () => {
    setLoading(true);
    
    try {
      const summary = await apiService.getSessionSummary(sessionData.sessionId);
      // You can add a modal or separate screen to show summary
      alert('Summary feature would open here');
    } catch (error) {
      setError({
        title: 'Summary Failed',
        message: 'Could not retrieve conversation summary.',
        action: 'Close',
        onAction: () => setError(null)
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingScreen />;
  }

  if (error) {
    return <ErrorScreen error={error} onRetry={error.onAction} />;
  }

  switch (currentScreen) {
    case 'welcome':
      return (
        <WelcomeScreen 
          onStartConversation={handleStartConversation}
        />
      );
    
    case 'conversation':
      return (
        <ConversationScreen
          sessionData={sessionData}
          onSubmitResponse={handleSubmitResponse}
          onSkipQuestion={handleSkipQuestion}
          onEndConversation={handleEndConversation}
          onShowSummary={handleShowSummary}
        />
      );
    
    case 'analysis':
      return (
        <AnalysisScreen
          sessionData={sessionData}
          onStartNew={handleStartNew}
        />
      );
    
    default:
      return <WelcomeScreen onStartConversation={handleStartConversation} />;
  }
}

export default App;