from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Create router with prefix
router = APIRouter(prefix="/api/agents")

class ChatRequest(BaseModel):
    message: str

# Note: Remove /api/agents from the route since it's in the prefix
@router.post("/literature-chat")
async def chat_with_literature(request: ChatRequest):
    try:
        # TODO: Implement your actual literature chat logic here
        async def generate_response():
            # Placeholder response
            yield "Processing your literature query...\n"
            
        return StreamingResponse(generate_response(), media_type="text/plain")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 