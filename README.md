# Feedback Lens

AI customer feedback analyzer — cluster themes, extract sentiment trends, and surface actionable product insights.

## Problem

Product teams drown in user feedback spread across Intercom, G2, App Store, surveys. No time to read it all.

## Solution

Paste 10–50 feedback snippets → AI clusters them into themes, scores sentiment per cluster, identifies top complaints, top praise, and gives product team prioritized action items.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
cd src
uvicorn main:app --reload --port 8000
# Open frontend/index.html in browser
```

## API

### POST /analyze
```json
{
  "feedbacks": ["The app crashes on upload", "Love the new UI!", "..."]
}
```

**Response:**
```json
{
  "clusters": [
    {
      "theme": "App Stability",
      "sentiment_score": -0.8,
      "sentiment_label": "negative",
      "count": 5,
      "examples": ["The app crashes on upload"],
      "summary": "Users experiencing crashes and bugs"
    }
  ],
  "top_complaints": ["App crashes on photo upload"],
  "top_praise": ["New dashboard design"],
  "action_items": [
    {
      "priority": "high",
      "action": "Fix photo upload crash on iOS",
      "rationale": "Affects 30% of feedback, core feature"
    }
  ],
  "overall_sentiment_score": 0.2,
  "total_analyzed": 25
}
```

## Tech Stack

- **Backend:** FastAPI + Anthropic Claude claude-opus-4-6
- **Frontend:** Vanilla HTML/CSS/JS + Tailwind CSS CDN
- **AI Model:** claude-opus-4-6
