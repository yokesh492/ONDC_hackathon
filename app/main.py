from fastapi import FastAPI
from app.api.routes import router as api_router
from app.api.auth import router

app = FastAPI()

app.include_router(api_router)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
