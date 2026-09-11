from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from ai_service.llm_client import get_response
from Schemas import ChatInput, ChatOutput

router = APIRouter()

@router.post("/chat", response_model=ChatOutput)
def chat(request: ChatInput, db: Session = Depends(get_db)):
    output = get_response(request.query, request.conversation_id, db)
    return output