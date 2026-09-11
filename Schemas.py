from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ChatInput(BaseModel):
    query : str
    conversation_id : Optional[UUID] = None

class ChatOutput(BaseModel):
    response : str
    conversation_id : UUID
    