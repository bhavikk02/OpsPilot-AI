import os
from pathlib import Path

import chromadb
from openai import OpenAI


# ============================================================
# 1. Connect to ChromaDB
# ============================================================

CHROMA_DIR = Path("chroma_db")

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_collection(
    name="opspilot_knowledge"
)


# ============================================================
# 2. Azure OpenAI configuration
# ============================================================

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]

client = OpenAI(
    api_key=api_key,
    base_url=endpoint.rstrip("/") + "/"
)


# ============================================================
# 3. User question
# ============================================================

question = "How do I troubleshoot a Kubernetes CrashLoopBackOff?"


# ============================================================
# 4. Retrieve top 3 chunks
# ============================================================

results = collection.query(
    query_texts=[question],
    n_results=3
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


# ============================================================
# 5. Build retrieved context
# ============================================================

context_parts = []

for document, metadata in zip(documents, metadatas):

    source = metadata.get("source", "Unknown")
    section = metadata.get("section", "Unknown")
    subsection = metadata.get("subsection", "Unknown")

    context_parts.append(
        f"""
SOURCE: {source}
SECTION: {section}
SUBSECTION: {subsection}

{document}
""".strip()
    )

context = "\n\n---\n\n".join(context_parts)


# ============================================================
# 6. Relevance check
# ============================================================

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

relevance_response = client.responses.create(
    model=deployment,
    input=relevance_prompt
)

decision = relevance_response.output_text.strip().upper()


# ============================================================
# 7. Display relevance check
# ============================================================

print("\n" + "=" * 60)
print("RELEVANCE CHECK")
print("=" * 60)

print("\nQuestion:")
print(question)

print("\nDecision:")
print(decision)


# ============================================================
# 8. Display retrieved chunks
# ============================================================

print("\nRetrieved Chunks:")
print("=" * 60)

for i, (document, metadata, distance) in enumerate(
    zip(documents, metadatas, distances),
    start=1
):

    print(f"\n--- CHUNK {i} ---")

    print(f"Distance: {distance}")

    print(
        f"Source: {metadata.get('source', 'Unknown')}"
    )

    print(
        f"Section: {metadata.get('section', 'Unknown')}"
    )

    print(
        f"Subsection: {metadata.get('subsection', 'Unknown')}"
    )

    print("\nContent:")
    print(document)

    print("-" * 60)


# ============================================================
# 9. Generate answer ONLY if context is relevant
# ============================================================

if decision == "YES":

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

    answer_response = client.responses.create(
        model=deployment,
        input=answer_prompt
    )

    answer = answer_response.output_text.strip()

    print("\n" + "=" * 60)
    print("GENERATED ANSWER")
    print("=" * 60)

    print(answer)


# ============================================================
# 10. Stop when knowledge is insufficient
# ============================================================

else:

    print("\n" + "=" * 60)
    print("GENERATED ANSWER")
    print("=" * 60)

    print(
        "I don't have enough relevant information in the "
        "knowledge base to answer this question accurately."
    )