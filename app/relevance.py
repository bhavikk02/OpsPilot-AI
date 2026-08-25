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
# Check whether retrieved knowledge is relevant
# ============================================================

def check_relevance(
    question: str,
    context: str
) -> str:

    relevance_prompt = f"""
You are evaluating retrieved knowledge for a DevOps RAG system.

User question:
{question}

Retrieved knowledge:
{context}

Determine whether the retrieved knowledge contains enough
information to answer the user's question accurately.

The retrieved knowledge must directly address the user's
question. Do not assume that information about a related
DevOps problem is sufficient.

Respond with ONLY one of these two values:

YES

or

NO
"""

    response = client.responses.create(
        model=deployment,
        input=relevance_prompt
    )

    decision = response.output_text.strip().upper()

    return decision