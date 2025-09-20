# 🤖 Chatbot Backend

A backend service for a chatbot application built with **FastAPI** and **MongoDB**, using **Ollama** for local language model integration. This backend streams real-time AI responses to the frontend via **WebSocket** and stores user data and conversation history in MongoDB.

## 🛠️ Tech Stack
- ⚡ **FastAPI**: High-performance web framework for building APIs
- 🗄️ **MongoDB**: NoSQL database for storing conversations and user data
- 🧠 **Ollama**: For running language models locally
- 🔄 **WebSocket**: For real-time streaming responses to the frontend

## 📋 Prerequisites
- 🐍 Python 3.8+
- 🗄️ MongoDB installed and running
- 🧠 Ollama installed (for local LLM support)

## 🚀 Installation
1. **📂 Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/chatbot-be.git

   cd chatbot-be
   ```

2. **🌐 Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **⚙️ Activate the virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

4. **📦 Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **🔧 Set up environment variables**: Create a `.env` file in the root directory with the following variables:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DB=chatbot
   OLLAMA_API_URL=http://localhost:11434/api
   ```

## ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once the application is running, you can access:

- 📘 **Interactive API documentation**: `http://localhost:8000/docs`
- 📕 **Alternative API documentation**: `http://localhost:8000/redoc`

## 🗂️ Project Structure
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

## ✨ Features
- 💬 Chat conversation management
- 🧠 Integration with Ollama for text generation
- 🗄️ Conversation history storage in MongoDB
- 👤 User management
- 🔄 Real-time response streaming via WebSocket

## 🖼️ Frontend Repository
The frontend for this project is available at: [🌐 Chatbot Frontend](https://github.com/NguyenNguyen0/chatbot-fe)

## 📜 License
📄 MIT License