
*This project is heavily built by Claude with Cursor.*

# English Learning Anki Card Generator

An AI-powered web application that automatically generates comprehensive Anki cards for English language learning. The application creates cards with phonetic transcriptions, usage examples, and relevant illustrations.

## Features

- 🔤 IPA phonetic transcription for American English pronunciation
- 📝 Multiple contextual usage examples
- 🖼️ AI-generated illustrations that represent the expression
- 🌐 Web interface for easy card generation
- 🎯 Focus on natural, conversational English

## Prerequisites

- Python 3.8+
- OpenAI API key

## Usage

1. Start the server:
```
uvicorn main:app --reload
```

2. Open your browser and navigate to:
```
http://127.0.0.1:8000
```

3. Enter an English word or phrase, and the application will generate a card with:
- Phonetic transcription
- Multiple usage examples
- AI-generated illustration

## Project Structure

- `main.py` - FastAPI web application setup and routes
- `english_learning_agent.py` - Core logic for generating Anki cards
- `templates/` - HTML templates for the web interface
- `static/` - Static files (CSS, JavaScript, images)