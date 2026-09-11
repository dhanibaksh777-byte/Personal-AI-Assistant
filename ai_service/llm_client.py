from groq import Groq
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from tools.web_searches import web_search,web_search_tool
from models import ChatMessage,Conversation
from sqlalchemy.dialects.postgresql import UUID
import json
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
    db.commit()
    db.refresh(save_message)

    history = db.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id).all()


    messages = [{"role" : "system", "content" : SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role" : msg.role, "content" : msg.content})

    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages=messages,
        tools=[web_search_tool],
        reasoning_effort="low"
    )

    while response.choices[0].message.tool_calls:
        msg = response.choices[0].message
        messages.append(msg)

        tool_call = msg.tool_calls[0]
        argument = json.loads(tool_call.function.arguments)
        search_result = web_search(argument["query"])

        messages.append({
            "role" : "tool",
            "content" : str(search_result),
            "tool_call_id" : tool_call.id,
            "name" : tool_call.function.name
        })

        response = client.chat.completions.create(
            model = "openai/gpt-oss-120b",
            messages=messages,
            tools = [web_search_tool]
        )
    assistant_reply = response.choices[0].message.content
    if not assistant_reply:
            assistant_reply = "I completed the search, but couldn't generate a text response"
    save_assistant_message = ChatMessage(
            role = "assistant",
            content = assistant_reply,
            conversation_id = conversation_id
            )
    db.add(save_assistant_message)
    db.commit()

    return {
        "response" : assistant_reply,
        "conversation_id" : str(conversation_id)

    }