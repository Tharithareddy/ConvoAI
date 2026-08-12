#!/usr/bin/env python3
"""
OpenAI Setup Script for ConvoAI
This script helps you configure OpenAI integration for enhanced analysis.
"""

import os
import sys
from pathlib import Path

def setup_openai():
    """Interactive setup for OpenAI integration"""
    
    print("🤖 ConvoAI - OpenAI Integration Setup")
    print("=" * 50)
    
    # Check if openai package is installed
    try:
        import openai
        print("✅ OpenAI package is installed")
    except ImportError:
        print("❌ OpenAI package not found")
        print("\nTo install OpenAI package, run:")
        print("pip install openai")
        
        install = input("\nWould you like to install it now? (y/n): ").lower().strip()
        if install in ['y', 'yes']:
            os.system("pip install openai")
            try:
                import openai
                print("✅ OpenAI package installed successfully")
            except ImportError:
                print("❌ Failed to install OpenAI package")
                return False
        else:
            print("⚠️ OpenAI integration will not be available without the package")
            return False
    
    # Get API key
    print("\n🔑 OpenAI API Key Configuration")
    print("-" * 30)
    print("You need an OpenAI API key to use enhanced features.")
    print("Get your key from: https://platform.openai.com/api-keys")
    
    # Check if key already exists
    existing_key = os.getenv('OPENAI_API_KEY')
    if existing_key:
        print(f"✅ Found existing API key in environment: {existing_key[:10]}...")
        use_existing = input("Use existing key? (y/n): ").lower().strip()
        if use_existing in ['y', 'yes']:
            return test_api_key(existing_key)
    
    # Get new key
    api_key = input("\nEnter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    # Test the key
    if test_api_key(api_key):
        # Save to config
        save_api_key(api_key)
        return True
    else:
        return False

def test_api_key(api_key: str) -> bool:
    """Test if the API key is valid"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        print("\n🧪 Testing API key...")
        
        # Simple test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        print("✅ API key is valid and working!")
        print(f"✅ Test response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {str(e)}")
        if "invalid" in str(e).lower():
            print("💡 Please check your API key and try again")
        elif "quota" in str(e).lower():
            print("💡 Your API quota may be exceeded")
        elif "billing" in str(e).lower():
            print("💡 Please check your OpenAI billing settings")
        return False

def save_api_key(api_key: str):
    """Save API key to config file"""
    try:
        # Update config.py
        config_path = Path("config.py")
        if config_path.exists():
            content = config_path.read_text()
            
            # Replace the api_key line
            import re
            pattern = r"'api_key': None"
            replacement = f"'api_key': '{api_key}'"
            
            if pattern in content:
                content = content.replace(pattern, replacement)
                config_path.write_text(content)
                print("✅ API key saved to config.py")
            else:
                print("⚠️ Could not update config.py automatically")
                print(f"💡 Manually set: OPENAI_CONFIG['api_key'] = '{api_key}'")
        
        # Also suggest environment variable
        print(f"\n💡 You can also set environment variable:")
        print(f"export OPENAI_API_KEY='{api_key}'")
        
    except Exception as e:
        print(f"⚠️ Could not save API key: {str(e)}")
        print(f"💡 Manually set: OPENAI_CONFIG['api_key'] = '{api_key}'")

def show_features():
    """Show what OpenAI integration adds"""
    print("\n🚀 Enhanced Features with OpenAI:")
    print("-" * 40)
    print("🧠 Advanced Response Analysis:")
    print("  • Deep psychological insights")
    print("  • Personality pattern detection") 
    print("  • Emotional intelligence assessment")
    print("  • Behavioral analysis")
    
    print("\n💬 Dynamic Question Generation:")
    print("  • Personalized follow-up questions")
    print("  • Context-aware inquiries")
    print("  • Adaptive conversation flow")
    
    print("\n📊 Enhanced Summaries:")
    print("  • Comprehensive session analysis")
    print("  • Actionable recommendations")
    print("  • Growth area identification")
    print("  • Professional-grade insights")
    
    print("\n💡 Cost Information:")
    print("  • GPT-4: ~$0.03-0.06 per analysis")
    print("  • GPT-3.5-turbo: ~$0.002-0.004 per analysis")
    print("  • Typical session: $0.20-0.50 with GPT-4")

def main():
    """Main setup function"""
    show_features()
    
    setup = input("\nWould you like to set up OpenAI integration? (y/n): ").lower().strip()
    if setup not in ['y', 'yes']:
        print("👍 You can run this setup anytime with: python setup_openai.py")
        return
    
    if setup_openai():
        print("\n🎉 OpenAI integration is ready!")
        print("✨ Restart ConvoAI to use enhanced features")
        
        # Test integration
        test_integration = input("\nTest integration now? (y/n): ").lower().strip()
        if test_integration in ['y', 'yes']:
            test_convoai_integration()
    else:
        print("\n❌ Setup failed. You can try again later.")

def test_convoai_integration():
    """Test ConvoAI with OpenAI integration"""
    try:
        from openai_integration import OpenAIAnalyzer
        from config import Config
        
        analyzer = OpenAIAnalyzer()
        if analyzer.enabled:
            print("✅ ConvoAI OpenAI integration is working!")
            
            # Quick test analysis
            test_response = analyzer.analyze_response_advanced(
                "How are you feeling today?",
                "I'm feeling pretty good, though a bit stressed about work deadlines.",
                []
            )
            
            if 'error' not in test_response:
                print("✅ Advanced analysis is working!")
                print("🎯 Sample insight:", test_response.get('psychological_insights', {}).get('emotional_state', 'Analysis complete'))
            else:
                print(f"⚠️ Analysis test failed: {test_response['error']}")
        else:
            print("❌ Integration test failed")
    except Exception as e:
        print(f"❌ Integration test error: {str(e)}")

if __name__ == "__main__":
    main()