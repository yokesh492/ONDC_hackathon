from fastapi import FastAPI
from app.api.routes import router as api_router
from app.api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, can be restricted in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include API and Auth routers
app.include_router(api_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    import os
    # Run the app using uvicorn, with port configuration from environment variable or default to 8000
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
