
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def test_gemini():

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say hello to Bashaar AI in one sentence."
    )

    return response.text
