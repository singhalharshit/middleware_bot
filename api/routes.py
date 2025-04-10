# # src/api/routes.py
# from fastapi import APIRouter, Depends, HTTPException
# from typing import Dict, Any, Optional
# import json
# import logging
# import asyncio
# from services.chat.gchat_service import GoogleChatService
# from .message_processor import process_message

# logger = logging.getLogger(__name__)
# router = APIRouter()

# @router.post("/webhook")
# async def chat_webhook(
#     event: dict,
#     chat_service: GoogleChatService = Depends(GoogleChatService)
# ):
#     try:
#         # Immediate acknowledgment to prevent "not responding" message
#         response_data = {"text": ""}

#         space_name = event.get("space", {}).get("name")
#         sender_name = event.get("message", {}).get("sender", {}).get("name") if event.get("message") else None
#         message_text = event.get("message", {}).get("text") if event.get("message") else None

#         logger.info(f"Received message: {message_text} from {sender_name} in space {space_name}")

#         # Don't respond to messages from the bot itself
#         if sender_name and "bot" in sender_name.lower():
#             logger.info("Ignoring bot message")
#             return response_data

#         if event.get("type") == "ADDED_TO_SPACE":
#             logger.info("Bot added to space")
#             await chat_service.send_message(
#                 space_name,
#                 "👋 Hello! I'm your Chat Bot. How can I help you today?"
#             )
#             return response_data

#         elif event.get("type") == "MESSAGE" and message_text:
#             # Process message and send response asynchronously
#             bot_response = await process_message(message_text)
#             await chat_service.send_message(space_name, bot_response)
#             return response_data

#         return response_data

#     except Exception as e:
#         logger.error(f"Error in webhook: {str(e)}", exc_info=True)
#         return {"text": "Processing your message..."}  # Fallback response



# # src/api/routes.py
# from fastapi import APIRouter, Depends, HTTPException
# from typing import Dict, Any, Optional
# import json
# import logging
# import asyncio
# from services.chat.gchat_service import GoogleChatService
# from .message_processor import (
#     process_message,
#     create_notification_card,
#     create_picked_up_card
# )

# logger = logging.getLogger(__name__)
# router = APIRouter()

# @router.post("/webhook")
# async def chat_webhook(
#     event: dict,
#     chat_service: GoogleChatService = Depends(GoogleChatService)
# ):
#     try:
#         # Immediate acknowledgment to prevent timeout
#         response_data = {"text": ""}

#         space_name = event.get("space", {}).get("name")
#         message = event.get("message", {})
#         sender = message.get("sender", {})
#         sender_name = sender.get("name") if sender else None
#         sender_display_name = sender.get("displayName") if sender else "Unknown User"
#         message_text = message.get("text") if message else None

#         logger.info(f"Received message: {message_text} from {sender_name} in space {space_name}")

#         # Don't respond to messages from the bot itself
#         if sender_name and "bot" in sender_name.lower():
#             logger.info("Ignoring bot message")
#             return response_data

#         # Handle different event types
#         if event.get("type") == "ADDED_TO_SPACE":
#             logger.info("Bot added to space")
#             await chat_service.send_message(
#                 space_name,
#                 "👋 Hello! I'm your Support Bot. I can help create and manage support tickets. How can I assist you today?"
#             )
#             return response_data

#         elif event.get("type") == "MESSAGE":
#             # Handle button clicks
#             if message.get("actionResponse", {}).get("type") == "DIALOG":
#                 action_data = message.get("actionResponse", {}).get("dialog", {})
#                 action_name = action_data.get("name")
                
#                 if action_name == "pick_ticket":
#                     ticket_id = action_data.get("parameters", {}).get("ticket_id")
                    
#                     # Create DM with the user who clicked
#                     dm_space = await chat_service.create_direct_message(sender_name)
                    
#                     # Update original notification
#                     updated_card = create_picked_up_card(
#                         ticket_id=ticket_id,
#                         user_name=sender_display_name,
#                         original_message=message_text
#                     )
#                     await chat_service.update_card(message.get("name"), updated_card)
                    
#                     # Send welcome message in DM
#                     await chat_service.send_message(
#                         dm_space,
#                         f"You've picked up ticket {ticket_id}. I'll transfer the conversation here.\n\nOriginal message: {message_text}"
#                     )
                    
#                     logger.info(f"Ticket {ticket_id} picked up by {sender_name}")
#                     return response_data

#             # Process regular messages
#             elif message_text:
#                 # Check if it's a DM or group space
#                 is_dm = event.get("space", {}).get("type") == "DM"
                
#                 # Process message
#                 response_text, ticket_id = await process_message(message_text, not is_dm)
                
#                 if ticket_id and not is_dm:
#                     # Create and send notification card for new ticket
#                     notification_card = create_notification_card(
#                         ticket_id=ticket_id,
#                         user_name=sender_display_name,
#                         message=message_text
#                     )
#                     await chat_service.send_card(space_name, notification_card)
                    
#                     # Send acknowledgment to user
#                     await chat_service.send_message(space_name, response_text)
#                     logger.info(f"Created ticket {ticket_id} for user {sender_name}")
#                 else:
#                     # Send regular response
#                     await chat_service.send_message(space_name, response_text)
                
#                 return response_data

#         return response_data

#     except Exception as e:
#         logger.error(f"Error in webhook: {str(e)}", exc_info=True)
#         return {"text": "Processing your message..."}  # Fallback response

# # src/api/routes.py
# from fastapi import APIRouter, Request, Depends
# from services.chat.gchat_service import GoogleChatService
# from api.message_processor import process_chat_event, create_ticket_notification
# import logging

