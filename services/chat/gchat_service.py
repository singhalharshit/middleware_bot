# # src/services/chat/gchat_service.py
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from typing import Dict, Any
# import asyncio
# import json
# import logging
# import os
# from dotenv import load_dotenv

# logger = logging.getLogger(__name__)

# class GoogleChatService:
#     def __init__(self):
#         load_dotenv()
#         self.credentials = self._get_credentials()
#         self.service = build('chat', 'v1', credentials=self.credentials)

#     def _get_credentials(self) -> service_account.Credentials:
#         """Initialize Google service account credentials"""
#         credentials_dict = {
#             "type": "service_account",
#             "project_id": os.getenv("GOOGLE_PROJECT_ID"),
#             "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
#             "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
#             "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
#         }

#         try:
#             credentials = service_account.Credentials.from_service_account_info(
#                 credentials_dict,
#                 scopes=['https://www.googleapis.com/auth/chat.bot']
#             )
#             return credentials
#         except Exception as e:
#             logger.error(f"Error initializing credentials: {str(e)}", exc_info=True)
#             raise

#     async def send_message(self, space: str, message: str) -> Dict[str, Any]:
#         """Send a message to Google Chat space asynchronously"""
#         try:
#             request = self.service.spaces().messages().create(
#                 parent=space,
#                 body={"text": message}
#             )
            
#             loop = asyncio.get_event_loop()
#             response = await loop.run_in_executor(None, request.execute)
            
#             logger.info(f"Message sent to space {space}")
#             return response

#         except Exception as e:
#             logger.error(f"Error sending message: {str(e)}", exc_info=True)
#             raise


# # src/services/chat/gchat_service.py
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from typing import Dict, Any
# import asyncio
# import logging
# import os
# from dotenv import load_dotenv

# logger = logging.getLogger(__name__)

# class GoogleChatService:
#     def __init__(self):
#         load_dotenv()
#         self.credentials = self._get_credentials()
#         self.service = build('chat', 'v1', credentials=self.credentials)

#     def _get_credentials(self) -> service_account.Credentials:
#         """Initialize Google service account credentials"""
#         credentials_dict = {
#             "type": "service_account",
#             "project_id": os.getenv("GOOGLE_PROJECT_ID"),
#             "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
#             "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
#             "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
#         }

#         try:
#             credentials = service_account.Credentials.from_service_account_info(
#                 credentials_dict,
#                 scopes=['https://www.googleapis.com/auth/chat.bot']
#             )
#             return credentials
#         except Exception as e:
#             logger.error(f"Error initializing credentials: {str(e)}", exc_info=True)
#             raise

#     async def send_message(self, space: str, message: str) -> Dict[str, Any]:
#         """Send a text message to Google Chat space"""
#         try:
#             request = self.service.spaces().messages().create(
#                 parent=space,
#                 body={"text": message}
#             )
            
#             loop = asyncio.get_event_loop()
#             response = await loop.run_in_executor(None, request.execute)
            
#             logger.info(f"Message sent to space {space}")
#             return response

#         except Exception as e:
#             logger.error(f"Error sending message: {str(e)}", exc_info=True)
#             raise

#     async def send_card(self, space: str, card: Dict) -> Dict[str, Any]:
#         """Send an interactive card to Google Chat space"""
#         try:
#             request = self.service.spaces().messages().create(
#                 parent=space,
#                 body=card
#             )
            
#             loop = asyncio.get_event_loop()
#             response = await loop.run_in_executor(None, request.execute)
            
#             logger.info(f"Card sent to space {space}")
#             return response

#         except Exception as e:
#             logger.error(f"Error sending card: {str(e)}", exc_info=True)
#             raise





# src/services/chat/gchat_service.py
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Dict, Any, Optional
import asyncio
import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Constants for response messages
WELCOME_MESSAGE = (
    "👋 Hello! I'm your Support Bot. I can assist with:\n"
    "✅ Creating support tickets\n"
    "✅ Handling inquiries\n"
    "✅ Getting assistance\n\n"
    "How can I help you today?"
)

