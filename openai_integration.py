"""
OpenAI Integration for ConvoAI
Provides enhanced analysis and dynamic question generation using GPT models.
"""

from openai import OpenAI
import json
import logging
from typing import Dict, List, Optional
from config import Config

class OpenAIAnalyzer:
    """Enhanced response analyzer using OpenAI GPT models"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client"""
        self.api_key = api_key or Config.get_openai_key()
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.enabled = True
            logging.info("OpenAI integration enabled")
        else:
            self.client = None
            self.enabled = False
            logging.warning("OpenAI API key not found. Using basic analysis only.")
    
    def analyze_response_advanced(self, question: str, response: str, context: List[Dict] = None) -> Dict:
        """
        Perform advanced analysis of user response using GPT
        
        Args:
            question: The question that was asked
            response: User's response
            context: Previous questions and responses for context
        
        Returns:
            Dictionary with advanced analysis insights
        """
        if not self.enabled:
            return {"error": "OpenAI integration not available"}
        
        try:
            # Build context from previous responses
            context_str = ""
            if context:
                context_str = "\n".join([
                    f"Q: {item['question']['text']}\nA: {item['response']}"
                    for item in context[-3:]  # Last 3 for context
                ])
            
            prompt = f"""
As a professional psychological analyst and life coach, analyze this conversation response in depth.

Previous Context (if any):
{context_str}

Current Question: {question}
User Response: {response}

Provide a comprehensive analysis in the following JSON format:
{{
    "psychological_insights": {{
        "emotional_state": "current emotional state with confidence level",
        "cognitive_patterns": ["identified thinking patterns"],
        "personality_indicators": ["personality traits observed"],
        "stress_indicators": ["signs of stress or well-being"],
        "growth_areas": ["potential areas for personal development"]
    }},
    "sentiment_analysis": {{
        "primary_emotion": "main emotion",
        "emotional_intensity": "scale 1-10",
        "emotional_complexity": "simple/moderate/complex",
        "positivity_score": "0-100"
    }},
    "behavioral_insights": {{
        "communication_style": "description of how they communicate",
        "openness_level": "how open/guarded they are",
        "reflection_depth": "shallow/moderate/deep",
        "self_awareness": "level of self-understanding shown"
    }},
    "recommendations": {{
        "immediate_actions": ["actionable steps they could take"],
        "reflection_questions": ["questions for deeper self-reflection"],
        "professional_guidance": "whether professional help might be beneficial",
        "strengths_to_leverage": ["positive aspects to build upon"]
    }},
    "conversation_guidance": {{
        "suggested_follow_up": "what to explore next",
        "conversation_depth": "should we go deeper or move on",
        "emotional_support_needed": "level of support/encouragement needed"
    }}
}}

Be empathetic, non-judgmental, and focus on growth and understanding. Provide specific, actionable insights.
"""
            
            response_obj = self.client.chat.completions.create(
                model="gpt-4",  # Use gpt-3.5-turbo for cost savings
                messages=[
                    {"role": "system", "content": "You are a professional psychological analyst and life coach with expertise in conversation analysis and personal development."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            analysis_text = response_obj.choices[0].message.content
            
            # Parse JSON response
            try:
                analysis = json.loads(analysis_text)
                analysis["source"] = "openai_gpt4"
                return analysis
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured fallback
                return {
                    "raw_analysis": analysis_text,
                    "source": "openai_gpt4_raw",
                    "error": "JSON parsing failed, returned raw analysis"
                }
                
        except Exception as e:
            logging.error(f"OpenAI analysis error: {str(e)}")
            return {
                "error": f"OpenAI analysis failed: {str(e)}",
                "source": "error"
            }
    
    def generate_follow_up_question(self, conversation_history: List[Dict], user_profile: Dict = None) -> Dict:
        """
        Generate a personalized follow-up question based on conversation history
        
        Args:
            conversation_history: List of previous questions and responses
            user_profile: User profile information if available
        
        Returns:
            Dictionary with generated question and metadata
        """
        if not self.enabled:
            return {"error": "OpenAI integration not available"}
        
        try:
            # Build conversation context
            history_str = "\n".join([
                f"Q: {item['question']['text']}\nA: {item['response']}"
                for item in conversation_history[-5:]  # Last 5 exchanges
            ])
            
            prompt = f"""
As a professional conversation facilitator and life coach, generate a thoughtful follow-up question based on this conversation history.

Conversation History:
{history_str}

Generate a question that:
1. Builds on themes already discussed
2. Helps the person explore their thoughts/feelings deeper
3. Is open-ended and encourages reflection
4. Feels natural and conversational
5. Promotes self-discovery and growth

Provide response in this JSON format:
{{
    "question": {{
        "text": "the generated question",
        "type": "open_ended",
        "category": "follow_up",
        "focus_area": "what this question explores (emotions/values/goals/relationships/etc)",
        "depth_level": "surface/moderate/deep"
    }},
    "rationale": {{
        "why_this_question": "explanation of why this question follows logically",
        "what_it_explores": "what insights this question might reveal",
        "connection_to_previous": "how it builds on previous responses"
    }},
    "coaching_notes": {{
        "expected_benefits": "what the person might gain from answering",
        "potential_resistance": "areas where they might hesitate",
        "support_needed": "how to encourage open sharing"
    }}
}}

Make the question feel personal and relevant to their specific situation.
"""
            
            response_obj = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert conversation facilitator and life coach specializing in personal development conversations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # Higher creativity for question generation
                max_tokens=800
            )
            
            question_text = response_obj.choices[0].message.content
            
            try:
                question_data = json.loads(question_text)
                question_data["source"] = "openai_generated"
                return question_data
            except json.JSONDecodeError:
                return {
                    "error": "JSON parsing failed",
                    "raw_response": question_text,
                    "source": "openai_raw"
                }
                
        except Exception as e:
            logging.error(f"OpenAI question generation error: {str(e)}")
            return {
                "error": f"Question generation failed: {str(e)}",
                "source": "error"
            }
    
    def generate_conversation_summary(self, conversation_history: List[Dict]) -> Dict:
        """
        Generate a comprehensive conversation summary and insights
        
        Args:
            conversation_history: Complete conversation history
        
        Returns:
            Dictionary with summary and insights
        """
        if not self.enabled:
            return {"error": "OpenAI integration not available"}
        
        try:
            # Build full conversation
            history_str = "\n".join([
                f"Q: {item['question']['text']}\nA: {item['response']}"
                for item in conversation_history
            ])
            
            prompt = f"""
As a professional therapist and life coach, provide a comprehensive summary of this conversation session.

Complete Conversation:
{history_str}

Provide a detailed analysis in this JSON format:
{{
    "session_summary": {{
        "main_themes": ["primary topics discussed"],
        "emotional_journey": "how their emotions evolved during conversation",
        "key_revelations": ["important insights they shared"],
        "growth_moments": ["moments of self-discovery or awareness"]
    }},
    "personality_profile": {{
        "communication_style": "how they express themselves",
        "core_values": ["values that seem important to them"],
        "strengths": ["positive qualities observed"],
        "challenges": ["areas where they might struggle"],
        "coping_mechanisms": ["how they handle difficulties"]
    }},
    "psychological_insights": {{
        "overall_mental_state": "general assessment of wellbeing",
        "stress_levels": "apparent stress or calm",
        "self_awareness": "level of insight into themselves",
        "emotional_regulation": "how well they manage emotions",
        "relationship_patterns": ["insights about how they relate to others"]
    }},
    "recommendations": {{
        "immediate_focus_areas": ["what to work on right away"],
        "long_term_development": ["areas for ongoing growth"],
        "suggested_resources": ["books, practices, or tools that might help"],
        "professional_support": "whether therapy or coaching would be beneficial",
        "action_steps": ["concrete steps they can take"]
    }},
    "conversation_quality": {{
        "depth_achieved": "how deep the conversation went",
        "openness_level": "how open and honest they were",
        "engagement": "how actively they participated",
        "breakthrough_moments": ["significant insights or realizations"]
    }}
}}

Be supportive, insightful, and focus on their strengths while gently addressing growth areas.
"""
            
            response_obj = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional therapist and life coach with expertise in conversation analysis and personal development."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            summary_text = response_obj.choices[0].message.content
            
            try:
                summary = json.loads(summary_text)
                summary["source"] = "openai_gpt4"
                summary["session_length"] = len(conversation_history)
                return summary
            except json.JSONDecodeError:
                return {
                    "raw_summary": summary_text,
                    "source": "openai_raw",
                    "error": "JSON parsing failed"
                }
                
        except Exception as e:
            logging.error(f"OpenAI summary generation error: {str(e)}")
            return {
                "error": f"Summary generation failed: {str(e)}",
                "source": "error"
            }

# Factory function to create analyzer
def create_openai_analyzer(api_key: str = None) -> OpenAIAnalyzer:
    """Create OpenAI analyzer instance"""
    return OpenAIAnalyzer(api_key)