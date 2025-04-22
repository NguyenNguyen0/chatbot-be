import time
import json
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.types import Message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("api")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request
        request_id = str(time.time())
        await self._log_request(request, request_id)

        # Process the request and get response
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log response
        await self._log_response(response, request_id, process_time)
        
        return response

    async def _log_request(self, request: Request, request_id: str):
        headers = dict(request.headers)
        # Mask Authorization token for security
        if "authorization" in headers:
            headers["authorization"] = f"{headers['authorization'][0:15]}...MASKED..."
        
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            # Make a copy of the request body
            receive_ = await request._receive()
            
            async def receive():
                return receive_
            
            request._receive = receive
            
            try:
                # Try to parse JSON body, catch exceptions for non-JSON content
                body_bytes = receive_.get("body", b"")
                if body_bytes:
                    body = json.loads(body_bytes)
            except json.JSONDecodeError:
                body = "Unable to parse request body"
                
        logger.info(f"REQUEST [{request_id}] - {request.method} {request.url.path}")
        logger.info(f"HEADERS [{request_id}] - {headers}")
        if body:
            logger.info(f"BODY [{request_id}] - {body}")
            
    async def _log_response(self, response: Response, request_id: str, process_time: float):
        # Log response status and processing time
        logger.info(f"RESPONSE [{request_id}] - Status: {response.status_code}, Time: {process_time:.4f}s")
        
        # Log response headers
        headers = dict(response.headers)
        logger.info(f"RESPONSE HEADERS [{request_id}] - {headers}")