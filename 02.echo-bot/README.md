# Adaptive AI Chatbot

![Python](https://img.shields.io/badge/Python-3.x-blue)
![NLP](https://img.shields.io/badge/NLP-Sentiment%20Analysis-green)
![Chatbot](https://img.shields.io/badge/AI-Chatbot-orange)

A Python-based conversational AI chatbot that adapts responses based on user language, sentiment, and preferences.

This project demonstrates how core NLP techniques can be applied to build more natural and adaptive user interactions.

---

## Overview

This project started as a simple echo bot and was later enhanced with AI-driven features such as sentiment analysis and language detection. The chatbot dynamically adjusts its tone and response style based on user input, making interactions more human-like and context-aware.

---

## Features

- Language detection (English & Turkish)
- Sentiment analysis (positive, negative, neutral)
- Adaptive response generation based on user mood
- User preference handling (/short, /casual, /reset)
- Context-aware conversational flow

---

## Tech Stack

Python  
Flask  
NLTK (VADER Sentiment Analysis)  
Microsoft Bot Framework  

---

## How It Works

Each user message is processed in three steps: language detection, sentiment analysis, and adaptive response generation based on sentiment and user preferences.

---

## Project Structure

bots/  
echo_bot.py  

analyzer.py  
intents.py  
services.py  
app.py  
config.py  
requirements.txt  

---

## How to Run

python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
python app.py  

Bot Framework Emulator üzerinden şu endpoint ile bağlanabilirsiniz:  
http://localhost:3978/api/messages

---

## Project Context

This project reflects hands-on experience in building NLP-based conversational systems and designing structured interaction logic for real-world AI applications.

---

## Future Improvements

- Persistent user preference storage  
- Multi-language expansion  
- Integration with advanced LLM models  
- Web-based interface  
