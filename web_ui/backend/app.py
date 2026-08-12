"""
Flask API Backend for ConvoAI Web UI
Provides REST endpoints for the conversation interface.
"""

import sys
import os
# Add the parent directory (ConvoAI root) to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import uuid

# Import ConvoAI components
from question_database import QuestionDatabase
from response_analyzer import ResponseAnalyzer
from conversation_engine import ConversationEngine
from config import Config

# Try to import OpenAI integration
try:
    from openai_integration import OpenAIAnalyzer
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAIAnalyzer = None

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React frontend

# Store active sessions in memory (in production, use Redis or database)
active_sessions = {}

class ConvoAISession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.question_db = QuestionDatabase()
        self.analyzer = ResponseAnalyzer()
        self.conversation_engine = ConversationEngine(self.question_db, self.analyzer)
        self.session_data = {
            'session_id': session_id,
            'start_time': datetime.now().isoformat(),
            'responses': [],
            'analysis_results': [],
            'current_question': None,
            'conversation_complete': False
        }
    
    def get_next_question(self):
        """Get the next question in the conversation."""
        question = self.conversation_engine.get_next_question()
        if question:
            self.session_data['current_question'] = question
            return question
        else:
            self.session_data['conversation_complete'] = True
            return None
    
    def process_response(self, response_text):
        """Process user response and return analysis."""
        if not self.session_data['current_question']:
            return {'error': 'No active question'}
        
        question = self.session_data['current_question']
        
        # Store response
        response_data = {
            'question_id': question['id'],
            'question_text': question['text'],
            'response': response_text,
            'timestamp': datetime.now().isoformat()
        }
        self.session_data['responses'].append(response_data)
        
        # Analyze response
        analysis = self.analyzer.analyze_response(question, response_text)
        analysis['timestamp'] = datetime.now().isoformat()
        self.session_data['analysis_results'].append(analysis)
        
        # Update conversation context
        self.conversation_engine.update_context(analysis)
        
        return analysis
    
    def get_session_summary(self):
        """Get current session summary."""
        if not self.session_data['analysis_results']:
            return {'error': 'No responses to analyze yet'}
        
        return self.analyzer.generate_summary(self.session_data['analysis_results'])
    
    def get_final_analysis(self):
        """Get comprehensive final analysis."""
        if not self.session_data['analysis_results']:
            return {'error': 'No responses recorded'}
        
        return self.analyzer.generate_final_analysis(
            self.session_data['responses'],
            self.session_data['analysis_results']
        )

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'ConvoAI API is running'})

@app.route('/api/session/start', methods=['POST'])
def start_session():
    """Start a new conversation session."""
    session_id = str(uuid.uuid4())
    session = ConvoAISession(session_id)
    
    # Get first question
    first_question = session.get_next_question()
    
    if first_question:
        active_sessions[session_id] = session
        return jsonify({
            'session_id': session_id,
            'question': first_question,
            'message': 'Session started successfully'
        })
    else:
        return jsonify({'error': 'Could not start session'}), 500

@app.route('/api/session/<session_id>/respond', methods=['POST'])
def submit_response(session_id):
    """Submit a response to the current question."""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    data = request.get_json()
    response_text = data.get('response', '').strip()
    
    if not response_text:
        return jsonify({'error': 'Response cannot be empty'}), 400
    
    session = active_sessions[session_id]
    
    # Process the response
    analysis = session.process_response(response_text)
    
    if 'error' in analysis:
        return jsonify(analysis), 400
    
    # Get next question
    next_question = session.get_next_question()
    
    response_data = {
        'analysis': analysis,
        'next_question': next_question,
        'conversation_complete': session.session_data['conversation_complete']
    }
    
    return jsonify(response_data)

@app.route('/api/session/<session_id>/question/next', methods=['GET'])
def get_next_question(session_id):
    """Get the next question without submitting a response."""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = active_sessions[session_id]
    next_question = session.get_next_question()
    
    if next_question:
        return jsonify({'question': next_question})
    else:
        return jsonify({'message': 'No more questions', 'conversation_complete': True})

@app.route('/api/session/<session_id>/summary', methods=['GET'])
def get_session_summary(session_id):
    """Get current session analysis summary."""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = active_sessions[session_id]
    summary = session.get_session_summary()
    
    return jsonify(summary)

@app.route('/api/session/<session_id>/analysis/final', methods=['GET'])
def get_final_analysis(session_id):
    """Get comprehensive final analysis."""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = active_sessions[session_id]
    final_analysis = session.get_final_analysis()
    
    return jsonify(final_analysis)

@app.route('/api/session/<session_id>/status', methods=['GET'])
def get_session_status(session_id):
    """Get session status and statistics."""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = active_sessions[session_id]
    stats = session.conversation_engine.get_conversation_stats()
    
    return jsonify({
        'session_id': session_id,
        'start_time': session.session_data['start_time'],
        'responses_count': len(session.session_data['responses']),
        'current_question': session.session_data['current_question'],
        'conversation_complete': session.session_data['conversation_complete'],
        'conversation_stats': stats
    })

@app.route('/api/session/<session_id>/skip', methods=['POST'])
def skip_question(session_id):
    """Skip the current question."""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = active_sessions[session_id]
    success = session.conversation_engine.skip_current_question()
    
    if success:
        next_question = session.get_next_question()
        return jsonify({
            'message': 'Question skipped',
            'next_question': next_question,
            'conversation_complete': session.session_data['conversation_complete']
        })
    else:
        return jsonify({'error': 'Could not skip question'}), 400

@app.route('/api/session/<session_id>/end', methods=['POST'])
def end_session(session_id):
    """End the conversation session."""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = active_sessions[session_id]
    
    # Get final analysis if there are responses
    final_analysis = None
    if session.session_data['analysis_results']:
        final_analysis = session.get_final_analysis()
    
    # Save session data to file
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"../session_web_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'session_data': session.session_data,
                'final_analysis': final_analysis
            }, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving session: {e}")
    
    # Remove session from active sessions
    del active_sessions[session_id]
    
    return jsonify({
        'message': 'Session ended successfully',
        'final_analysis': final_analysis,
        'session_saved': True
    })

@app.route('/api/questions/categories', methods=['GET'])
def get_question_categories():
    """Get all available question categories."""
    db = QuestionDatabase()
    categories = db.get_all_categories()
    
    category_info = {}
    for category in categories:
        questions = db.get_questions_by_category(category)
        category_info[category] = {
            'name': category.replace('_', ' ').title(),
            'count': len(questions),
            'description': get_category_description(category)
        }
    
    return jsonify(category_info)

def get_category_description(category):
    """Get description for question category."""
    descriptions = {
        'personal': 'Questions about your goals, motivations, and personal aspirations',
        'problem_solving': 'Questions about how you approach decisions and solve problems',
        'values': 'Questions about your core beliefs and what matters most to you',
        'learning': 'Questions about how you prefer to learn and acquire new skills',
        'reflection': 'Questions that encourage self-reflection and personal growth',
        'future': 'Questions about your future plans and long-term vision'
    }
    return descriptions.get(category, 'General conversation topics')

if __name__ == '__main__':
    print("🚀 Starting ConvoAI API Backend...")
    print("📡 API will be available at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("📚 Available endpoints:")
    print("  POST /api/session/start - Start new conversation")
    print("  POST /api/session/{id}/respond - Submit response")
    print("  GET  /api/session/{id}/summary - Get analysis summary")
    print("  GET  /api/session/{id}/analysis/final - Get final analysis")
    print("  POST /api/session/{id}/end - End conversation")
    print()
    
    app.run(debug=True, port=5000, host='0.0.0.0')