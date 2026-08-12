#!/usr/bin/env python3
"""
ConvoAI with OpenAI Integration - Example Usage
Run this script to see how OpenAI enhances your ConvoAI experience.
"""

import os
from main import ConvoAI

def demo_with_openai():
    """Demo ConvoAI with OpenAI features"""
    
    print("🤖 ConvoAI + OpenAI Integration Demo")
    print("=" * 50)
    
    # Get API key (you can set this directly or use environment variable)
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️ No API key provided - running with basic features only")
            convo = ConvoAI()
        else:
            print("✅ Using API key from environment variable")
            convo = ConvoAI(openai_api_key=api_key)
    else:
        print("✅ Using provided API key")
        convo = ConvoAI(openai_api_key=api_key)
    
    # Start the conversation
    convo.start_conversation()

def quick_analysis_demo():
    """Quick demo of OpenAI analysis features"""
    
    print("\n🧪 Quick OpenAI Analysis Demo")
    print("-" * 30)
    
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ API key required for this demo")
        return
    
    try:
        from openai_integration import OpenAIAnalyzer
        
        analyzer = OpenAIAnalyzer(api_key)
        
        if not analyzer.enabled:
            print("❌ Failed to initialize OpenAI analyzer")
            return
        
        # Sample analysis
        question = "How do you handle stress in your daily life?"
        response = "I usually try to take deep breaths and go for walks when I'm feeling overwhelmed. Sometimes I listen to music or talk to friends. But honestly, I often end up just pushing through it without really dealing with the underlying issues."
        
        print(f"\n📝 Sample Question: {question}")
        print(f"💬 Sample Response: {response}")
        print("\n🔄 Analyzing with OpenAI...")
        
        analysis = analyzer.analyze_response_advanced(question, response)
        
        if 'error' in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return
        
        print("\n✨ OpenAI Analysis Results:")
        print("-" * 40)
        
        # Display key insights
        if 'psychological_insights' in analysis:
            insights = analysis['psychological_insights']
            print(f"🧠 Emotional State: {insights.get('emotional_state', 'N/A')}")
            print(f"💡 Growth Areas: {', '.join(insights.get('growth_areas', []))}")
        
        if 'recommendations' in analysis:
            recs = analysis['recommendations']
            print(f"\n🎯 Immediate Actions:")
            for action in recs.get('immediate_actions', [])[:3]:
                print(f"  • {action}")
        
        print(f"\n💰 Estimated cost: ~$0.02-0.06")
        print("🎉 This is just a sample of what OpenAI integration provides!")
        
    except ImportError:
        print("❌ OpenAI integration not available. Run: pip install openai")
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Full ConvoAI session with OpenAI")
    print("2. Quick analysis demo")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        demo_with_openai()
    elif choice == "2":
        quick_analysis_demo()
    else:
        print("👋 Goodbye!")