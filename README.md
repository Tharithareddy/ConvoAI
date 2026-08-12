# ConvoAI - Conversational AI Application

ConvoAI is a Python-based conversational AI that asks predefined questions and analyzes your responses to provide insights about your thinking patterns, values, and perspectives.

## Features

- **Intelligent Question Flow**: Adaptive conversation that adjusts based on your responses
- **Response Analysis**: Analyzes sentiment, emotions, themes, and engagement levels
- **Personalized Insights**: Provides customized feedback and recommendations
- **Multiple Question Types**: Open-ended, multiple choice, and ranking questions
- **Session Tracking**: Saves conversation data for future reference
- **Interactive Interface**: Clean, colorful console interface with helpful commands

## Quick Start

1. Make sure you have Python 3.7+ installed
2. Navigate to the ConvoAI directory
3. Run the application:
   ```
   python main.py
   ```

## How It Works

1. **Welcome & Setup**: The AI introduces itself and explains how the conversation works
2. **Question Flow**: You'll be asked thoughtful questions from different categories:
   - Personal goals and aspirations
   - Problem-solving approaches  
   - Values and beliefs
   - Learning preferences
   - Self-reflection
   - Future planning

3. **Response Analysis**: Each response is analyzed for:
   - Sentiment (positive, negative, neutral)
   - Emotional indicators
   - Key themes and topics
   - Engagement level
   - Complexity of thought

4. **Adaptive Conversation**: The AI adjusts future questions based on your response patterns
5. **Final Report**: At the end, you receive comprehensive insights and personalized recommendations

## Commands

During the conversation, you can use these commands:
- `help` - Show help information
- `summary` - Get current analysis summary
- `quit`, `exit`, or `stop` - End conversation

## Question Categories

- **Personal**: Goals, motivations, and aspirations
- **Problem Solving**: Decision-making and adaptability
- **Values**: Core beliefs and relationship priorities  
- **Learning**: How you prefer to acquire new skills
- **Reflection**: Self-awareness and growth
- **Future**: Long-term planning and vision

## File Structure

- `main.py` - Main application entry point
- `conversation_engine.py` - Manages conversation flow and question selection
- `question_database.py` - Predefined questions and management
- `response_analyzer.py` - Response analysis and insight generation
- `ui_handler.py` - User interface and display formatting

## Sample Questions

- "What are your main goals for this year?"
- "When facing a difficult decision, what factors do you consider most important?"
- "How do you handle stress and pressure in challenging situations?"
- "What values are most important to you in your relationships?"
- "Where do you see yourself in 5 years, and what steps are you taking to get there?"

## Privacy & Data

- All analysis is performed locally on your machine
- Session data is saved to local JSON files
- No data is sent to external servers
- You control all conversation data

## Example Session Flow

```
🤖 Welcome to ConvoAI! 🤖

Question: What are your main goals for this year?
> I want to learn new programming skills and improve my health

💡 Quick Analysis:
  Sentiment: Positive (confident)  
  Engagement: High (12 words)
  Key themes: learn, programming, health
  Emotions detected: motivation

Would you like to continue? (y/n): y

Question: What challenges do you anticipate in achieving these goals?
> Finding time to balance learning with work responsibilities...
```

## Customization

You can extend ConvoAI by:
- Adding new questions to the database
- Modifying analysis algorithms
- Customizing the UI appearance
- Adding new question categories
- Implementing additional analysis metrics

## Requirements

- Python 3.7 or higher
- No external dependencies required (uses only built-in Python modules)

## Getting Started

Simply run `python main.py` and start having a thoughtful conversation with your AI! 

The application will guide you through the process and provide insights based on your responses. Each session is unique and adapts to your communication style and interests.

---

*ConvoAI - Understanding yourself through conversation* 🤖✨