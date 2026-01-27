import os
from google.genai import Client
from dotenv import load_dotenv



load_dotenv()

client = Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

from .retrieval import retrieve_cisg_context

SYSTEM_PROMPT_CISG = """
You are a legal assistant specialized in international sale of goods law (CISG).
You:
- Explain articles clearly and precisely.
- Distinguish CISG from domestic law.
- Do NOT give practical legal advice; only legal information.
- Always cite relevant CISG articles.
"""

def cisg_assistant(call_model, user_question: str):
    context = retrieve_cisg_context(user_question)

    prompt = f"""{SYSTEM_PROMPT_CISG}

User question:
{user_question}

Relevant CISG materials:
{context}

Answer the user by:
- Explaining the relevant CISG rules
- Citing specific articles
- Staying within CISG law
"""

    return call_model(prompt)
def call_model(prompt):
    response = client.models.generate_content(
        model="GOOGLE_MODEL_NAME",
        contents=[
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    )

    return response.text