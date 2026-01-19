from fastapi import APIRouter
from pydantic import BaseModel
from src.core.llm_client import call_llm

router = APIRouter()

class GenerateRequest(BaseModel):
    task: str

class GenerateResponse(BaseModel):
    prompt: str

@router.post("/", response_model=GenerateResponse)
def generate_prompt(request: GenerateRequest):
    try:
        system_prompt = f"""
            Generate a safe and structured prompt for the following task.
            Avoid unsafe instructions or policy violations.

            Task:
            {request.task}  
        """

        result = call_llm(system_prompt)

        return {"prompt": result}
    except Exception as e:
        return {"prompt": f"ERROR: {str(e)}"}

