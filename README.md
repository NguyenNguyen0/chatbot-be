# Chatbot Backend

A backend service for a chatbot application built with FastAPI and MongoDB, using Ollama for language model integration.

## Tech Stack
- FastAPI: High-performance web framework for building APIs
- MongoDB: NoSQL database for storing conversations and user data
- Ollama: For running language models locally
## Prerequisites
- Python 3.8+
- MongoDB installed and running
- Ollama installed (for local LLM support)
## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/chatbot-be.git

cd chatbot-be
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables: Create a .env file in the root directory with the following variables:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=chatbot
OLLAMA_API_URL=http://localhost:11434/api
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- Interactive API documentation: `http://localhost:8000/docs\`
- Alternative API documentation: `http://localhost:8000/redoc`
 
## Project Structure
  ```
    chatbot-be/
    ├── app/
    │   ├── api/           # API routes
    │   ├── core/          # Core functionality, config
    │   ├── db/            # Database models and connections
    │   ├── models/        # Pydantic models
    │   ├── services/      # Business logic
    │   └── main.py        # Application entry point
    ├── tests/             # Test files
    ├── .env               # Environment variables
    ├── .gitignore
    ├── requirements.txt
    └── README.md
  ```
## Features
- Chat conversation management
- Integration with Ollama for text generation
- Conversation history storage
- User management

## License
MIT License