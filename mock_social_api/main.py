from fastapi import FastAPI, Request
import httpx
from mock_social_api.api.v1.api import api_router as api_router_v1

app = FastAPI()

TARGET_BASE_URL = "http://arntreal.upstar.club:2001"

@app.get("/")
def read_root() -> str:
    """
    Root endpoint to verify that the API is up.
    
    Returns:
    --------
    status : str
        A string indicating the API status.
    """
    return "Active"

@app.api_route("/upstar/{path:path}", methods=["GET"])
async def proxy(request: Request, path: str):
    """
    This endpoint acts as a proxy, redirecting all incoming requests to the target base URL.
    """
    target_url = f"{TARGET_BASE_URL}/{path}?{request.query_params}"
    
    # Prepare the data for proxying the request
    headers = dict(request.headers)
    body = await request.body()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:  # Set timeout to 60 seconds
            # Use request's method dynamically to forward the request
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body
            )
        
        # Forward the response back to the client
        return response.json()

    except httpx.RequestError as e:
        return {"error": "Proxy request failed", "detail": str(e)}



# Add Routers
app.include_router(api_router_v1, prefix="/api/v1")