"""
Question Database Module
Manages predefined questions for the conversational AI.
"""

import json
from typing import List, Dict, Any, Optional

class QuestionDatabase:
    def __init__(self):
        """Initialize the question database."""
        self.questions = self._load_default_questions()
        self.categories = self._organize_by_category()
    
    def _load_default_questions(self) -> List[Dict[str, Any]]:
        """Load default set of predefined questions."""
        return [
            {
                'id': 1,
                'category': 'personal',
                'text': "What are your main goals for this year?",
                'type': 'open_ended',
                'keywords': ['goals', 'objectives', 'plans', 'aspirations'],
                'follow_up_questions': [2, 3]
            },
            {
                'id': 2,
                'category': 'personal',
                'text': "What challenges do you anticipate in achieving these goals?",
                'type': 'open_ended',
                'keywords': ['challenges', 'obstacles', 'difficulties', 'barriers'],
                'follow_up_questions': [4]
            },
            {
                'id': 3,
                'category': 'personal',
                'text': "How do you typically measure success in your endeavors?",
                'type': 'open_ended',
                'keywords': ['success', 'measurement', 'metrics', 'achievement'],
                'follow_up_questions': [5]
            },
            {
                'id': 4,
                'category': 'problem_solving',
                'text': "When facing a difficult decision, what factors do you consider most important?",
                'type': 'multiple_choice',
                'options': [
                    'Logic and facts',
                    'Gut feeling and intuition',
                    'Advice from others',
                    'Past experiences',
                    'Potential consequences'
                ],
                'keywords': ['decision', 'factors', 'important', 'consider'],
                'follow_up_questions': [6, 7]
            },
            {
                'id': 5,
                'category': 'personal',
                'text': "What motivates you most in your daily activities?",
                'type': 'open_ended',
                'keywords': ['motivation', 'drive', 'inspiration', 'purpose'],
                'follow_up_questions': [8]
            },
            {
                'id': 6,
                'category': 'problem_solving',
                'text': "Can you describe a recent situation where you had to adapt quickly to change?",
                'type': 'open_ended',
                'keywords': ['adapt', 'change', 'flexibility', 'adjustment'],
                'follow_up_questions': [9]
            },
            {
                'id': 7,
                'category': 'problem_solving',
                'text': "How do you handle stress and pressure in challenging situations?",
                'type': 'open_ended',
                'keywords': ['stress', 'pressure', 'handle', 'cope'],
                'follow_up_questions': [10]
            },
            {
                'id': 8,
                'category': 'values',
                'text': "What values are most important to you in your relationships?",
                'type': 'ranking',
                'options': [
                    'Trust and honesty',
                    'Mutual respect',
                    'Good communication',
                    'Shared interests',
                    'Emotional support',
                    'Independence'
                ],
                'keywords': ['values', 'relationships', 'important'],
                'follow_up_questions': [11]
            },
            {
                'id': 9,
                'category': 'learning',
                'text': "How do you prefer to learn new skills or information?",
                'type': 'multiple_choice',
                'options': [
                    'Hands-on practice',
                    'Reading and research',
                    'Watching tutorials/videos',
                    'Learning from others',
                    'Trial and error'
                ],
                'keywords': ['learn', 'skills', 'information', 'prefer'],
                'follow_up_questions': [12]
            },
            {
                'id': 10,
                'category': 'reflection',
                'text': "What do you think is your greatest strength, and how do you use it?",
                'type': 'open_ended',
                'keywords': ['strength', 'greatest', 'use', 'advantage'],
                'follow_up_questions': [13]
            },
            {
                'id': 11,
                'category': 'values',
                'text': "If you could change one thing about your current situation, what would it be?",
                'type': 'open_ended',
                'keywords': ['change', 'situation', 'current', 'improve'],
                'follow_up_questions': [14]
            },
            {
                'id': 12,
                'category': 'learning',
                'text': "What's something new you've learned recently that excited you?",
                'type': 'open_ended',
                'keywords': ['learned', 'recently', 'excited', 'new'],
                'follow_up_questions': [15]
            },
            {
                'id': 13,
                'category': 'reflection',
                'text': "How do you handle criticism or feedback from others?",
                'type': 'open_ended',
                'keywords': ['criticism', 'feedback', 'handle', 'others'],
                'follow_up_questions': []
            },
            {
                'id': 14,
                'category': 'future',
                'text': "Where do you see yourself in 5 years, and what steps are you taking to get there?",
                'type': 'open_ended',
                'keywords': ['future', '5 years', 'steps', 'progress'],
                'follow_up_questions': []
            },
            {
                'id': 15,
                'category': 'learning',
                'text': "What advice would you give to someone facing a similar challenge to one you've overcome?",
                'type': 'open_ended',
                'keywords': ['advice', 'challenge', 'overcome', 'similar'],
                'follow_up_questions': []
            }
        ]
    
    def _organize_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """Organize questions by category."""
        categories = {}
        for question in self.questions:
            category = question['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(question)
        return categories
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific question by ID."""
        for question in self.questions:
            if question['id'] == question_id:
                return question
        return None
    
    def get_questions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all questions in a specific category."""
        return self.categories.get(category, [])
    
    def get_follow_up_questions(self, question_id: int) -> List[Dict[str, Any]]:
        """Get follow-up questions for a given question."""
        question = self.get_question_by_id(question_id)
        if not question:
            return []
        
        follow_ups = []
        for follow_up_id in question.get('follow_up_questions', []):
            follow_up = self.get_question_by_id(follow_up_id)
            if follow_up:
                follow_ups.append(follow_up)
        
        return follow_ups
    
    def get_starting_questions(self) -> List[Dict[str, Any]]:
        """Get good starting questions for a conversation."""
        # Return first question from each category
        starting_questions = []
        seen_categories = set()
        
        for question in self.questions:
            if question['category'] not in seen_categories:
                starting_questions.append(question)
                seen_categories.add(question['category'])
        
        return starting_questions[:3]  # Limit to 3 starting questions
    
    def search_questions_by_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Search questions by keywords."""
        matching_questions = []
        keywords_lower = [k.lower() for k in keywords]
        
        for question in self.questions:
            question_keywords = [k.lower() for k in question.get('keywords', [])]
            question_text_lower = question['text'].lower()
            
            # Check if any keyword matches
            if any(keyword in question_keywords or keyword in question_text_lower 
                   for keyword in keywords_lower):
                matching_questions.append(question)
        
        return matching_questions
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories."""
        return list(self.categories.keys())
    
    def add_question(self, question: Dict[str, Any]) -> bool:
        """Add a new question to the database."""
        try:
            # Generate new ID
            max_id = max([q['id'] for q in self.questions]) if self.questions else 0
            question['id'] = max_id + 1
            
            # Add to questions list
            self.questions.append(question)
            
            # Update categories
            self.categories = self._organize_by_category()
            
            return True
        except Exception:
            return False
    
    def save_questions_to_file(self, filename: str) -> bool:
        """Save questions to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.questions, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def load_questions_from_file(self, filename: str) -> bool:
        """Load questions from a JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
            self.categories = self._organize_by_category()
            return True
        except Exception:
            return False