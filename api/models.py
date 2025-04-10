# # # src/api/models.py
# # from pydantic import BaseModel
# # from typing import Optional, Dict

# # class WebhookEvent(BaseModel):
# #     type: str
# #     space: Dict
# #     message: Optional[Dict]
# #     user: Optional[Dict]



# # src/api/models.py
# from pydantic import BaseModel
# from typing import Optional, Dict


# class Sender(BaseModel):
#     name: str
#     displayName: Optional[str] = None

# class ActionParameter(BaseModel):
#     key: Optional[str] = None
#     value: Optional[str] = None


# class ActionResponse(BaseModel):
#     action: Optional[Action] = None


# class MessageSender(BaseModel):
#     name: str
#     displayName: Optional[str]
#     type: Optional[str]

# class SpaceDetails(BaseModel):
#     name: str
#     displayName: Optional[str]
#     type: str

# class MessageDetails(BaseModel):
#     name: Optional[str]
#     text: Optional[str]
#     sender: Optional[MessageSender]
#     createTime: Optional[str]

# class WebhookEvent(BaseModel):
#     type: str
#     eventTime: Optional[str]
#     space: SpaceDetails
#     message: Optional[MessageDetails]
#     user: Optional[MessageSender]



# class Message(BaseModel):
#     name: Optional[str] = None
#     text: Optional[str] = None
#     sender: Optional[Sender] = None
#     actionResponse: Optional[ActionResponse] = None

# class Space(BaseModel):
#     name: str
#     type: Optional[str] = "ROOM"
#     displayName: Optional[str] = None

# class ChatEvent(BaseModel):
#     type: str
#     space: Space
#     message: Optional[Message] = None
#     user: Optional[User] = None
#     eventTime: Optional[str] = None
    
    
# class User(BaseModel):
#     name: str
#     displayName: Optional[str] = None




# src/api/models.py
from pydantic import BaseModel
from typing import Optional, Dict, List, Any

class Sender(BaseModel):
    name: str
    displayName: Optional[str] = None
    type: Optional[str] = None  # Added type field for bot detection

class ActionParameter(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None

class Action(BaseModel):
    function: Optional[str] = None
    parameters: Optional[List[ActionParameter]] = None

class ActionResponse(BaseModel):
    action: Optional[Action] = None

class Message(BaseModel):
    name: Optional[str] = None
    text: Optional[str] = None
    sender: Optional[Sender] = None
    actionResponse: Optional[ActionResponse] = None

class Space(BaseModel):
    name: str
    type: Optional[str] = "ROOM"
    displayName: Optional[str] = None

class User(BaseModel):
    name: str
    displayName: Optional[str] = None
    type: Optional[str] = None  # Added type field for consistency

class ChatEvent(BaseModel):
    type: str
    space: Space
    message: Optional[Message] = None
    user: Optional[User] = None
    eventTime: Optional[str] = None