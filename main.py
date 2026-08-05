# main.py
from fastapi import FastAPI
from app.routes import api_router
from app.exception_handler import register_exception_handlers

app = FastAPI(
    title="Smoothie Registration API",
    version="1.0.0",
    description="API for registering customers for smoothie subscriptions."
)

register_exception_handlers(app)  # Register custom exception handlers

# Include your API router with a prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"message": "Hello from smoothie-registration!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)