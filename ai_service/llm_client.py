from groq import Groq
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from tools.web_searches import web_search
from models import ChatMessage,Conversation
from sqlalchemy.dialects.postgresql import UUID
import uuid

SYSTEM_PROMPT = """You are a helpful personal assistant. You have access to a web search tool. 
Use it when the user asks about current events, real-time information, or anything you are not sure about.
Otherwise answer directly from your knowledge.
Keep responses concise and helpful."""

load_dotenv()

api_key = os.getenv("groq_api_key")
if not api_key:
    raise RuntimeError("groq_api_key does'nt exists check your .env file")
client = Groq(api_key=api_key)
def get_response(message : str,conversation_id : str,db : Session):
    
    if not conversation_id:
        new_conv = Conversation()
        db.add(new_conv)
        db.commit()
        conversation_id = new_conv.id

    save_message = ChatMessage(role = "user", content = message,conversation_id = conversation_id)
    db.add(save_message)
    db.refresh(save_message)
    db.commit()

    history = db.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id).all()


    messages = [{"role" : "system", "content" : SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role" : msg.role, "content" : msg.content})
    messages.append({"role" : "user", "content" : message})

    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages=messages,
        tools=[web_search],
        reasoning_effort="low"
    )

    tool_call = response.choices[0].message.tool_calls
    if tool_call:
        response = web_search(message)
        return response

    else:
        return response.choices[0].message.content

    save_message = Message(role = "user", content = message, conversation_id = conversation_id)
    db.add()
    db.commit()
    return save_message


    



