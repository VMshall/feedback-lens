from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from analyzer import analyze_feedback

app = FastAPI(title="Feedback Lens API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5500", "http://127.0.0.1:5500", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FeedbackRequest(BaseModel):
    feedbacks: List[str]

@app.get("/")
def root():
    return {"status": "ok", "service": "feedback-lens"}

@app.post("/analyze")
async def analyze(request: FeedbackRequest):
    if len(request.feedbacks) < 1:
        raise HTTPException(status_code=400, detail="At least 1 feedback required")
    if len(request.feedbacks) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 feedbacks at once")
    try:
        result = analyze_feedback(request.feedbacks)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
