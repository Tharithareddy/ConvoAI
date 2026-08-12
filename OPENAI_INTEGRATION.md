# 🤖 OpenAI Integration for ConvoAI

Transform your ConvoAI experience with advanced AI-powered analysis and dynamic conversations!

## 🌟 What OpenAI Integration Adds

### 🧠 Advanced Analysis
- **Deep psychological insights** instead of basic keyword matching
- **Personality pattern detection** across conversation sessions  
- **Emotional intelligence assessment** with professional-grade accuracy
- **Behavioral analysis** that understands context and nuance

### 💬 Dynamic Conversations
- **Personalized follow-up questions** based on your specific responses
- **Context-aware inquiries** that build on previous conversations
- **Adaptive conversation flow** that adjusts to your communication style

### 📊 Professional Insights  
- **Comprehensive session summaries** with actionable recommendations
- **Growth area identification** with specific steps for improvement
- **Professional-grade analysis** comparable to coaching sessions

## 🚀 Quick Setup

### 1. Install OpenAI Package
```bash
pip install openai
```

### 2. Get Your API Key
- Visit [OpenAI Platform](https://platform.openai.com/api-keys)
- Create a new API key
- Keep it secure!

### 3. Configure ConvoAI
```bash
# Run the setup script
python setup_openai.py

# Or set environment variable
export OPENAI_API_KEY="your-key-here"

# Or edit config.py directly
OPENAI_CONFIG['api_key'] = 'your-key-here'
```

### 4. Test Integration
```bash
python demo_openai.py
```

## 💡 Usage Examples

### Basic Usage with API Key
```python
from main import ConvoAI

# Initialize with OpenAI
convo = ConvoAI(openai_api_key="your-key-here")
convo.start_conversation()
```

### Advanced Analysis
```python
from openai_integration import OpenAIAnalyzer

analyzer = OpenAIAnalyzer("your-key-here")
analysis = analyzer.analyze_response_advanced(
    question="How do you handle stress?",
    response="I usually go for walks and listen to music...",
    context=[]  # Previous conversation context
)

print(analysis['psychological_insights'])
```

### Generate Follow-up Questions
```python
follow_up = analyzer.generate_follow_up_question(
    conversation_history=[...],  # Your conversation history
)

print(follow_up['question']['text'])
```

## 💰 Cost Information

| Model | Cost per Analysis | Typical Session |
|-------|------------------|-----------------|
| GPT-4 | $0.03-0.06 | $0.30-0.60 |
| GPT-3.5-turbo | $0.002-0.004 | $0.02-0.06 |

**Tips to minimize costs:**
- Use GPT-3.5-turbo for basic analysis (set in config)
- Set `cost_limit_per_session` in config  
- Enable cost tracking in your OpenAI dashboard

## 🔧 Configuration Options

Edit `config.py`:

```python
OPENAI_CONFIG = {
    'api_key': 'your-key-here',
    'model': 'gpt-4',  # or 'gpt-3.5-turbo'
    'max_tokens': 1500,
    'temperature': 0.3,  # Lower = more consistent
    'enable_advanced_analysis': True,
    'enable_dynamic_questions': True,
    'enable_conversation_summary': True,
    'cost_limit_per_session': 1.00,  # USD
}
```

## 🌐 Web UI Integration

The OpenAI features work automatically in the web interface:

1. Start backend: `python web_ui/backend/app.py`
2. Start frontend: `cd web_ui/frontend && npm start`
3. Enhanced analysis appears automatically when available

## 🔒 Security Best Practices

- **Never commit API keys** to version control
- Use **environment variables** for production
- Set **usage limits** in your OpenAI dashboard
- **Monitor costs** regularly
- **Rotate keys** periodically

## 🆘 Troubleshooting

### "OpenAI integration not available"
```bash
pip install openai
```

### "API key test failed"
- Check your API key is correct
- Verify billing is set up in OpenAI dashboard
- Check usage limits haven't been exceeded

### "Analysis failed" 
- Check internet connection
- Verify API key has sufficient credits
- Try with GPT-3.5-turbo for lower costs

### High costs
- Switch to GPT-3.5-turbo in config
- Reduce `max_tokens` setting
- Set `cost_limit_per_session`

## 🎯 Example Output

**Basic Analysis:**
```
Sentiment: Positive (0.7)
Themes: stress, work, coping
```

**OpenAI Analysis:**
```
🧠 Psychological Insights:
- Emotional State: Cautiously optimistic with underlying stress (confidence: 0.85)
- Cognitive Patterns: Problem-solving oriented, self-aware, seeks balance
- Growth Areas: Stress management, boundary setting, self-care routines

🎯 Recommendations:
- Practice mindfulness techniques during high-stress periods
- Establish clear work-life boundaries
- Consider stress management resources or professional support

💬 Suggested Follow-up:
"You mentioned seeking balance - what does an ideal balanced day look like for you?"
```

## 🤝 Support

- **Issues**: Open GitHub issues for bugs
- **Questions**: Check existing documentation  
- **Feature Requests**: Create feature request issues
- **API Problems**: Check OpenAI status page

---

**Ready to unlock the full potential of conversational AI?** 🚀

Run `python setup_openai.py` to get started!