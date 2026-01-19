from fastapi import FastAPI
from src.api.evaluate import router as evaluate_router
from src.api.generate import router as generate_router
from src.api.health import router as health_router

app = FastAPI(title="PromptGuard")

app.include_router(evaluate_router, prefix="/evaluate", tags=["Evaluate"])
app.include_router(generate_router, prefix="/generate", tags=["Generate"])
app.include_router(health_router, prefix="/health", tags=["Health"])

@app.get("/")
def root():
    return {"message": "Welcome to PromptGuard API"}