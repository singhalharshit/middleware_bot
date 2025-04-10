# # src/api/message_processor.py
# import asyncio
# import logging

# logger = logging.getLogger(__name__)

# async def process_message(message: str) -> str:
#     """
#     Process incoming messages and generate appropriate responses.
#     Includes a natural delay and context-aware responses.
#     """
#     try:
#         # Add a small delay to make responses feel more natural
#         await asyncio.sleep(0.8)
        
#         # Convert message to lowercase for easier matching
#         message = message.lower().strip()
        
#         # Basic message handling patterns
#         if any(greeting in message for greeting in ["hello", "hi", "hey", "howdy"]):
#             return "Hello! 👋 How can I assist you today?"
            
#         elif "help" in message:
#             return """I'm here to help! I can assist you with:
# - General inquiries
# - Support requests
# - Information lookup
# What would you like to know?"""
            
#         elif any(word in message for word in ["bye", "goodbye", "see you"]):
#             return "Goodbye! Have a great day! 👋"
            
#         elif "thank" in message:
#             return "You're welcome! 😊 Let me know if you need anything else!"
            
#         elif any(word in message for word in ["how are you", "how're you"]):
#             return "I'm doing well, thank you for asking! How can I help you today?"
            
#         else:
#             return f"I received your message about '{message}'\nHow can I help you with that?"

#     except Exception as e:
#         logger.error(f"Error processing message: {str(e)}", exc_info=True)
#         return "I apologize, but I'm having trouble processing your message. Could you please try again?"



# # src/api/message_processor.py
# import logging
# from datetime import datetime
# from typing import Dict, Optional

# logger = logging.getLogger(__name__)

# def create_ticket_id() -> str:
#     """Generate a unique ticket ID"""
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     return f"TKT-{timestamp}"

# def create_ticket_notification(data: Dict) -> Dict:
#     """Create a notification card for new tickets"""
#     ticket_id = create_ticket_id()
    
#     return {
#         "cardsV2": [
#             {
#                 "cardId": ticket_id,
#                 "card": {
#                     "header": {
#                         "title": f"New Ticket Created: {ticket_id}",
#                         "subtitle": f"From: {data['user']}"
#                     },
#                     "sections": [
#                         {
#                             "widgets": [
#                                 {
#                                     "decoratedText": {
#                                         "text": f"Issue: {data['issue']}",
#                                         "wrapText": True
#                                     }
#                                 },
#                                 {
#                                     "buttonList": {
#                                         "buttons": [
#                                             {
#                                                 "text": "Pick this ticket",
#                                                 "onClick": {
#                                                     "action": {
#                                                         "function": "pick_ticket",
#                                                         "parameters": [
#                                                             {
#                                                                 "key": "ticket_id",
#                                                                 "value": ticket_id
#                                                             }
#                                                         ]
#                                                     }
#                                                 }
#                                             }
#                                         ]
#                                     }
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             }
#         ]
#     }

# def process_chat_event(event: Dict) -> Dict:
#     """Process incoming chat events"""
#     try:
#         action = event.get("message", {}).get("actionResponse", {}).get("action", {})
#         if action.get("function") == "pick_ticket":
#             ticket_id = None
#             for param in action.get("parameters", []):
#                 if param.get("key") == "ticket_id":
#                     ticket_id = param.get("value")
#                     break
                    
#             if ticket_id:
#                 user = event.get("user", {}).get("displayName", "Unknown User")
#                 return {
#                     "text": f"🎫 {user} has picked up ticket {ticket_id}. Start chatting in the support bot thread."
#                 }
        
#         return {"text": "Unhandled event"}
        
#     except Exception as e:
#         logger.error(f"Error processing chat event: {str(e)}", exc_info=True)
#         return {"text": "Error processing action"}




# src/api/message_processor.py
import asyncio
import logging
from datetime import datetime
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)

def create_ticket_id() -> str:
    """Generate a unique ticket ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"TKT-{timestamp}"

async def process_message(message: str, user_name: str = "Unknown User") -> Tuple[Optional[str], Optional[Dict]]:
    """
    Process incoming messages and generate appropriate responses.
    Returns: (text_response, ticket_data)
    """
    try:
        # Add a small delay to make responses feel more natural
        await asyncio.sleep(0.5)
        
        message_lower = message.lower().strip()
        
        # Basic message handling patterns
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "howdy"]):
            return "I can assist you with:\n• Creating support tickets\n• Handling inquiries\n• Getting assistance\nWhat would you like help with?", None
            
        elif "help" in message_lower and len(message_lower) <= 5:
            return "I can assist you with:\n• Creating support tickets\n• Handling inquiries\n• Getting assistance\nWhat would you like help with?", None
            
        else:
            # For non-basic messages, return ticket info
            ticket_id = create_ticket_id()
            ticket_data = {
                "ticket_id": ticket_id,
                "user": user_name,
                "issue": message
            }
            return None, ticket_data

    except Exception as e:
        logger.exception("Error processing message")  # `exception()` auto-captures traceback
        return "I apologize, but I'm having trouble processing your message. Could you please try again?", None