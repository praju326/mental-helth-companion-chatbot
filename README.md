# AI-Chat-bot-

Architecture Overview
Front-end: A web page with a chat box. Users type messages, which are sent to the back-end via AJAX.
Back-end: Receives messages, analyzes sentiment, generates responses, logs data (if enabled), and returns replies.
Database: Stores conversation history (e.g., timestamp, sentiment, response) for improvement, but only if opted in.
Security: Basic CORS handling; in production, add authentication, encryption, and rate limiting.
Tools and Technologies
Programming Languages: Python (back-end logic), HTML/CSS (front-end UI).
Frameworks/Libraries:
Flask: Web framework for API and routing.
TextBlob: NLP library for sentiment analysis.
SQLAlchemy: ORM for database management.
Flask-CORS: Handles cross-origin requests.
Testing Tools: Pytest for unit testing.
Deployment Tools: Heroku CLI for cloud hosting.
Other: Git for version control, Notepad++/VS Code for editing.
Architecture
Layered Architecture:
Presentation Layer: HTML/CSS front-end for user interaction (chat interface).
Application Layer: Flask back-end for processing (sentiment analysis, response generation).
Data Layer: SQLite/SQLAlchemy for anonymized conversation logs.
Data Flow:
User Input → Front-End → API (Flask) → Analysis/Response → Database Log → Output.
Design Principles: Modular (separate functions), responsive (mobile-friendly), secure (anonymized data, UTF-8 encoding).
