
import json
from utils.gemini import client


def assign_role(name, education, background, skills,
                experience, interests):

    prompt = f"""
    You are an AI Intern Skill Assessor for Bashaar AI.

    Analyze the following intern profile:

    Name: {name}
    Education: {education}
    Background: {background}
    Skills: {", ".join(skills)}
    Experience: {experience}
    Interests: {interests}

    Assign the intern ONE most suitable role from these options:

    1. Outreach Strategist
    2. Automation Builder
    3. Content Creator

    Consider the intern's skills, background, experience
    and interests before assigning the role.

    Return ONLY valid JSON in this exact format:

    {{
        "assigned_role": "Role Name",
        "assessment": "Short explanation of why this role suits the intern"
    }}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result = json.loads(response.text)

    return result
