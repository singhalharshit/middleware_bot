# services/chat/__init__.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseChatService(ABC):
    @abstractmethod
    async def send_message(self, space: str, message: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def create_thread(self, space: str, message: str) -> str:
        pass
    
    @abstractmethod
    async def update_thread(self, thread_name: str, message: str) -> Dict[str, Any]:
        pass