TICKET_PICKED_MESSAGE = (
    "🎫 You've picked up ticket {ticket_id}\n\n"
    "Original Issue: {issue}\n"
    "You can now chat here to handle the ticket."
)

class GoogleChatService:
    def __init__(self):
        load_dotenv()
        self.credentials = self._get_credentials()
        self.service = build('chat', 'v1', credentials=self.credentials)

    def _get_credentials(self) -> service_account.Credentials:
        """Initialize Google service account credentials"""
        try:
            # First try to load from environment variables
            credentials_dict = {
                "type": "service_account",
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "private_key": os.getenv("GOOGLE_PRIVATE_KEY", "").replace('\\n', '\n'),  # Handle newlines
                "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID", "")
            }

            # Validate required fields
            required_fields = ["project_id", "private_key", "client_email"]
            missing_fields = [field for field in required_fields if not credentials_dict.get(field)]
            if missing_fields:
                raise ValueError(f"Missing required credentials: {', '.join(missing_fields)}")

            return service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=['https://www.googleapis.com/auth/chat.bot']
            )

        except Exception as e:
            logger.error(f"Error initializing credentials: {str(e)}", exc_info=True)
            raise ValueError("Failed to initialize Google Chat credentials. Check your environment variables.")
    
    
    async def _execute_request(self, request) -> Dict[str, Any]:
        """Execute Google Chat API request asynchronously"""
        try:
            return await asyncio.to_thread(request.execute)
        except Exception as e:
            logger.error(f"Error executing request: {str(e)}", exc_info=True)
            raise

    async def handle_chat_event(self, event: dict) -> Dict[str, Any]:
        """Main handler for chat events"""
        try:
            space = event.get('space', {}).get('name')
            message = event.get('message', {})
            event_type = event.get('type')

            # Handle space addition
            if event_type == 'ADDED_TO_SPACE':
                return await self.send_message(space, WELCOME_MESSAGE)

            # Handle button clicks
            if message.get('actionResponse'):
                return await self._handle_button_click(event)

            # Handle regular messages
            if message.get('text'):
                return await self._handle_message(event)

            return {"text": ""}

        except Exception as e:
            logger.error(f"Error handling chat event: {str(e)}", exc_info=True)
            return {"text": "An error occurred processing your request"}

    async def _handle_button_click(self, event: dict) -> Dict[str, Any]:
        """Handle button click events"""
        try:
            space = event.get('space', {}).get('name')
            message = event.get('message', {})
            action = message.get('actionResponse', {}).get('action', {})
            
            if action.get('function') != 'pick_ticket':
                return {"text": "Invalid action"}

            # Get ticket info
            parameters = action.get('parameters', [])
            ticket_id = next((
                p.get('value') for p in parameters 
                if p.get('key') == 'ticket_id'
            ), None)
            
            if not ticket_id:
                return {"text": "Invalid ticket selection"}

            user = event.get('user', {})
            if not user or not user.get('name'):
                return {"text": "Invalid user information"}

            # Create DM space
            dm_space = await self.create_direct_message(user['name'])
            
            # Send welcome message in DM
            await self.send_message(
                dm_space,
                TICKET_PICKED_MESSAGE.format(
                    ticket_id=ticket_id,
                    issue=message.get('text', 'No description provided')
                )
            )
            
            # Update original card
            await self.update_card(
                message['name'],
                self._create_picked_status_card(ticket_id, user.get('displayName', 'Unknown User'))
            )
            
            # Send confirmation in original space
            await self.send_message(
                space,
                f"✅ Ticket {ticket_id} has been picked up by {user.get('displayName', 'Unknown User')}"
            )
            
            return {"text": ""}
        
        except Exception as e:
            logger.error(f"Error handling button click: {str(e)}", exc_info=True)
            raise

    async def _handle_message(self, event: dict) -> Dict[str, Any]:
        """Handle regular message events"""
        try:
            space = event.get('space', {}).get('name')
            message = event.get('message', {})
            text = message.get('text', '').lower().strip()
            sender = message.get('sender', {}).get('displayName', 'Unknown User')

            # Handle greetings
            if any(greeting in text for greeting in ['hi', 'hello', 'hey']):
                return await self.send_message(space, WELCOME_MESSAGE)

            # Create ticket for other messages
            ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            await self.send_card(space, self._create_ticket_card(ticket_id, sender, text))
            return {"text": ""}

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}", exc_info=True)
            raise

    def _create_ticket_card(self, ticket_id: str, user: str, issue: str) -> Dict:
        """Create a ticket notification card"""
        dm_url = f"https://mail.google.com/mail/u/0/?ogbl#chat/dm/m80AU8AAAAE"
        
        return {
        "cardsV2": [{
            "cardId": ticket_id,
            "card": {
                "header": {
                    "title": f"New Support Ticket: {ticket_id}",
                    "subtitle": f"From: {user}"
                },
                "sections": [{
                    "widgets": [
                        {
                            "decoratedText": {
                                "text": f"Issue: {issue}",
                                "wrapText": True
                            }
                        },
                        {
                            "buttonList": {
                                "buttons": [
                                    {
                                        "text": "Pick this ticket",
                                        "onClick": {
                                            "openLink": {
                                                "url": dm_url
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }]
            }
        }]
    }

    def _create_picked_status_card(self, ticket_id: str, user: str) -> Dict:
        """Create a card showing ticket has been picked up"""
        return {
            "cardsV2": [{
                "cardId": f"{ticket_id}_picked",
                "card": {
                    "header": {
                        "title": f"Ticket {ticket_id} Status",
                        "subtitle": "Ticket Assigned"
                    },
                    "sections": [{
                        "widgets": [{
                            "decoratedText": {
                                "text": f"✅ Picked up by {user}",
                                "wrapText": True
                            }
                        }]
                    }]
                }
            }]
        }

    async def send_message(self, space: str, message: str) -> Dict[str, Any]:
        """Send a text message to Google Chat space"""
        try:
            request = self.service.spaces().messages().create(
                parent=space,
                body={"text": message}
            )
            return await self._execute_request(request)
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}", exc_info=True)
            raise

    async def send_card(self, space: str, card: Dict) -> Dict[str, Any]:
        """Send an interactive card to Google Chat space"""
        try:
            request = self.service.spaces().messages().create(
                parent=space,
                body=card
            )
            return await self._execute_request(request)
        except Exception as e:
            logger.error(f"Error sending card: {str(e)}", exc_info=True)
            raise

    async def update_card(self, message_name: str, card: Dict) -> Dict[str, Any]:
        """Update an existing card"""
        try:
            request = self.service.spaces().messages().update(
                name=message_name,
                updateMask="cardsV2",
                body=card
            )
            return await self._execute_request(request)
        except Exception as e:
            logger.error(f"Error updating card: {str(e)}", exc_info=True)
            raise

    async def create_direct_message(self, user: str) -> str:
        """Create a direct message space with a user"""
        try:
            request = self.service.spaces().create(
                body={
                    "space": {
                        "type": "DM",
                        "singleUserBotDm": True,
                        "threaded": True
                    }
                }
            )
            response = await self._execute_request(request)
            logger.info(f"DM space created with user {user}")
            return response.get('name')
        except Exception as e:
            logger.error(f"Error creating DM space: {str(e)}", exc_info=True)
            raise
    
    async def send_ticket_notification(self, space: str, ticket_id: str, user: str, issue: str) -> Dict[str, Any]:
        """Send a ticket notification with an action button"""
        try:
            # Create the ticket card
            card = self._create_ticket_card(ticket_id, user, issue)

            # Send the card
            return await self.send_card(space, card)
        except Exception as e:
            logger.error(f"Error sending ticket notification: {str(e)}", exc_info=True)
            raise