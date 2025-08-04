from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    query: str
    # --- NEW: Add an optional field for chat history ---
    history: Optional[List[Dict[str, Any]]] = None

class ChatResponse(BaseModel):
    response: str