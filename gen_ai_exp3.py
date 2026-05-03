from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json


app = FastAPI(title="GenAI RAG API")


KNOWLEDGE_BASE = [
    "Mortgage preapproval is an estimate from a lender of how much a borrower may be able to borrow.",
    "A fixed-rate mortgage keeps the same interest rate over the life of the loan.",
    "An adjustable-rate mortgage can change its interest rate over time.",
    "Closing costs usually include lender fees, title fees, taxes, and insurance-related costs.",
]


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    confidence: float
    source_count: int


def retrieve_context(query: str, kb: List[str], top_k: int = 2) -> List[str]:
    query_words = set(query.lower().split())
    scored = []

    for chunk in kb:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored[:top_k] if score > 0]


def build_prompt(user_query: str, context_chunks: List[str]) -> str:
    context_text = "\n".join(f"- {chunk}" for chunk in context_chunks)

    return f"""
Use ONLY the provided context to answer the question.
Return ONLY valid JSON.

JSON schema:
{{
  "answer": "string",
  "confidence": 0.0,
  "source_count": 0
}}

Context:
{context_text}

Question:
{user_query}
""".strip()


def mock_llm_call(prompt: str) -> str:
    return json.dumps({
        "answer": "A fixed-rate mortgage keeps the same interest rate over the life of the loan.",
        "confidence": 0.94,
        "source_count": 2
    })


def parse_llm_json(response_text: str) -> Dict:
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM: {e}")

    required_keys = ["answer", "confidence", "source_count"]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

    return data


def answer_question(user_query: str) -> Dict:
    context_chunks = retrieve_context(user_query, KNOWLEDGE_BASE, top_k=2)

    if not context_chunks:
        return {
            "answer": "I don't know.",
            "confidence": 0.0,
            "source_count": 0
        }

    prompt = build_prompt(user_query, context_chunks)
    llm_response = mock_llm_call(prompt)
    parsed_output = parse_llm_json(llm_response)

    return parsed_output


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    try:
        result = answer_question(request.question)
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
'''
How to run

Save as: main.py

Install: pip install fastapi uvicorn pydantic

Run: uvicorn main:app --reload

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