"""
Configuration file for ConvoAI application.
Adjust these settings to customize the AI behavior.
"""

# Conversation Settings
CONVERSATION_CONFIG = {
    'max_questions_per_session': 15,
    'min_response_length': 3,  # Minimum words for a valid response
    'adaptive_mode': True,  # Whether to adapt based on user responses
    'save_sessions': True,  # Whether to save session data
    'show_progress': True,  # Show question progress
}

# Analysis Settings  
ANALYSIS_CONFIG = {
    'sentiment_threshold': 0.6,  # Confidence threshold for sentiment detection
    'emotion_detection': True,  # Enable emotion detection
    'theme_extraction': True,  # Enable theme extraction
    'engagement_tracking': True,  # Track engagement levels
    'complexity_analysis': True,  # Analyze response complexity
}

# UI Settings
UI_CONFIG = {
    'use_colors': True,  # Enable colored output (if supported)
    'console_width': 80,  # Width for text wrapping
    'show_analysis_feedback': True,  # Show immediate feedback after responses
    'verbose_mode': False,  # Show detailed analysis information
    'animation_speed': 0.5,  # Seconds for typing animations (if implemented)
}

# Question Database Settings
QUESTION_CONFIG = {
    'shuffle_questions': True,  # Randomize question order within categories
    'enable_follow_ups': True,  # Ask follow-up questions
    'max_follow_ups': 2,  # Maximum follow-up questions per main question
    'category_balance': True,  # Try to balance questions across categories
}

# File Settings
FILE_CONFIG = {
    'session_filename_format': 'session_%Y%m%d_%H%M%S.json',
    'backup_sessions': True,  # Keep backup of previous sessions
    'auto_save_frequency': 5,  # Auto-save after N responses
    'max_session_files': 50,  # Maximum session files to keep
}

# Advanced Analysis Settings
ADVANCED_ANALYSIS = {
    'pattern_recognition': True,  # Detect patterns across responses
    'personality_insights': True,  # Generate personality-related insights
    'goal_tracking': True,  # Track and analyze mentioned goals
    'value_analysis': True,  # Analyze expressed values and beliefs
    'learning_style_detection': True,  # Detect learning preferences
}

# Recommendation Engine Settings
RECOMMENDATION_CONFIG = {
    'enable_recommendations': True,  # Generate personalized recommendations
    'recommendation_categories': [
        'personal_development',
        'goal_setting', 
        'communication',
        'learning_strategies',
        'stress_management'
    ],
    'max_recommendations': 5,  # Maximum recommendations to show
}

# Debug and Development Settings
DEBUG_CONFIG = {
    'debug_mode': False,  # Enable debug output
    'log_analysis_steps': False,  # Log detailed analysis steps
    'test_mode': False,  # Enable test mode with sample responses
    'performance_monitoring': False,  # Monitor performance metrics
}

import os

# OpenAI Integration Settings
OPENAI_CONFIG = {
    'api_key': os.getenv('OPENAI_API_KEY', ''),  # Set via OPENAI_API_KEY environment variable
    'model': 'gpt-4',  # Options: 'gpt-4', 'gpt-3.5-turbo'
    'max_tokens': 1500,
    'temperature': 0.3,  # Lower = more consistent, Higher = more creative
    'enable_advanced_analysis': True,  # Use GPT for response analysis
    'enable_dynamic_questions': True,  # Generate follow-up questions
    'enable_conversation_summary': True,  # Generate session summaries
    'cost_limit_per_session': 1.00,  # Maximum cost in USD per session
}

class Config:
    """Main configuration class with helper methods"""
    
    @staticmethod
    def set_openai_key(api_key: str):
        """Set OpenAI API key"""
        OPENAI_CONFIG['api_key'] = api_key
    
    @staticmethod
    def get_openai_key() -> str:
        """Get OpenAI API key from config or environment"""
        import os
        return OPENAI_CONFIG['api_key'] or os.getenv('OPENAI_API_KEY')
    
    @staticmethod
    def has_openai_key() -> bool:
        """Check if OpenAI API key is available"""
        key = Config.get_openai_key()
        return key is not None and len(key.strip()) > 0
    
    @staticmethod
    def get_config_summary():
        """Get a summary of current configuration"""
        return {
            'conversation': CONVERSATION_CONFIG,
            'analysis': ANALYSIS_CONFIG,
            'openai_enabled': Config.has_openai_key(),
            'ui': UI_CONFIG
        }