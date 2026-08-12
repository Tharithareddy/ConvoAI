#!/usr/bin/env python3
"""
Demo script for ConvoAI - Shows key features and capabilities
Run this to see a quick demonstration of the application.
"""

import json
from datetime import datetime
from conversation_engine import ConversationEngine
from question_database import QuestionDatabase
from response_analyzer import ResponseAnalyzer
from ui_handler import UIHandler

def demo_analysis():
    """Demonstrate the analysis capabilities with sample responses."""
    print("🔬 ConvoAI Analysis Demo")
    print("=" * 50)
    
    # Initialize components
    question_db = QuestionDatabase()
    analyzer = ResponseAnalyzer()
    ui = UIHandler()
    
    # Sample responses for demonstration
    sample_responses = [
        {
            'question': question_db.get_question_by_id(1),  # Goals question
            'response': "I want to learn Python programming and start a small business. I'm excited about the possibilities but worried about finding enough time with my current job responsibilities."
        },
        {
            'question': question_db.get_question_by_id(4),  # Decision-making question  
            'response': "Logic and facts are important, but I also trust my gut feeling. Past experiences really shape how I approach new situations."
        },
        {
            'question': question_db.get_question_by_id(5),  # Motivation question
            'response': "Making a positive impact motivates me the most. I love helping others and seeing tangible results from my efforts."
        }
    ]
    
    analysis_results = []
    
    print("\n📝 Analyzing Sample Responses:\n")
    
    for i, sample in enumerate(sample_responses, 1):
        question = sample['question']
        response = sample['response']
        
        print(f"Question {i}: {question['text']}")
        print(f"Response: \"{response}\"")
        
        # Analyze the response
        analysis = analyzer.analyze_response(question, response)
        analysis_results.append(analysis)
        
        # Show analysis
        print(f"\n💡 Analysis:")
        print(f"  Sentiment: {analysis['sentiment']['overall'].title()} (confidence: {analysis['sentiment']['confidence']:.2f})")
        print(f"  Engagement: {analysis['engagement_level']['level'].title()}")
        print(f"  Word count: {analysis['response_length']}")
        print(f"  Complexity: {analysis['complexity_score']:.2f}")
        
        if analysis['emotions']:
            emotions = [e['emotion'] for e in analysis['emotions'][:2]]
            print(f"  Emotions: {', '.join(emotions)}")
        
        if analysis['key_themes']:
            print(f"  Key themes: {', '.join(analysis['key_themes'][:3])}")
        
        print("-" * 40)
    
    # Generate summary
    print(f"\n📊 Summary Analysis:")
    summary = analyzer.generate_summary(analysis_results)
    ui.display_analysis_summary(summary)
    
    # Generate final analysis
    print(f"\n🎯 Final Analysis:")
    responses_data = [
        {
            'question_id': sample['question']['id'],
            'question_text': sample['question']['text'],
            'response': sample['response'],
            'timestamp': datetime.now().isoformat()
        }
        for sample in sample_responses
    ]
    
    final_analysis = analyzer.generate_final_analysis(responses_data, analysis_results)
    ui.display_final_analysis(final_analysis)

def demo_conversation_flow():
    """Demonstrate conversation flow without user input."""
    print("\n🤖 Conversation Flow Demo")
    print("=" * 50)
    
    question_db = QuestionDatabase()
    analyzer = ResponseAnalyzer() 
    engine = ConversationEngine(question_db, analyzer)
    
    print("\n📋 Available Question Categories:")
    categories = question_db.get_all_categories()
    for category in categories:
        questions_count = len(question_db.get_questions_by_category(category))
        print(f"  • {category.title()}: {questions_count} questions")
    
    print(f"\n🎯 Sample Starting Questions:")
    starting_questions = question_db.get_starting_questions()
    for i, question in enumerate(starting_questions, 1):
        print(f"  {i}. [{question['category'].title()}] {question['text']}")
    
    print(f"\n🔄 Adaptive Question Selection:")
    print("  • Questions adapt based on your response patterns")
    print("  • Follow-up questions are selected contextually")  
    print("  • Keywords from responses influence future questions")
    print("  • Engagement level affects question complexity")
    
    # Show conversation stats
    stats = engine.get_conversation_stats()
    print(f"\n📈 Current Conversation Statistics:")
    print(f"  Questions available: {stats['questions_remaining']}")
    print(f"  Categories: {', '.join(stats['categories_covered']) if stats['categories_covered'] else 'None yet'}")
    print(f"  Style: {stats['current_style'].title()}")

def demo_question_types():
    """Demonstrate different types of questions."""
    print("\n❓ Question Types Demo") 
    print("=" * 50)
    
    question_db = QuestionDatabase()
    ui = UIHandler()
    
    # Find examples of each question type
    question_types = {}
    for question in question_db.questions:
        q_type = question.get('type', 'open_ended')
        if q_type not in question_types:
            question_types[q_type] = question
    
    print("\n📋 Different Question Types:\n")
    
    for q_type, question in question_types.items():
        print(f"🔸 {q_type.replace('_', ' ').title()} Question:")
        
        # Display the question using UI handler
        ui.display_question(question)
        
        # Show sample response based on type
        if q_type == 'multiple_choice':
            print("Sample response: 'I'd choose option 2 - Logic and facts, because...'")
        elif q_type == 'ranking':
            print("Sample response: 'Trust is most important, followed by communication...'")
        else:
            print("Sample response: 'This is where you share your thoughts in detail...'")
        
        print("\n" + "-" * 60 + "\n")

def main():
    """Run all demos."""
    print("🚀 ConvoAI Feature Demonstration")
    print("=" * 60)
    print("This demo shows the key features of ConvoAI without requiring user input.\n")
    
    # Run demos
    demo_question_types()
    demo_conversation_flow() 
    demo_analysis()
    
    print(f"\n✨ Demo Complete!")
    print("To try ConvoAI interactively, run: python main.py")
    print("=" * 60)

if __name__ == "__main__":
    main()