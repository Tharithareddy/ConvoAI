#!/usr/bin/env python3
"""
Simple test script to verify ConvoAI components work correctly.
"""

def test_imports():
    """Test that all modules can be imported."""
    try:
        from question_database import QuestionDatabase
        from response_analyzer import ResponseAnalyzer
        from conversation_engine import ConversationEngine
        from ui_handler import UIHandler
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_question_database():
    """Test QuestionDatabase functionality."""
    try:
        from question_database import QuestionDatabase
        db = QuestionDatabase()
        questions = db.questions
        assert len(questions) > 0, "No questions loaded"
        
        # Test getting question by ID
        first_question = db.get_question_by_id(1)
        assert first_question is not None, "Could not get question by ID"
        
        # Test categories
        categories = db.get_all_categories()
        assert len(categories) > 0, "No categories found"
        
        print(f"✅ Question Database: {len(questions)} questions, {len(categories)} categories")
        return True
    except Exception as e:
        print(f"❌ Question Database error: {e}")
        return False

def test_response_analyzer():
    """Test ResponseAnalyzer functionality."""
    try:
        from response_analyzer import ResponseAnalyzer
        analyzer = ResponseAnalyzer()
        
        # Test with sample question and response
        sample_question = {
            'id': 1,
            'text': 'Test question',
            'type': 'open_ended',
            'category': 'test'
        }
        sample_response = "I am feeling excited and motivated about my goals for the future."
        
        analysis = analyzer.analyze_response(sample_question, sample_response)
        
        assert 'sentiment' in analysis, "No sentiment analysis"
        assert 'emotions' in analysis, "No emotion detection"
        assert 'key_themes' in analysis, "No theme extraction"
        
        print("✅ Response Analyzer: All analysis features working")
        return True
    except Exception as e:
        print(f"❌ Response Analyzer error: {e}")
        return False

def test_ui_handler():
    """Test UIHandler functionality."""
    try:
        from ui_handler import UIHandler
        ui = UIHandler()
        
        # Test text wrapping
        long_text = "This is a very long text that should be wrapped properly when displayed in the console interface."
        wrapped = ui._wrap_text(long_text)
        assert len(wrapped) > 0, "Text wrapping failed"
        
        # Test color functionality
        colored_text = ui._colorize("Test", "blue")
        assert len(colored_text) > 0, "Color formatting failed"
        
        print("✅ UI Handler: Display formatting working")
        return True
    except Exception as e:
        print(f"❌ UI Handler error: {e}")
        return False

def test_conversation_engine():
    """Test ConversationEngine functionality."""
    try:
        from question_database import QuestionDatabase
        from response_analyzer import ResponseAnalyzer
        from conversation_engine import ConversationEngine
        
        db = QuestionDatabase()
        analyzer = ResponseAnalyzer()
        engine = ConversationEngine(db, analyzer)
        
        # Test getting next question
        question = engine.get_next_question()
        assert question is not None, "Could not get next question"
        
        # Test conversation stats
        stats = engine.get_conversation_stats()
        assert 'questions_asked' in stats, "No conversation stats"
        
        print("✅ Conversation Engine: Question flow working")
        return True
    except Exception as e:
        print(f"❌ Conversation Engine error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 ConvoAI Component Tests")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_question_database, 
        test_response_analyzer,
        test_ui_handler,
        test_conversation_engine
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! ConvoAI is ready to use.")
        print("Run 'python main.py' to start the interactive conversation.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()