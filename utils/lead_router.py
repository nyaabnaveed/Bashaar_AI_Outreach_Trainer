import json
from utils.gemini import client


def qualify_lead(inquiry):

    prompt = f"""
    You are an AI Lead Qualification Assistant for Bashaar AI.

    Analyze the following incoming customer inquiry:

    INQUIRY:
    {inquiry}

    Extract the following information:

    1. Budget: Customer's available budget.
       If not mentioned, write "Not specified".

    2. Needs: What service or solution does the customer need?

    3. Timeline: When does the customer need the service?
       If not mentioned, write "Not specified".

    4. Urgency: Identify urgency as High, Medium, or Low.

    5. Lead Category: Classify the lead as Hot, Warm, or Cold.

    Classification guidelines:
    - Hot: Customer has a clear need, strong buying intent,
      and wants to proceed soon.
    - Warm: Customer is interested but needs more information
      or has a less immediate timeline.
    - Cold: Customer has weak interest or no clear buying intent.

    Return ONLY valid JSON in this exact format:

    {{
        "budget": "Customer budget",
        "needs": "Customer requirements",
        "timeline": "Expected timeline",
        "urgency": "High, Medium, or Low",
        "lead_category": "Hot, Warm, or Cold",
        "reasoning": "Short explanation of classification"
    }}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result = json.loads(response.text)

    if result["lead_category"] not in ["Hot", "Warm", "Cold"]:
        raise ValueError("Invalid lead category")

    if result["urgency"] not in ["High", "Medium", "Low"]:
        raise ValueError("Invalid urgency level")

    return result