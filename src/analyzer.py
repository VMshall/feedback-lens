import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_feedback(feedbacks: list[str]) -> dict:
    if not feedbacks:
        raise ValueError("No feedback provided")

    feedback_block = "\n".join(f"{i+1}. {fb}" for i, fb in enumerate(feedbacks))

    prompt = f"""You are a product analytics expert. Analyze the following {len(feedbacks)} customer feedback snippets.

FEEDBACK:
{feedback_block}

Produce a JSON response with this exact structure:
{{
  "clusters": [
    {{
      "theme": "short theme name",
      "sentiment_score": 0.75,
      "sentiment_label": "positive|neutral|negative|mixed",
      "count": 3,
      "examples": ["feedback snippet 1", "feedback snippet 2"],
      "summary": "one sentence summary of this cluster"
    }}
  ],
  "top_complaints": ["specific complaint 1", "specific complaint 2", "specific complaint 3"],
  "top_praise": ["specific praise 1", "specific praise 2", "specific praise 3"],
  "action_items": [
    {{
      "priority": "high|medium|low",
      "action": "specific actionable recommendation",
      "rationale": "why this matters"
    }}
  ],
  "overall_sentiment_score": 0.6,
  "total_analyzed": {len(feedbacks)}
}}

Rules:
- sentiment_score: -1.0 (very negative) to 1.0 (very positive)
- Create 3-7 meaningful clusters based on actual themes in the data
- top_complaints and top_praise should each have 3-5 items
- action_items should have 3-5 prioritized items
- Return ONLY valid JSON, no markdown fences"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    return json.loads(raw)