# logger = logging.getLogger(__name__)
# router = APIRouter()

# @router.post("/webhook")
# async def chat_webhook(
#     request: Request,
#     chat_service: GoogleChatService = Depends(GoogleChatService)
# ):
#     try:
#         event = await request.json()
#         space_name = event.get("space", {}).get("name")
#         message = event.get("message", {})
        
#         # Handle button clicks/actions
#         if message.get("actionResponse"):
#             response = process_chat_event(event)
#             if response.get("text"):
#                 await chat_service.send_message(space_name, response["text"])
#             return {"text": ""}

#         # Handle new messages
#         if event.get("type") == "MESSAGE" and message.get("text"):
#             # Create ticket notification
#             ticket_data = {
#                 "issue": message.get("text"),
#                 "user": message.get("sender", {}).get("displayName", "Unknown User")
#             }
            
#             notification = create_ticket_notification(ticket_data)
#             await chat_service.send_card(space_name, notification)
            
#             return {"text": ""}

#         return {"text": ""}

#     except Exception as e:
#         logger.error(f"Error in webhook: {str(e)}", exc_info=True)
#         return {"text": "Processing your message..."}


# # src/api/routes.py
# from fastapi import APIRouter, Request, Depends
# from services.chat.gchat_service import GoogleChatService
# from api.message_processor import process_chat_event, create_ticket_notification
# import logging

# logger = logging.getLogger(__name__)
# router = APIRouter()

# @router.post("/webhook")
# async def chat_webhook(
#     request: Request,
#     chat_service: GoogleChatService = Depends(GoogleChatService)
# ):
#     try:
#         event = await request.json()
#         space_name = event.get("space", {}).get("name")
#         message = event.get("message", {})
        
#         # Handle button clicks/actions
#         if message.get("actionResponse"):
#             # Process the event and get response data
#             response, dm_user, status_card = await process_chat_event(event)
            
#             if dm_user:
#                 # Create DM space with the user
#                 dm_space = await chat_service.create_direct_message(dm_user)
#                 # Send initial message in DM
#                 await chat_service.send_message(dm_space, response["text"])
                
#                 # Update the original card in group chat
#                 if status_card:
#                     await chat_service.update_card(message.get("name"), status_card)
            
#             return {"text": ""}

#         # Handle new messages
#         if event.get("type") == "MESSAGE" and message.get("text"):
#             # Create ticket notification
#             ticket_data = {
#                 "issue": message.get("text"),
#                 "user": message.get("sender", {}).get("displayName", "Unknown User")
#             }
            
#             notification = create_ticket_notification(ticket_data)
#             await chat_service.send_card(space_name, notification)
            
#             return {"text": ""}

#         return {"text": ""}

#     except Exception as e:
#         logger.error(f"Error in webhook: {str(e)}", exc_info=True)
#         return {"text": "Processing your message..."}




# src/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from services.chat.gchat_service import GoogleChatService
from api.message_processor import process_message
from api.models import ChatEvent
from typing import Dict
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def is_bot_message(message) -> bool:
    """Check if message is from a bot"""
    if not message or not message.sender:
        return False
    return (
        message.sender.type == "BOT" or 
        (message.sender.name and "bot" in message.sender.name.lower())
    )

@router.post("/webhook")
async def chat_webhook(
    event: ChatEvent,
    chat_service: GoogleChatService = Depends(GoogleChatService)
) -> Dict[str, str]:
    """Handle incoming webhook events from Google Chat"""
    try:
        # Extract event details
        space_name = event.space.name
        message = event.message

        # Log incoming event
        logger.info(f"Received event type: {event.type} in space: {space_name}")

        # Ignore bot messages
        if is_bot_message(message):
            logger.debug("Ignoring bot message")
            return {"text": ""}

        # Handle different event types
        if event.type == "ADDED_TO_SPACE":
            logger.info(f"Bot added to space: {space_name}")
            await chat_service.send_message(
                space_name,
                "👋 Hello! I'm your Support Bot. How can I assist you today?"
            )
            return {"text": ""}

        elif event.type == "MESSAGE":
            # Handle button clicks
            if message and message.actionResponse:
                logger.info(f"Processing button click in space: {space_name}")
                return await chat_service.handle_chat_event(event)

            # Handle text messages
            elif message and message.text:
                logger.info(f"Processing message: '{message.text[:50]}...' in space: {space_name}")
                
                # Get user details
                user_name = message.sender.displayName if message.sender else "Unknown User"
                
                # Process the message
                response_text, ticket_data = await process_message(message.text, user_name)
                
                # Handle ticket creation
                if ticket_data:
                    logger.info(f"Creating ticket for user: {user_name}")
                    await chat_service.send_card(space_name,chat_service._create_ticket_card( ticket_data["ticket_id"], ticket_data["user"], ticket_data["issue"]))
                
                # Handle regular response
                if response_text:
                    logger.info("Sending regular response")
                    await chat_service.send_message(space_name, response_text)
                
                return {"text": ""}

            else:
                logger.warning(f"Received MESSAGE event without text or action")
                return {"text": ""}

        else:
            logger.warning(f"Unhandled event type: {event.type}")
            return {"text": ""}

    except Exception as e:
        logger.error(
            "Error processing webhook event",
            extra={
                "event_type": event.type,
                "space": event.space.name,
                "error": str(e)
            },
            exc_info=True
        )
        return {"text": "I apologize, but I encountered an error processing your request. Please try again."}