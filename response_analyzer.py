"""
Response Analyzer Module
Analyzes user responses to provide insights and feedback.
"""

import re
from typing import Dict, List, Any, Tuple
from collections import Counter
from datetime import datetime

class ResponseAnalyzer:
    def __init__(self):
        """Initialize the response analyzer."""
        self.sentiment_keywords = {
            'positive': [
                'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                'love', 'enjoy', 'excited', 'happy', 'satisfied', 'confident',
                'optimistic', 'successful', 'achievement', 'progress', 'growth'
            ],
            'negative': [
                'bad', 'terrible', 'awful', 'hate', 'dislike', 'frustrated',
                'angry', 'sad', 'disappointed', 'worried', 'stressed', 'anxious',
                'difficult', 'challenging', 'problem', 'issue', 'struggle'
            ],
            'neutral': [
                'okay', 'fine', 'normal', 'average', 'usual', 'standard',
                'typical', 'regular', 'common', 'moderate'
            ]
        }
        
        self.emotion_patterns = {
            'enthusiasm': r'\b(excited|thrilled|passionate|energetic|motivated)\b',
            'concern': r'\b(worried|concerned|anxious|nervous|uncertain)\b',
            'confidence': r'\b(confident|sure|certain|determined|strong)\b',
            'doubt': r'\b(unsure|doubt|uncertain|hesitant|confused)\b',
            'satisfaction': r'\b(satisfied|content|pleased|happy|fulfilled)\b',
            'frustration': r'\b(frustrated|annoyed|irritated|stuck|blocked)\b'
        }
        
        self.goal_indicators = [
            'want to', 'plan to', 'hoping to', 'aiming for', 'working towards',
            'goal is', 'objective', 'target', 'aspire to', 'strive for'
        ]
        
        self.value_indicators = [
            'important', 'value', 'believe', 'principle', 'matters to me',
            'care about', 'priority', 'essential', 'crucial', 'fundamental'
        ]
    
    def analyze_response(self, question: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Analyze a single response to a question."""
        analysis = {
            'question_id': question['id'],
            'response_length': len(response.split()),
            'sentiment': self._analyze_sentiment(response),
            'emotions': self._detect_emotions(response),
            'key_themes': self._extract_key_themes(response),
            'goals_mentioned': self._extract_goals(response),
            'values_expressed': self._extract_values(response),
            'complexity_score': self._calculate_complexity(response),
            'engagement_level': self._assess_engagement(response),
            'question_type': question.get('type', 'unknown'),
            'category': question.get('category', 'unknown')
        }
        
        # Add specific analysis based on question type
        if question.get('type') == 'multiple_choice':
            analysis['selected_option'] = self._extract_choice(response, question.get('options', []))
        
        return analysis
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the text."""
        text_lower = text.lower()
        sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for sentiment, keywords in self.sentiment_keywords.items():
            for keyword in keywords:
                sentiment_scores[sentiment] += text_lower.count(keyword)
        
        # Determine overall sentiment
        total_score = sum(sentiment_scores.values())
        if total_score == 0:
            overall_sentiment = 'neutral'
            confidence = 0.5
        else:
            overall_sentiment = max(sentiment_scores, key=sentiment_scores.get)
            confidence = sentiment_scores[overall_sentiment] / total_score
        
        return {
            'overall': overall_sentiment,
            'confidence': confidence,
            'scores': sentiment_scores
        }
    
    def _detect_emotions(self, text: str) -> List[Dict[str, Any]]:
        """Detect emotions in the text."""
        emotions_found = []
        text_lower = text.lower()
        
        for emotion, pattern in self.emotion_patterns.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                emotions_found.append({
                    'emotion': emotion,
                    'strength': len(matches),
                    'indicators': matches
                })
        
        return sorted(emotions_found, key=lambda x: x['strength'], reverse=True)
    
    def _extract_key_themes(self, text: str) -> List[str]:
        """Extract key themes and topics from the text."""
        # Simple keyword extraction (could be enhanced with NLP libraries)
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common words
        stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
            'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
            'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
            'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
            'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
            'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
            'with', 'through', 'during', 'before', 'after', 'above', 'below',
            'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
        }
        
        filtered_words = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Count word frequency and return most common themes
        word_counts = Counter(filtered_words)
        return [word for word, count in word_counts.most_common(5)]
    
    def _extract_goals(self, text: str) -> List[str]:
        """Extract mentioned goals from the text."""
        goals = []
        text_lower = text.lower()
        
        for indicator in self.goal_indicators:
            if indicator in text_lower:
                # Find the sentence containing the goal indicator
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    if indicator in sentence.lower():
                        goals.append(sentence.strip())
        
        return goals[:3]  # Limit to 3 goals
    
    def _extract_values(self, text: str) -> List[str]:
        """Extract expressed values from the text."""
        values = []
        text_lower = text.lower()
        
        for indicator in self.value_indicators:
            if indicator in text_lower:
                # Find the sentence containing the value indicator
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    if indicator in sentence.lower():
                        values.append(sentence.strip())
        
        return values[:3]  # Limit to 3 values
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate complexity score of the response."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        if not words or not sentences:
            return 0.0
        
        # Factors for complexity
        avg_word_length = sum(len(word) for word in words) / len(words)
        avg_sentence_length = len(words) / len([s for s in sentences if s.strip()])
        
        # Simple complexity score (0-1)
        complexity = min(1.0, (avg_word_length * avg_sentence_length) / 50)
        
        return round(complexity, 2)
    
    def _assess_engagement(self, text: str) -> Dict[str, Any]:
        """Assess user engagement level based on response characteristics."""
        word_count = len(text.split())
        
        # Engagement indicators
        has_examples = bool(re.search(r'\b(for example|such as|like|including)\b', text, re.IGNORECASE))
        has_personal_pronouns = bool(re.search(r'\b(i|me|my|myself)\b', text, re.IGNORECASE))
        has_emotions = len(self._detect_emotions(text)) > 0
        
        # Calculate engagement score
        score = 0
        if word_count > 10: score += 1
        if word_count > 30: score += 1
        if has_examples: score += 1
        if has_personal_pronouns: score += 1
        if has_emotions: score += 1
        
        engagement_level = 'low' if score <= 1 else 'medium' if score <= 3 else 'high'
        
        return {
            'level': engagement_level,
            'score': score,
            'word_count': word_count,
            'indicators': {
                'has_examples': has_examples,
                'has_personal_pronouns': has_personal_pronouns,
                'has_emotions': has_emotions
            }
        }
    
    def _extract_choice(self, response: str, options: List[str]) -> str:
        """Extract selected choice from multiple choice response."""
        response_lower = response.lower()
        
        # Check for exact matches or partial matches
        for option in options:
            option_lower = option.lower()
            if option_lower in response_lower:
                return option
        
        # Check for numbered choices
        for i, option in enumerate(options, 1):
            if str(i) in response or f"{i}." in response or f"{i})" in response:
                return option
        
        return "No clear choice detected"
    
    def generate_summary(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of all analysis results."""
        if not analysis_results:
            return {'error': 'No analysis results to summarize'}
        
        # Aggregate data
        total_responses = len(analysis_results)
        sentiments = [result['sentiment']['overall'] for result in analysis_results]
        engagement_levels = [result['engagement_level']['level'] for result in analysis_results]
        
        # Count sentiments and engagement
        sentiment_counts = Counter(sentiments)
        engagement_counts = Counter(engagement_levels)
        
        # Extract all themes
        all_themes = []
        for result in analysis_results:
            all_themes.extend(result['key_themes'])
        
        top_themes = [theme for theme, count in Counter(all_themes).most_common(5)]
        
        # Calculate averages
        avg_complexity = sum(result['complexity_score'] for result in analysis_results) / total_responses
        avg_word_count = sum(result['response_length'] for result in analysis_results) / total_responses
        
        return {
            'total_responses': total_responses,
            'sentiment_distribution': dict(sentiment_counts),
            'engagement_distribution': dict(engagement_counts),
            'top_themes': top_themes,
            'average_complexity': round(avg_complexity, 2),
            'average_word_count': round(avg_word_count, 1),
            'dominant_sentiment': sentiment_counts.most_common(1)[0][0] if sentiment_counts else 'neutral',
            'dominant_engagement': engagement_counts.most_common(1)[0][0] if engagement_counts else 'medium'
        }
    
    def generate_final_analysis(self, responses: List[Dict[str, Any]], 
                              analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive final analysis."""
        summary = self.generate_summary(analysis_results)
        
        # Extract patterns and insights
        patterns = self._identify_patterns(analysis_results)
        insights = self._generate_insights(summary, patterns)
        recommendations = self._generate_recommendations(summary, patterns)
        
        return {
            'session_summary': summary,
            'patterns_identified': patterns,
            'key_insights': insights,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _identify_patterns(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify patterns in the analysis results."""
        patterns = {
            'sentiment_trend': [],
            'engagement_trend': [],
            'complexity_trend': [],
            'common_emotions': [],
            'recurring_themes': []
        }
        
        # Track trends over time
        for result in analysis_results:
            patterns['sentiment_trend'].append(result['sentiment']['overall'])
            patterns['engagement_trend'].append(result['engagement_level']['level'])
            patterns['complexity_trend'].append(result['complexity_score'])
        
        # Find common emotions
        all_emotions = []
        for result in analysis_results:
            for emotion_data in result['emotions']:
                all_emotions.append(emotion_data['emotion'])
        
        patterns['common_emotions'] = [emotion for emotion, count in 
                                     Counter(all_emotions).most_common(3)]
        
        # Find recurring themes
        all_themes = []
        for result in analysis_results:
            all_themes.extend(result['key_themes'])
        
        patterns['recurring_themes'] = [theme for theme, count in 
                                      Counter(all_themes).most_common(3)]
        
        return patterns
    
    def _generate_insights(self, summary: Dict[str, Any], patterns: Dict[str, Any]) -> List[str]:
        """Generate key insights from the analysis."""
        insights = []
        
        # Sentiment insights
        dominant_sentiment = summary.get('dominant_sentiment', 'neutral')
        if dominant_sentiment == 'positive':
            insights.append("You generally express a positive outlook in your responses.")
        elif dominant_sentiment == 'negative':
            insights.append("Your responses tend to focus on challenges and concerns.")
        
        # Engagement insights
        dominant_engagement = summary.get('dominant_engagement', 'medium')
        if dominant_engagement == 'high':
            insights.append("You show high engagement with detailed, thoughtful responses.")
        elif dominant_engagement == 'low':
            insights.append("You tend to give brief, concise responses.")
        
        # Theme insights
        top_themes = summary.get('top_themes', [])
        if top_themes:
            insights.append(f"Your main areas of focus include: {', '.join(top_themes[:3])}.")
        
        # Emotion insights
        common_emotions = patterns.get('common_emotions', [])
        if common_emotions:
            insights.append(f"You frequently express emotions related to: {', '.join(common_emotions)}.")
        
        return insights
    
    def _generate_recommendations(self, summary: Dict[str, Any], 
                                patterns: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        
        # Based on sentiment
        dominant_sentiment = summary.get('dominant_sentiment', 'neutral')
        if dominant_sentiment == 'negative':
            recommendations.append("Consider exploring positive coping strategies and focusing on strengths.")
        
        # Based on engagement
        dominant_engagement = summary.get('dominant_engagement', 'medium')
        if dominant_engagement == 'low':
            recommendations.append("Try to elaborate more on your thoughts to gain deeper insights.")
        
        # Based on complexity
        avg_complexity = summary.get('average_complexity', 0)
        if avg_complexity < 0.3:
            recommendations.append("Consider exploring more nuanced aspects of your thoughts and feelings.")
        
        # Based on themes
        top_themes = summary.get('top_themes', [])
        if 'goal' in ' '.join(top_themes).lower() or 'future' in ' '.join(top_themes).lower():
            recommendations.append("Focus on creating specific action plans for your goals.")
        
        return recommendations