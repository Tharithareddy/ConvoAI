# ConvoAI Setup Guide

## Quick Start (Recommended)

### Option 1: Double-click to Run
1. Double-click `start_convoai.bat` 
2. The batch file will check for Python and launch the application
3. If Python is missing, it will show installation instructions

### Option 2: Command Line
1. Open Command Prompt or PowerShell
2. Navigate to the ConvoAI folder:
   ```
   cd "C:\Users\[YourUsername]\Desktop\Haru\ConvoAI"
   ```
3. Run the application:
   ```
   python main.py
   ```

## Prerequisites

### Python Installation
- **Minimum Version**: Python 3.7 or higher
- **Download**: https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation

### Verify Python Installation
Open Command Prompt and run:
```
python --version
```
You should see something like: `Python 3.9.7`

## Testing the Installation

Before running the full application, test that everything works:

```
python test_components.py
```

This will verify all components are working correctly.

## First Time Usage

1. **Run the application**: `python main.py` or double-click `start_convoai.bat`
2. **Read the welcome message** - it explains how ConvoAI works
3. **Answer questions honestly** - there are no right or wrong answers
4. **Use commands when needed**:
   - Type `help` for assistance
   - Type `summary` to see your current analysis
   - Type `quit` to end the conversation

## Demo Mode

To see ConvoAI's features without interactive conversation:
```
python demo.py
```

## File Structure

```
ConvoAI/
├── main.py                 # Main application
├── conversation_engine.py  # Manages question flow
├── question_database.py    # Predefined questions
├── response_analyzer.py    # Analyzes your responses
├── ui_handler.py          # User interface
├── config.py              # Configuration settings
├── demo.py                # Feature demonstration
├── test_components.py     # Component testing
├── start_convoai.bat      # Windows launcher
├── requirements.txt       # Dependencies (optional)
└── README.md              # Documentation
```

## Troubleshooting

### Python Not Found
- **Windows**: Install Python from python.org, ensure "Add to PATH" is checked
- **Error Message**: "Python was not found"
- **Solution**: Reinstall Python with PATH option enabled

### Import Errors
- **Cause**: Missing or corrupted Python files
- **Solution**: Re-download ConvoAI files, ensure all .py files are present

### Permission Errors
- **Cause**: Insufficient file permissions
- **Solution**: Run Command Prompt as Administrator

### Session Files
- **Location**: Same folder as main.py
- **Format**: `session_YYYYMMDD_HHMMSS.json`
- **Purpose**: Stores your conversation data for review

## Configuration

Edit `config.py` to customize:
- Maximum questions per session
- Analysis sensitivity
- UI appearance
- File saving options

## Advanced Usage

### Adding Custom Questions
```python
from question_database import QuestionDatabase

db = QuestionDatabase()
custom_question = {
    'text': 'Your custom question here?',
    'category': 'custom',
    'type': 'open_ended',
    'keywords': ['custom', 'question'],
    'follow_up_questions': []
}
db.add_question(custom_question)
```

### Analyzing Previous Sessions
Session files are saved as JSON and can be loaded for further analysis.

## Privacy & Security

- ✅ **Local Processing**: All analysis happens on your computer
- ✅ **No Internet Required**: Works completely offline
- ✅ **Data Control**: You own all conversation data
- ✅ **No Tracking**: No data sent to external servers

## Support

If you encounter issues:

1. **Test Components**: Run `python test_components.py`
2. **Check Python**: Verify Python 3.7+ is installed
3. **File Permissions**: Ensure you can read/write in the folder
4. **Read Error Messages**: They usually indicate the specific problem

## Getting the Most Out of ConvoAI

### Tips for Better Analysis
- **Be Detailed**: Longer responses provide richer analysis
- **Be Honest**: Authentic responses lead to better insights
- **Use Examples**: Specific examples help identify patterns
- **Take Your Time**: Thoughtful responses yield better results

### Understanding Your Results
- **Sentiment**: Overall emotional tone of your responses
- **Engagement**: How detailed and involved your answers are
- **Themes**: Key topics and concepts you discuss
- **Patterns**: Recurring elements across your responses

### Session Management
- Sessions are automatically saved with timestamps
- You can review previous sessions by opening the JSON files
- Each session is independent - start fresh anytime

---

**Ready to start? Run `python main.py` or double-click `start_convoai.bat`!** 🤖