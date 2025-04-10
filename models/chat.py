# models/chat.py
from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatMessage(BaseModel):
    space_name: str
    message_text: str
    sender_name: Optional[str]
    message_id: Optional[str]
    thread_id: Optional[str]

class Card(BaseModel):
    title: str
    subtitle: Optional[str]
    sections: List[Dict]