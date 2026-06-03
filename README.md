# Multilingual AI Exam Assistant

A Flask based AI assistant that helps students get quick answers to academic questions in multiple languages. The application uses Google's Gemini model for answer generation and ElevenLabs for text to speech functionality.

## Features

* AI powered question answering using Gemini
* Supports multiple languages:

  * English
  * Urdu
  * Arabic
  * Turkish
* Text to Speech (TTS) support using ElevenLabs
* Clean and responsive web interface
* Fast response generation
* Language specific voice selection
* Secure API key management using environment variables

## Tech Stack

### Backend

* Python
* Flask
* Google Generative AI (Gemini)
* ElevenLabs API

### Frontend

* HTML
* CSS
* JavaScript

### Other Libraries

* Requests
* Python Dotenv
* Gunicorn

## Project Structure

```text
Multilingual-AI-Exam-Assistant/
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Hassan-Ahmad007/Multilingual-Ai-exam-assistant.git
cd Multilingual-AI-Exam-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / MacOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

## Running the Application

```bash
python main.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Usage

1. Enter a question in the input field.
2. Select your preferred language.
3. Submit the question.
4. Receive an AI generated answer.
5. Listen to the response using the text to speech feature.

## Supported Languages

| Language | Code |
| -------- | ---- |
| English  | en   |
| Urdu     | ur   |
| Arabic   | ar   |
| Turkish  | tr   |

## Security Improvements

The project uses:

* Environment variables for API keys
* Request size limits
* Input validation
* API timeout handling
* Error handling and logging

## Future Improvements

* Additional language support
* Voice customization
* Conversation history
* User authentication
* Speech to Text support
* Better translation workflow

## Educational Purpose

This project was originally developed as a university project to explore:

* Generative AI integration
* Natural Language Processing
* Flask web development
* API integration
* Multilingual applications

## License

This project is intended for educational and learning purposes.

## Author

Hassan

Computer Science Student
