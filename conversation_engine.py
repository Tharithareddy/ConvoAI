"""
Conversation Engine Module
Manages the flow of conversation and question selection.
"""

import random
from typing import Dict, List, Any, Optional
from question_database import QuestionDatabase
from response_analyzer import ResponseAnalyzer

class ConversationEngine:
    def __init__(self, question_db: QuestionDatabase, analyzer: ResponseAnalyzer):
        """Initialize the conversation engine."""
        self.question_db = question_db
        self.analyzer = analyzer
        self.conversation_state = {
            'current_question_index': 0,
            'asked_questions': set(),
            'question_sequence': [],
            'context_keywords': [],
            'user_preferences': {},
            'conversation_style': 'adaptive'  # adaptive, sequential, random
        }
        self.initialize_conversation()
    
    def initialize_conversation(self):
        """Initialize the conversation with starting questions."""
        # Get starting questions from different categories
        starting_questions = self.question_db.get_starting_questions()
        self.conversation_state['question_sequence'] = starting_questions.copy()
        
        # Add some follow-up questions to the initial sequence
        for question in starting_questions[:2]:  # Add follow-ups for first 2 questions
            follow_ups = self.question_db.get_follow_up_questions(question['id'])
            self.conversation_state['question_sequence'].extend(follow_ups[:1])  # Add 1 follow-up each
    
    def get_next_question(self) -> Optional[Dict[str, Any]]:
        """Get the next question based on conversation state and context."""
        # Check if we have pre-planned questions
        if (self.conversation_state['current_question_index'] < 
            len(self.conversation_state['question_sequence'])):
            
            question = self.conversation_state['question_sequence'][
                self.conversation_state['current_question_index']
            ]
            
            # Skip if already asked
            if question['id'] not in self.conversation_state['asked_questions']:
                self.conversation_state['current_question_index'] += 1
                self.conversation_state['asked_questions'].add(question['id'])
                return question
            else:
                self.conversation_state['current_question_index'] += 1
                return self.get_next_question()  # Recursive call to get next
        
        # If no pre-planned questions, use adaptive selection
        return self._select_adaptive_question()
    
    def _select_adaptive_question(self) -> Optional[Dict[str, Any]]:
        """Select next question based on conversation context."""
        # Get all available questions not yet asked
        available_questions = [
            q for q in self.question_db.questions 
            if q['id'] not in self.conversation_state['asked_questions']
        ]
        
        if not available_questions:
            return None  # No more questions available
        
        # If we have context keywords, try to find relevant questions
        if self.conversation_state['context_keywords']:
            relevant_questions = self.question_db.search_questions_by_keywords(
                self.conversation_state['context_keywords']
            )
            
            # Filter out already asked questions
            relevant_available = [
                q for q in relevant_questions 
                if q['id'] not in self.conversation_state['asked_questions']
            ]
            
            if relevant_available:
                question = random.choice(relevant_available)
                self.conversation_state['asked_questions'].add(question['id'])
                return question
        
        # Fallback to random selection from available questions
        if available_questions:
            question = random.choice(available_questions)
            self.conversation_state['asked_questions'].add(question['id'])
            return question
        
        return None
    
    def update_context(self, analysis: Dict[str, Any]):
        """Update conversation context based on response analysis."""
        # Add key themes to context keywords
        key_themes = analysis.get('key_themes', [])
        for theme in key_themes:
            if theme not in self.conversation_state['context_keywords']:
                self.conversation_state['context_keywords'].append(theme)
        
        # Keep only the most recent 10 keywords to avoid overflow
        if len(self.conversation_state['context_keywords']) > 10:
            self.conversation_state['context_keywords'] = \
                self.conversation_state['context_keywords'][-10:]
        
        # Update user preferences based on sentiment and engagement
        sentiment = analysis.get('sentiment', {}).get('overall', 'neutral')
        engagement = analysis.get('engagement_level', {}).get('level', 'medium')
        
        # Track user's typical response patterns
        if 'sentiment_pattern' not in self.conversation_state['user_preferences']:
            self.conversation_state['user_preferences']['sentiment_pattern'] = []
        if 'engagement_pattern' not in self.conversation_state['user_preferences']:
            self.conversation_state['user_preferences']['engagement_pattern'] = []
        
        self.conversation_state['user_preferences']['sentiment_pattern'].append(sentiment)
        self.conversation_state['user_preferences']['engagement_pattern'].append(engagement)
        
        # Keep only recent patterns (last 5 responses)
        for pattern_type in ['sentiment_pattern', 'engagement_pattern']:
            pattern = self.conversation_state['user_preferences'][pattern_type]
            if len(pattern) > 5:
                self.conversation_state['user_preferences'][pattern_type] = pattern[-5:]
        
        # Adapt conversation style based on engagement
        recent_engagement = self.conversation_state['user_preferences'].get('engagement_pattern', [])
        if len(recent_engagement) >= 3:
            avg_engagement = self._calculate_engagement_score(recent_engagement[-3:])
            
            if avg_engagement < 1.5:  # Low engagement
                self._adapt_to_low_engagement()
            elif avg_engagement > 2.5:  # High engagement
                self._adapt_to_high_engagement()
    
    def _calculate_engagement_score(self, engagement_levels: List[str]) -> float:
        """Calculate average engagement score."""
        score_map = {'low': 1, 'medium': 2, 'high': 3}
        scores = [score_map.get(level, 2) for level in engagement_levels]
        return sum(scores) / len(scores) if scores else 2.0
    
    def _adapt_to_low_engagement(self):
        """Adapt conversation for users with low engagement."""
        # Prioritize shorter, more direct questions
        # Look for questions that are more engaging or personal
        self.conversation_state['conversation_style'] = 'engaging'
        
        # Add some engaging questions to the sequence
        engaging_categories = ['personal', 'values']
        for category in engaging_categories:
            category_questions = self.question_db.get_questions_by_category(category)
            available_in_category = [
                q for q in category_questions 
                if q['id'] not in self.conversation_state['asked_questions']
            ]
            
            if available_in_category:
                # Add one engaging question from each category
                self.conversation_state['question_sequence'].append(available_in_category[0])
    
    def _adapt_to_high_engagement(self):
        """Adapt conversation for users with high engagement."""
        # Add more follow-up questions and deeper exploration
        self.conversation_state['conversation_style'] = 'deep'
        
        # Add follow-up questions for recent responses
        if self.conversation_state['question_sequence']:
            last_question = self.conversation_state['question_sequence'][-1]
            follow_ups = self.question_db.get_follow_up_questions(last_question['id'])
            
            # Add available follow-ups
            for follow_up in follow_ups:
                if follow_up['id'] not in self.conversation_state['asked_questions']:
                    self.conversation_state['question_sequence'].append(follow_up)
    
    def add_custom_question(self, question_text: str, category: str = 'custom', 
                           question_type: str = 'open_ended') -> bool:
        """Add a custom question to the conversation."""
        try:
            custom_question = {
                'text': question_text,
                'category': category,
                'type': question_type,
                'keywords': question_text.lower().split(),
                'follow_up_questions': []
            }
            
            # Add to database
            success = self.question_db.add_question(custom_question)
            
            if success:
                # Add to current conversation sequence
                self.conversation_state['question_sequence'].append(custom_question)
                return True
            
            return False
        except Exception:
            return False
    
    def skip_current_question(self) -> bool:
        """Skip the current question and move to the next."""
        try:
            # Move to next question in sequence
            if (self.conversation_state['current_question_index'] < 
                len(self.conversation_state['question_sequence'])):
                self.conversation_state['current_question_index'] += 1
                return True
            return False
        except Exception:
            return False
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about the current conversation."""
        return {
            'questions_asked': len(self.conversation_state['asked_questions']),
            'questions_remaining': len([
                q for q in self.question_db.questions 
                if q['id'] not in self.conversation_state['asked_questions']
            ]),
            'current_style': self.conversation_state['conversation_style'],
            'context_keywords': self.conversation_state['context_keywords'],
            'categories_covered': list(set([
                q['category'] for q in self.question_db.questions 
                if q['id'] in self.conversation_state['asked_questions']
            ]))
        }
    
    def suggest_topics(self) -> List[str]:
        """Suggest conversation topics based on available questions."""
        # Get categories not yet extensively covered
        stats = self.get_conversation_stats()
        covered_categories = stats['categories_covered']
        
        all_categories = self.question_db.get_all_categories()
        uncovered_categories = [cat for cat in all_categories if cat not in covered_categories]
        
        # Create topic suggestions
        topic_suggestions = []
        category_descriptions = {
            'personal': 'Personal goals and aspirations',
            'problem_solving': 'Decision-making and problem-solving approaches',
            'values': 'Core values and beliefs',
            'learning': 'Learning preferences and experiences',
            'reflection': 'Self-reflection and personal growth',
            'future': 'Future planning and vision',
            'relationships': 'Relationship dynamics and communication',
            'career': 'Career goals and professional development',
            'lifestyle': 'Lifestyle choices and preferences',
            'creativity': 'Creative thinking and expression'
        }
        
        for category in uncovered_categories[:3]:  # Suggest top 3 uncovered topics
            description = category_descriptions.get(category, f'{category.title()} related topics')
            topic_suggestions.append(description)
        
        return topic_suggestions
    
    def reset_conversation(self):
        """Reset the conversation to start fresh."""
        self.conversation_state = {
            'current_question_index': 0,
            'asked_questions': set(),
            'question_sequence': [],
            'context_keywords': [],
            'user_preferences': {},
            'conversation_style': 'adaptive'
        }
        self.initialize_conversation()
    
    def export_conversation_data(self) -> Dict[str, Any]:
        """Export conversation data for analysis or saving."""
        # Convert sets to lists for JSON serialization
        exportable_state = self.conversation_state.copy()
        exportable_state['asked_questions'] = list(self.conversation_state['asked_questions'])
        
        return {
            'conversation_state': exportable_state,
            'stats': self.get_conversation_stats(),
            'suggested_topics': self.suggest_topics()
        }