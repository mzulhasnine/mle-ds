from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal


app = FastAPI(title="Structured Extraction API")


class ExtractRequest(BaseModel):
    text: str


class LoanInfo(BaseModel):
    name: str
    loan_amount: float
    risk_level: Literal["low", "medium", "high"]


def extract_loan_info(text: str) -> LoanInfo:
    # In real life, this would call LLM structured output.
    # Here we mock it for interview/demo.
    return LoanInfo(
        name="John",
        loan_amount=200000,
        risk_level="medium"
    )


@app.post("/extract", response_model=LoanInfo)
def extract(request: ExtractRequest):
    try:
        result = extract_loan_info(request.text)
        return result

    except Exception:
        raise HTTPException(status_code=500, detail="Extraction failed")
    

'''
How to run

Save as: main.py

Install: pip install fastapi uvicorn pydantic

Run: uvicorn gen_ai_exp4:app --reload

Open browser: http://127.0.0.1:8000/docs

FastAPI gives you Swagger UI automatically.

3. Example request

Endpoint:

POST /ask

Request body:
{
  "question": "What is a fixed-rate mortgage?"
}

Response:
{
  "answer": "A fixed-rate mortgage keeps the same interest rate over the life of the loan.",
  "confidence": 0.94,
  "source_count": 2
}
'''