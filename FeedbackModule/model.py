from pydantic import BaseModel
from enum import Enum

class StatusType(str, Enum):
    CREATED = "StatusType.CREATED"
    PENDING = "StatusType.PENDING"
    CLOSED = "StatusType.CLOSED"
    DECLINED = "StatusType.DECLINED"

class FeedbackType(str, Enum):
    DEVICE_FEEDBACK = "ATM_FEEDBACK"
    UZCARD_CANCEL = "UZCARD"
    HUMO_CANCEL = "HUMO"
    DEVICE_REPAIR = "ATM_REPAIR"
    TRANSFER = "TRANSFER"

class FeedbackInfo(BaseModel):
    feedback_id: int
    user_id: str
    client_form: dict
    feedback_status: str
    feedback_answer: str
    feedback_type_id: int
    
class FeedbackList(BaseModel):
    contents: list[FeedbackInfo]

class Feedback(BaseModel):
    feedback_id: int
    user_id: str
    client_form: dict
    feedback_status: str
    feedback_answer: str
    feedback_type_id: int
    category: str
    atm_unique_id: str
    uploaded_file: str

class FeedbackUpdate(BaseModel):
    status: str

class FileResponse(BaseModel):
    file: bytes