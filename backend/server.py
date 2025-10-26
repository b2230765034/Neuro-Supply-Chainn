"""
FastAPI server wrapper for the oracle service.
Provides REST API endpoints for frontend integration.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging

from oracle import OracleService
from config import Config

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Change log level to WARNING
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Neuro-Generative Supply Chain Oracle API",
    description="REST API for AI-powered supply chain optimization",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize oracle service
# Set use_mock_ai=False to enable real LLM calls. Make sure HUGGINGFACE_API_TOKEN is set in the environment.
oracle = OracleService(use_mock_ai=False)


@app.get("/api/llm-test")
async def llm_test():
    """Check whether the configured LLM model is reachable and working.

    Returns a quick diagnostic: HTTP status for the model endpoint and any message.
    """
    try:
        if Config.LLM_TYPE == 'local':
            from local_llm_client import LocalLLMClient
            client = LocalLLMClient()
        else:
            from qwen_client import QwenClient
            client = QwenClient()

        result = client.check_model()

        if result.get('ok'):
            return {
                'success': True,
                'status_code': result.get('status_code'),
                'message': f'{Config.LLM_TYPE.title()} LLM endpoint reachable and working.'
            }
        else:
            return {
                'success': False,
                'status_code': result.get('status_code'),
                'message': f'{Config.LLM_TYPE.title()} LLM endpoint unreachable.',
                'details': result.get('body')
            }

    except Exception as e:
        logger.error(f"LLM test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Request/Response Models
class EventRequest(BaseModel):
    event_description: str
    shipment_id: Optional[str] = None

class EventResponse(BaseModel):
    success: bool
    shipment_id: str
    event_description: str
    ai_report: dict
    signature: str
    transaction: dict
    processing_time: float
    timestamp: str

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Neuro-Generative Supply Chain Oracle API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "process_event": "/api/process-event",
            "query_shipment": "/api/shipment/{shipment_id}",
            "oracle_status": "/api/status"
        }
    }

@app.get("/api/status")
async def get_status():
    """Get oracle service status"""
    try:
        info = oracle.get_oracle_info()
        return info
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-event")
async def process_event(request: EventRequest):
    """
    Process a logistics event and generate AI report
    
    Args:
        request: EventRequest containing event_description and optional shipment_id
        
    Returns:
        EventResponse with AI report and blockchain transaction details
    """
    try:
        logger.info(f"Processing event: {request.event_description[:50]}...")
        
        result = oracle.process_event(
            event_description=request.event_description,
            shipment_id=request.shipment_id
        )
        
        if not result.get('success'):
            raise HTTPException(
                status_code=500, 
                detail=result.get('error', 'Failed to process event')
            )
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing event: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/shipment/{shipment_id}")
async def query_shipment(shipment_id: str):
    """
    Query shipment details from blockchain
    
    Args:
        shipment_id: Unique shipment identifier
        
    Returns:
        Shipment data from blockchain
    """
    try:
        logger.info(f"Querying shipment: {shipment_id}")
        
        result = oracle.query_shipment(shipment_id)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=404,
                detail=f"Shipment {shipment_id} not found"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying shipment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "oracle-api"}

# Run server
if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Oracle API Server...")
    logger.info(f"Host: {Config.BACKEND_HOST}")
    logger.info(f"Port: {Config.BACKEND_PORT}")
    
    uvicorn.run(
        "server:app",
        host=Config.BACKEND_HOST,
        port=Config.BACKEND_PORT,
        reload=False,  # Disable hot reload
        log_level="info"
    )
