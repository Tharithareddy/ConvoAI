#!/usr/bin/env python3
"""
ConvoAI - A Basic Conversational AI Application
This application can ask predefined questions and analyze user responses.
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any
from conversation_engine import ConversationEngine
from question_database import QuestionDatabase
from response_analyzer import ResponseAnalyzer
from ui_handler import UIHandler
from config import OPENAI_CONFIG, Config

# Try to import OpenAI integration
try:
    from openai_integration import OpenAIAnalyzer
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAIAnalyzer = None

class ConvoAI:
    def __init__(self, openai_api_key: str = None):
        """Initialize the ConvoAI application."""
        self.question_db = QuestionDatabase()
        self.analyzer = ResponseAnalyzer()
        self.ui = UIHandler()
        self.conversation_engine = ConversationEngine(self.question_db, self.analyzer)
        
        # Initialize OpenAI if available and key provided
        self.openai_analyzer = None
        if OPENAI_AVAILABLE and (openai_api_key or Config.has_openai_key()):
            try:
                api_key = openai_api_key or Config.get_openai_key()
                self.openai_analyzer = OpenAIAnalyzer(api_key)
                if self.openai_analyzer.enabled:
                    self.ui.success("🤖 OpenAI integration enabled - Enhanced analysis available!")
                else:
                    self.ui.warning("⚠️ OpenAI integration failed - Using basic analysis only")
            except Exception as e:
                self.ui.error(f"❌ Failed to initialize OpenAI: {str(e)}")
        else:
            if not OPENAI_AVAILABLE:
                self.ui.info("💡 Install 'openai' package for enhanced AI analysis")
            elif not Config.has_openai_key():
                self.ui.info("💡 Set OpenAI API key for enhanced analysis features")
        
        self.session_data = {
            'start_time': datetime.now().isoformat(),
            'responses': [],
            'analysis_results': [],
            'openai_enabled': self.openai_analyzer is not None and self.openai_analyzer.enabled
        }
    
    def start_conversation(self):
        """Start the main conversation loop."""
        self.ui.display_welcome_message()
        
        while True:
            # Get next question from conversation engine
            question = self.conversation_engine.get_next_question()
            
            if question is None:
                self.ui.display_message("Thank you for completing the conversation!")
                break
            
            # Display question to user
            self.ui.display_question(question)
            
            # Get user response
            response = self.ui.get_user_input()
            
            # Handle special commands
            if response.lower() in ['quit', 'exit', 'stop']:
                self.ui.display_message("Goodbye!")
                break
            elif response.lower() == 'help':
                self.ui.display_help()
                continue
            elif response.lower() == 'summary':
                self.show_analysis_summary()
                continue
            
            # Process the response
            self.process_response(question, response)
            
            # Ask if user wants to continue
            if not self.ui.ask_continue():
                break
        
        # Show final analysis
        self.show_final_analysis()
    
    def process_response(self, question: Dict[str, Any], response: str):
        """Process user response and analyze it."""
        # Store response
        response_data = {
            'question_id': question['id'],
            'question_text': question['text'],
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        self.session_data['responses'].append(response_data)
        
        # Analyze response
        analysis = self.analyzer.analyze_response(question, response)
        analysis['timestamp'] = datetime.now().isoformat()
        self.session_data['analysis_results'].append(analysis)
        
        # Update conversation engine with analysis
        self.conversation_engine.update_context(analysis)
        
        # Display immediate feedback
        self.ui.display_analysis_feedback(analysis)
    
    def show_analysis_summary(self):
        """Show current analysis summary."""
        if not self.session_data['analysis_results']:
            self.ui.display_message("No responses to analyze yet.")
            return
        
        summary = self.analyzer.generate_summary(self.session_data['analysis_results'])
        self.ui.display_analysis_summary(summary)
    
    def show_final_analysis(self):
        """Show final comprehensive analysis."""
        if not self.session_data['analysis_results']:
            self.ui.display_message("No responses were recorded.")
            return
        
        final_analysis = self.analyzer.generate_final_analysis(
            self.session_data['responses'],
            self.session_data['analysis_results']
        )
        
        self.ui.display_final_analysis(final_analysis)
        
        # Save session data
        self.save_session()
    
    def save_session(self):
        """Save session data to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2, ensure_ascii=False)
            self.ui.display_message(f"Session saved to {filename}")
        except Exception as e:
            self.ui.display_message(f"Error saving session: {e}")

def main():
    """Main entry point."""
    try:
        app = ConvoAI()
        app.start_conversation()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()