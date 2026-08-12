"""
UI Handler Module
Handles user interface interactions and display formatting.
"""

from typing import Dict, List, Any, Optional
import textwrap
from datetime import datetime

class UIHandler:
    def __init__(self):
        """Initialize the UI handler."""
        self.width = 80  # Console width for text wrapping
        self.separator = "=" * self.width
        self.thin_separator = "-" * self.width
        
        # Color codes for better display (if terminal supports it)
        self.colors = {
            'blue': '\033[94m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'underline': '\033[4m',
            'end': '\033[0m'
        }
    
    def _colorize(self, text: str, color: str = 'white') -> str:
        """Add color to text if supported."""
        return f"{self.colors.get(color, '')}{text}{self.colors['end']}"
    
    def _wrap_text(self, text: str, indent: int = 0) -> str:
        """Wrap text to fit console width."""
        wrapper = textwrap.TextWrapper(
            width=self.width - indent,
            initial_indent=' ' * indent,
            subsequent_indent=' ' * indent
        )
        return wrapper.fill(text)
    
    def display_welcome_message(self):
        """Display welcome message and instructions."""
        welcome_text = f"""
{self.separator}
{self._colorize('🤖 Welcome to ConvoAI! 🤖', 'cyan')}
{self.separator}

{self._colorize('About ConvoAI:', 'blue')}
This conversational AI will ask you thoughtful questions and analyze your responses
to provide insights about your thinking patterns, values, and perspectives.

{self._colorize('How it works:', 'green')}
• I'll ask you a series of questions from different categories
• You can answer as briefly or detailed as you'd like  
• I'll analyze your responses for sentiment, themes, and patterns
• At the end, you'll get personalized insights and recommendations

{self._colorize('Commands you can use anytime:', 'yellow')}
• Type 'help' - Show help information
• Type 'summary' - Get current analysis summary
• Type 'quit', 'exit', or 'stop' - End conversation

{self.thin_separator}
Let's begin! Remember, there are no right or wrong answers - just be honest
and thoughtful in your responses.
{self.thin_separator}
        """
        print(welcome_text)
    
    def display_question(self, question: Dict[str, Any]):
        """Display a question to the user."""
        print(f"\n{self._colorize('Question:', 'purple')}")
        
        # Show question category
        category = question.get('category', 'General').title()
        print(f"{self._colorize(f'Category: {category}', 'cyan')}")
        
        # Show question text
        question_text = self._wrap_text(question['text'], 0)
        print(f"\n{self._colorize(question_text, 'white')}")
        
        # Handle different question types
        question_type = question.get('type', 'open_ended')
        
        if question_type == 'multiple_choice':
            options = question.get('options', [])
            if options:
                print(f"\n{self._colorize('Options:', 'yellow')}")
                for i, option in enumerate(options, 1):
                    print(f"  {i}. {option}")
                print(f"\n{self._colorize('You can respond with the number, or describe your choice:', 'green')}")
        
        elif question_type == 'ranking':
            options = question.get('options', [])
            if options:
                print(f"\n{self._colorize('Please rank these options (or discuss their importance):', 'yellow')}")
                for i, option in enumerate(options, 1):
                    print(f"  {i}. {option}")
        
        print(f"\n{self._colorize('Your response:', 'green')}")
    
    def get_user_input(self) -> str:
        """Get input from user."""
        try:
            response = input("> ").strip()
            return response
        except (EOFError, KeyboardInterrupt):
            return "quit"
    
    def display_analysis_feedback(self, analysis: Dict[str, Any]):
        """Display immediate feedback after analyzing a response."""
        print(f"\n{self._colorize('💡 Quick Analysis:', 'cyan')}")
        
        # Show sentiment
        sentiment = analysis.get('sentiment', {})
        sentiment_text = sentiment.get('overall', 'neutral').title()
        confidence = sentiment.get('confidence', 0)
        
        if confidence > 0.7:
            print(f"  Sentiment: {self._colorize(sentiment_text, 'green')} (confident)")
        else:
            print(f"  Sentiment: {self._colorize(sentiment_text, 'yellow')}")
        
        # Show engagement level
        engagement = analysis.get('engagement_level', {})
        engagement_level = engagement.get('level', 'medium').title()
        word_count = engagement.get('word_count', 0)
        
        print(f"  Engagement: {self._colorize(engagement_level, 'blue')} ({word_count} words)")
        
        # Show key themes if any
        themes = analysis.get('key_themes', [])
        if themes:
            themes_text = ', '.join(themes[:3])
            print(f"  Key themes: {self._colorize(themes_text, 'purple')}")
        
        # Show emotions if detected
        emotions = analysis.get('emotions', [])
        if emotions:
            emotion_names = [e['emotion'] for e in emotions[:2]]
            emotions_text = ', '.join(emotion_names)
            print(f"  Emotions detected: {self._colorize(emotions_text, 'yellow')}")
        
        print()  # Add spacing
    
    def display_analysis_summary(self, summary: Dict[str, Any]):
        """Display analysis summary."""
        print(f"\n{self.separator}")
        print(f"{self._colorize('📊 Analysis Summary', 'cyan')}")
        print(f"{self.separator}")
        
        # Basic stats
        total_responses = summary.get('total_responses', 0)
        avg_word_count = summary.get('average_word_count', 0)
        print(f"Total responses analyzed: {self._colorize(str(total_responses), 'green')}")
        print(f"Average response length: {self._colorize(f'{avg_word_count:.1f} words', 'blue')}")
        
        # Sentiment distribution
        sentiment_dist = summary.get('sentiment_distribution', {})
        print(f"\n{self._colorize('Sentiment Distribution:', 'yellow')}")
        for sentiment, count in sentiment_dist.items():
            percentage = (count / total_responses * 100) if total_responses > 0 else 0
            print(f"  {sentiment.title()}: {count} ({percentage:.1f}%)")
        
        # Engagement distribution
        engagement_dist = summary.get('engagement_distribution', {})
        print(f"\n{self._colorize('Engagement Distribution:', 'purple')}")
        for level, count in engagement_dist.items():
            percentage = (count / total_responses * 100) if total_responses > 0 else 0
            print(f"  {level.title()}: {count} ({percentage:.1f}%)")
        
        # Top themes
        top_themes = summary.get('top_themes', [])
        if top_themes:
            print(f"\n{self._colorize('Top Themes:', 'cyan')}")
            for theme in top_themes:
                print(f"  • {theme}")
        
        print(f"\n{self.thin_separator}")
    
    def display_final_analysis(self, final_analysis: Dict[str, Any]):
        """Display comprehensive final analysis."""
        print(f"\n{self.separator}")
        print(f"{self._colorize('🎯 Final Analysis Report', 'bold')}")
        print(f"{self.separator}")
        
        # Session summary
        session_summary = final_analysis.get('session_summary', {})
        self._display_session_summary(session_summary)
        
        # Key insights
        insights = final_analysis.get('key_insights', [])
        if insights:
            print(f"\n{self._colorize('🔍 Key Insights:', 'cyan')}")
            for i, insight in enumerate(insights, 1):
                wrapped_insight = self._wrap_text(insight, 4)
                print(f"  {i}. {wrapped_insight}")
        
        # Patterns identified
        patterns = final_analysis.get('patterns_identified', {})
        if patterns:
            self._display_patterns(patterns)
        
        # Recommendations
        recommendations = final_analysis.get('recommendations', [])
        if recommendations:
            print(f"\n{self._colorize('💡 Recommendations:', 'green')}")
            for i, rec in enumerate(recommendations, 1):
                wrapped_rec = self._wrap_text(rec, 4)
                print(f"  {i}. {wrapped_rec}")
        
        # Footer
        timestamp = final_analysis.get('timestamp', datetime.now().isoformat())
        print(f"\n{self.thin_separator}")
        print(f"Analysis completed at: {timestamp}")
        print(f"Thank you for using ConvoAI! 🤖")
        print(f"{self.separator}")
    
    def _display_session_summary(self, summary: Dict[str, Any]):
        """Display session summary section."""
        print(f"\n{self._colorize('Session Overview:', 'blue')}")
        
        total_responses = summary.get('total_responses', 0)
        avg_complexity = summary.get('average_complexity', 0)
        dominant_sentiment = summary.get('dominant_sentiment', 'neutral')
        dominant_engagement = summary.get('dominant_engagement', 'medium')
        
        print(f"  Responses given: {total_responses}")
        print(f"  Average complexity: {avg_complexity:.2f}/1.0")
        print(f"  Dominant sentiment: {dominant_sentiment.title()}")
        print(f"  Typical engagement: {dominant_engagement.title()}")
    
    def _display_patterns(self, patterns: Dict[str, Any]):
        """Display identified patterns."""
        print(f"\n{self._colorize('📈 Patterns Identified:', 'purple')}")
        
        # Sentiment trend
        sentiment_trend = patterns.get('sentiment_trend', [])
        if sentiment_trend:
            print(f"  Sentiment trend: {' → '.join(sentiment_trend[-3:])}")
        
        # Common emotions
        common_emotions = patterns.get('common_emotions', [])
        if common_emotions:
            print(f"  Common emotions: {', '.join(common_emotions)}")
        
        # Recurring themes
        recurring_themes = patterns.get('recurring_themes', [])
        if recurring_themes:
            print(f"  Recurring themes: {', '.join(recurring_themes)}")
    
    def ask_continue(self) -> bool:
        """Ask user if they want to continue."""
        print(f"\n{self._colorize('Would you like to continue? (y/n):', 'yellow')}")
        response = input("> ").strip().lower()
        return response in ['y', 'yes', 'continue', '']
    
    def display_help(self):
        """Display help information."""
        help_text = f"""
{self.thin_separator}
{self._colorize('ConvoAI Help', 'cyan')}
{self.thin_separator}

{self._colorize('Available Commands:', 'yellow')}
• help - Show this help message
• summary - Display current analysis summary  
• quit/exit/stop - End the conversation

{self._colorize('Question Types:', 'green')}
• Open-ended: Answer in your own words
• Multiple choice: Select an option or describe your choice
• Ranking: Rank options or discuss their importance

{self._colorize('Tips for Better Analysis:', 'blue')}
• Be honest and authentic in your responses
• Provide details and examples when possible
• Don't worry about "right" answers - there aren't any!
• The AI learns from your response patterns over time

{self._colorize('Privacy:', 'purple')}
• Your responses are analyzed locally
• Session data is saved to a local file
• No data is sent to external servers

{self.thin_separator}
        """
        print(help_text)
    
    def display_message(self, message: str, color: str = 'white'):
        """Display a general message."""
        colored_message = self._colorize(message, color)
        wrapped_message = self._wrap_text(colored_message)
        print(f"\n{wrapped_message}\n")
    
    def display_error(self, error_message: str):
        """Display an error message."""
        self.display_message(f"❌ Error: {error_message}", 'red')
    
    def display_success(self, success_message: str):
        """Display a success message."""
        self.display_message(f"✅ {success_message}", 'green')
    
    def get_yes_no_input(self, prompt: str) -> bool:
        """Get yes/no input from user."""
        while True:
            print(f"{self._colorize(prompt + ' (y/n):', 'yellow')}")
            response = input("> ").strip().lower()
            
            if response in ['y', 'yes', 'true', '1']:
                return True
            elif response in ['n', 'no', 'false', '0']:
                return False
            else:
                self.display_message("Please enter 'y' for yes or 'n' for no.", 'yellow')
    
    def display_loading(self, message: str = "Processing..."):
        """Display loading message."""
        print(f"\n{self._colorize(f'⏳ {message}', 'yellow')}")
    
    def clear_loading(self):
        """Clear loading message (simple implementation)."""
        print()  # Just add some space