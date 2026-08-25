import os

from openai import OpenAI


# ============================================================
# Azure OpenAI configuration
# ============================================================

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]

client = OpenAI(
    api_key=api_key,
    base_url=endpoint.rstrip("/") + "/"
)


# ============================================================
# Generate grounded answer
# ============================================================

def generate_answer(
    question: str,
    context: str
) -> str:

    answer_prompt = f"""
You are OpsPilot, a DevOps troubleshooting assistant.

Answer the user's question using ONLY the retrieved knowledge
provided below.

Do not invent commands, causes, troubleshooting steps, or
technical details that are not supported by the retrieved
knowledge.

User question:
{question}

Retrieved knowledge:
{context}

Provide a clear and practical answer for a DevOps engineer.
"""

    response = client.responses.create(
        model=deployment,
        input=answer_prompt
    )

    answer = response.output_text.strip()

    return answer