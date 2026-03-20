# models/pydantic_models.py

from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    thread_id: str  
    message: str

class ChatResponse(BaseModel):
    response: str

class ApiCallArguments(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

