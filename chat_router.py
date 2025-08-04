from fastapi import APIRouter, HTTPException
from schemas import ChatRequest, ChatResponse
from chatbot import get_chatbot_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse, include_in_schema=False)
@router.post("/chat/", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    """
    Menangani permintaan chat dari pengguna dan mengembalikan respons dari chatbot.
    """
    try:
        # --- MODIFIED: Pass the history to the chatbot function ---
        response_text = get_chatbot_response(request.query, request.history)
        return ChatResponse(response=response_text)
    except Exception as e:
        print(f"API Error in chat_router: {type(e).__name__} - {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan internal pada server.")