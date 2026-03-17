## Adaptive AI Chatbot

![Python](https://img.shields.io/badge/Python-3.x-blue)
![NLP](https://img.shields.io/badge/NLP-Sentiment%20Analysis-green)
![Chatbot](https://img.shields.io/badge/AI-Chatbot-orange)

A conversational AI chatbot built with Python and NLP techniques including language detection and sentiment analysis.  
The bot dynamically adapts responses based on user sentiment and preferences.

Tech stack: Python, NLP (NLTK), Bot Framework, Flask

1. Project Overview

This project started as a simple “echo bot” that I built earlier in the semester to learn how basic message handling works. Later, I decided to improve that simple version and turn it into a smarter chatbot using AI features.

In this version, the bot not only repeats or replies but also detects the user’s language, analyzes their sentiment, and adapts its responses based on the user’s preferences and emotional tone. The goal was to make the chatbot feel more natural and human-like — something that reacts differently when the user sounds positive, frustrated, or neutral.

Even though it’s still a basic-level project, it shows how small AI components can make a simple chatbot more intelligent and user-friendly.

2. Features

- Language Detection: Supports both English and Turkish.

- Sentiment Analysis: Detects if a message is positive, negative, or neutral.

- Adaptive Responses: Bot changes its tone or length depending on mood or commands.

- User Preferences: Users can set preferences with simple commands like:

  /short → shorter replies

  /casual → more friendly tone

  /reset → restore default settings

- Clean Interaction Flow: Replies are generated smoothly with context-aware behavior.

3. Technologies Used

Python 3.13

BotBuilder SDK for Python

NLTK (VADER Sentiment Analyzer)

Flask for local server setup

Bot Framework Emulator for testing

4. File Structure

02.echo-bot/
│
├── bots/
│   ├── __init__.py
│   ├── echo_bot.py        # Main bot logic (language, sentiment, preferences)
│
├── analyzer.py            # Language and sentiment analyzer
├── intents.py             # Intent recognition (simple keywords)
├── services.py            # Response service for intents
├── app.py                 # Flask entry point for running the bot
├── config.py              # Configuration file
├── .env.example           # Environment variable example
├── .gitignore             # Hidden files and cache ignore setup
├── requirements.txt       # All dependencies
└── README.md              # Project documentation

5. How to Run

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the bot:

python app.py


Open Bot Framework Emulator:

Connect to http://localhost:3978/api/messages

Chat with your bot!

6. How It Works (Short Summary)

When a user sends a message, the bot first detects the language (English or Turkish), then performs a sentiment analysis (positive, neutral, or negative). Based on that result and the user’s preference commands, it selects the right tone and reply.

For example:

If the user says something negative like “It’s not working”, the bot responds in a calm, supportive way.

If the user says something positive, it reacts more cheerfully.

If the user types /short or /casual, it changes its reply style immediately.

7. Testing & Examples

The project was tested using the Bot Framework Emulator.
Each feature was verified with screenshots, including:

Language detection (Figure 1–2)

Sentiment-based responses (Figure 3–4)

Preference handling and reset behavior (Figure 5–6)

Through the tests, the bot correctly switched between languages, adapted to user tone, and restored defaults after a reset command.

8. Future Improvements

Add a simple GUI or web interface for better visuals

Store user preferences in a small database

Add support for more languages and advanced NLP models

9. License / Note

This project was created for academic purposes as part of a hands-on exercise to explore Adaptive User Interfaces (AUI) and Intelligent User Interaction concepts using Python.
