
import json
from utils.gemini import client


def evaluate_outreach(message, campaign):

    prompt = f"""
    You are the Lead Sales Trainer at Bashaar AI.

    Your task is to evaluate an outreach message written by an intern.

    CAMPAIGN TARGET: {campaign}

    INTERN'S OUTREACH MESSAGE:
    {message}

    Evaluate the message on these 3 metrics:

    1. Hook Quality (0-10):
       Does it capture attention instantly without sounding spammy?

    2. Value Proposition (0-10):
       Does it clearly explain how Bashaar AI solves the
       target audience's problem?

    3. Call-To-Action Clarity (0-10):
       Does it provide a direct and easy next step?

    Also provide:
    - Overall feedback about the message.
    - Actionable improvement suggestions for every metric
      that receives a score below 7.
    - A complete improved version of the outreach message
      ready to send.

    Return ONLY valid JSON in this exact format:

    {{
        "hook_score": 8,
        "value_score": 6,
        "cta_score": 7,
        "overall_feedback": "Feedback about the message",
        "improvement_suggestions": [
            "Specific suggestion for improving weak areas"
        ],
        "improved_version": "Complete rewritten outreach message"
    }}

    All scores must be numbers between 0 and 10.
    Do not include markdown or text outside JSON.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result = json.loads(response.text)

    score_fields = ["hook_score", "value_score", "cta_score"]

    for field in score_fields:
        score = result[field]

        if not isinstance(score, (int, float)) or not 0 <= score <= 10:
            raise ValueError(f"Invalid score: {field}")

    return result
