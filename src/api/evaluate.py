from fastapi import APIRouter
from pydantic import BaseModel
from src.core.llm_client import call_llm

router = APIRouter()

class EvaluateRequest(BaseModel):
    prompt: str

class EvaluateResponse(BaseModel):
    risk_level: str
    reasoning: str

@router.post("/", response_model=EvaluateResponse)
def evaluate_prompt(request: EvaluateRequest):
    try:
        system_prompt = f"""
            You are an AI safety classifier.
            Classify the following prompt as LOW, MEDIUM, or HIGH risk.
            Also provide reasoning for your classification.

            Prompt:
            {request.prompt}
        """

        result = call_llm(system_prompt)

        return {
            "risk_level": "HIGH" if "HIGH" in result.upper() else "LOW",
            "reasoning": result,
        }
    except Exception as e:
        return {
            "risk_level": "ERROR",
            "reasoning": str(e),
        }

