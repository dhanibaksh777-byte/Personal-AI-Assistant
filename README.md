# AI Personal Assistant

A conversational AI assistant with real-time web search and persistent memory — built with FastAPI, Groq, and Tavily.

## Live Demo

Frontend: https://ai-ui-rouge.vercel.app/  
Backend: https://personal-ai-assistant-q5cp.onrender.com/

## Screenshot

![AI Personal Assistant](https://github.com/dhanibaksh777-byte/Personal-AI-Assistant/blob/c339bf9973c66b149d0b3113ea14a00d1ea01c23/Screenshot%202026-09-12%20164110.png?raw=true)

## Features

- Conversation Memory — context preserved across messages using PostgreSQL
- Real-time Web Search — Tavily API for up-to-date information
- Function Calling — Groq decides when to search vs answer directly
- Multi-conversation support — start new chats, history preserved

## Tech Stack

- **Backend:** FastAPI
- **LLM:** Groq (openai/gpt-oss-120b)
- **Web Search:** Tavily API
- **Database:** PostgreSQL + Neon.tech
- **Migrations:** Alembic
- **Deployment:** Render (backend) + Vercel (frontend)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a message, get AI response |

## Request / Response

```json
// Request
{
  "query": "what is the latest news?",
  "conversation_id": null
}

// Response
{
  "response": "Here are today's headlines...",
  "conversation_id": "uuid"
}
```

## Setup

```bash
git clone https://github.com/dhanibaksh777-byte/Personal-AI-Assistant
cd Personal-AI-Assistant
pip install -r requirements.txt
```

Add `.env`:
