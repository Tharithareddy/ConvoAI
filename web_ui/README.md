# ConvoAI Web UI

A modern React-based web interface for ConvoAI with real-time conversation analysis.

## Features

- 🎨 **Beautiful UI**: Modern, responsive design with gradient backgrounds and glass effects
- 🧠 **Real-time Analysis**: Instant feedback on sentiment, emotions, and engagement
- 📊 **Comprehensive Analytics**: Detailed insights with charts and visualizations  
- 💬 **Interactive Chat**: Smooth conversation flow with adaptive questions
- 📱 **Mobile Friendly**: Responsive design that works on all devices
- 🔄 **Live Updates**: Real-time progress tracking and analysis updates

## Quick Start

### Prerequisites
- Python 3.7+ (for backend)
- Node.js 14+ (for frontend)

### Setup
1. **Run the setup script**:
   ```bash
   setup.bat
   ```
   This will install all dependencies for both backend and frontend.

2. **Start the servers**:
   - **Backend**: Double-click `start_backend.bat` or run:
     ```bash
     cd backend
     python app.py
     ```
   - **Frontend**: Double-click `start_frontend.bat` or run:
     ```bash
     cd frontend
     npm start
     ```

3. **Open in browser**:
   Navigate to `http://localhost:3000`

## Architecture

### Backend (Flask API)
- **Port**: 5000
- **Endpoints**: RESTful API for conversation management
- **Features**: Session handling, response analysis, data persistence

### Frontend (React)
- **Port**: 3000  
- **Framework**: React 18 with functional components
- **Styling**: Tailwind CSS with custom animations
- **Icons**: Lucide React for beautiful icons

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/session/start` | Start new conversation |
| POST | `/api/session/{id}/respond` | Submit response |
| GET | `/api/session/{id}/summary` | Get analysis summary |
| GET | `/api/session/{id}/analysis/final` | Get final analysis |
| POST | `/api/session/{id}/end` | End conversation |

## Screens & Components

### 1. Welcome Screen
- Introduction to ConvoAI
- Feature highlights
- Getting started guide
- Start conversation button

### 2. Conversation Screen
- Real-time chat interface
- Question cards with category indicators
- Instant analysis feedback
- Progress tracking
- Skip/end options

### 3. Analysis Screen
- Comprehensive results dashboard
- Interactive tabs (Overview, Patterns, Insights, Responses)
- Downloadable analysis reports
- Visualization charts

## Key Features

### Smart Question Flow
- Adaptive question selection based on responses
- Multiple question types (open-ended, multiple choice, ranking)
- Context-aware follow-up questions

### Real-time Analysis
- **Sentiment Analysis**: Positive, negative, neutral detection
- **Emotion Recognition**: Enthusiasm, concern, confidence, etc.
- **Theme Extraction**: Key topics and concepts
- **Engagement Scoring**: Response depth and involvement
- **Complexity Analysis**: Sophistication of responses

### Comprehensive Insights
- Personal communication patterns
- Sentiment trends over time
- Recurring themes and topics
- Personalized recommendations
- Downloadable analysis reports

## Technology Stack

### Frontend
- React 18
- Tailwind CSS
- Lucide React (icons)
- Axios (API calls)
- React Router (navigation)

### Backend
- Flask (API server)
- Flask-CORS (cross-origin support)
- ConvoAI core modules (analysis engine)

## Development

### File Structure
```
web_ui/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   ├── App.js         # Main application
│   │   └── index.js       # Entry point
│   ├── public/            # Static assets
│   └── package.json       # Node dependencies
├── setup.bat              # Automated setup
├── start_backend.bat      # Backend launcher
└── start_frontend.bat     # Frontend launcher
```

### Component Architecture
- **App.js**: Main state management and routing
- **WelcomeScreen**: Landing page and introduction
- **ConversationScreen**: Chat interface and question handling
- **AnalysisScreen**: Results dashboard with tabs
- **Supporting Components**: Cards, loading screens, error handling

### State Management
- Session data (responses, analysis results)
- Current screen routing
- Loading and error states
- Real-time analysis updates

## Customization

### Styling
- Modify `src/index.css` for global styles
- Update Tailwind config in `tailwind.config.js`
- Customize color schemes and animations

### API Configuration  
- Backend URL: `src/services/api.js`
- Timeout settings and error handling
- Additional endpoints

### Features
- Add new question types in backend
- Extend analysis algorithms
- Custom visualization components

## Deployment

### Production Build
```bash
cd frontend
npm run build
```

### Docker (Optional)
Create Dockerfile for containerized deployment

### Cloud Deployment
- Backend: Deploy Flask app to Heroku, AWS, or similar
- Frontend: Deploy to Netlify, Vercel, or serve static files
- Update API URLs in production

## Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure ports 3000 and 5000 are available
2. **CORS errors**: Check Flask-CORS configuration
3. **Dependency errors**: Run setup script again
4. **API connection**: Verify backend is running on port 5000

### Debug Mode
- Backend: Set `debug=True` in `app.py`
- Frontend: Check browser console for errors
- Network tab for API call inspection

## Browser Support
- Chrome 80+
- Firefox 75+ 
- Safari 13+
- Edge 80+

## Performance
- Optimized React rendering
- Efficient API calls with axios
- Responsive design for all screen sizes
- Smooth animations and transitions

---

**Ready to start?** Run `setup.bat` and then open `http://localhost:3000` in your browser! 🚀