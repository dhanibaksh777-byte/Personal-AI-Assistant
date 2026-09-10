from database import base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from datetime import datetime ,timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid



class Conversation(base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid = True),primary_key = True, default = uuid.uuid4)
    created_at = Column(DateTime,default = datetime.now(timezone.utc))
    messages = relationship("Message",back_populates="conversation")


class Message(base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid = True),primary_key=True,default = uuid.uuid4)
    role = Column(String())
    content = Column(String())
    created_at = Column(DateTime,default= datetime.now(timezone.utc))
    conversation_id = Column(UUID(as_uuid=True,default = uuid.uuid4), ForeignKey("conversations.id"))
    conversation = relationship("Conversation",back_populates="messages")

