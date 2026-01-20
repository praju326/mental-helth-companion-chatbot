from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for front-end requests

# Database setup (SQLite for simplicity)
engine = create_engine('sqlite:///chatbot.db')
Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_input = Column(Text)
    sentiment = Column(String)
    response = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Crisis keywords
CRISIS_KEYWORDS = ["suicide", "kill myself", "end it all", "harm myself", "hopeless"]

# Responses and tips
RESPONSES = {
    "positive": [
        "That's great to hear! Keep up the positive momentum. Remember, small wins add up.",
        "I'm glad you're feeling good. What's one thing that made your day better?"
    ],
    "neutral": [
        "It sounds like you're in a balanced place. How can I support you today?",
        "Okay, let's chat. What's on your mind?"
    ],
    "negative": [
        "I'm sorry you're feeling this way—it's okay to have tough days. You're not alone.",
        "That sounds challenging. Let's take a deep breath: Inhale for 4, hold for 4, exhale for 4. How does that feel?",
        "Stress and anxiety are common, but you're taking a step by reaching out. What's one small thing bothering you?"
    ]
}

RELAXATION_TIPS = [
    "Try the 4-7-8 breathing technique: Inhale for 4 seconds, hold for 7, exhale for 8.",
    "Go for a short walk outside—fresh air can help clear your mind.",
    "Journal your thoughts for 5 minutes to process emotions.",
    "Listen to calming music or a guided meditation app like Calm."
]

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def detect_crisis(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in CRISIS_KEYWORDS)

def generate_response(user_input):
    if detect_crisis(user_input):
        return "I'm really concerned about what you're saying. Please reach out to a professional immediately—call 988 (US) or a local hotline. You're not alone, and help is available."
    
    sentiment = analyze_sentiment(user_input)
    response = random.choice(RESPONSES[sentiment])
    
    if sentiment in ["negative", "neutral"]:
        tip = random.choice(RELAXATION_TIPS)
        response += f" As a tip: {tip}"
    
    return response, sentiment

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'response': 'Please share something so I can help.'})
    
    response, sentiment = generate_response(user_input)
    
    # Log to database (anonymized)
    session = Session()
    new_conv = Conversation(user_input=user_input, sentiment=sentiment, response=response)
    session.add(new_conv)
    session.commit()
    session.close()
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)