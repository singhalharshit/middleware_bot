# api/dependencies.py
from services.chat.gchat_service import GoogleChatService

def get_chat_service():
    return GoogleChatService()