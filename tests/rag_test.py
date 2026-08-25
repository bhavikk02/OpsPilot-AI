import os
from pathlib import Path

import chromadb
from openai import OpenAI


# ============================================================
# 1. Connect to our persistent ChromaDB
# ============================================================

CHROMA_DIR = Path("chroma_db")

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_collection(
    name="opspilot_knowledge"
)


# ============================================================
# 2. User question
# ============================================================

question = "How do I check if my Nginx configuration is valid?"


# ============================================================
# 3. Retrieve relevant chunks from ChromaDB
# ============================================================

results = collection.query(
    query_texts=[question],
    n_results=3
)


# ============================================================
# 4. Extract retrieved documents
# ============================================================

documents = results["documents"][0]
metadatas = results["metadatas"][0]


sources = []

for metadata in metadatas:
    sources.append({
        "source": metadata.get("source", "Unknown"),
        "section": metadata.get("section", "Unknown"),
        "subsection": metadata.get("subsection", "Unknown")
    })

context = "\n\n---\n\n".join(documents)

# ============================================================
# 5. Display retrieved context
# ============================================================

print("\nRetrieved Context:")
print("=" * 60)
print(context)


# ============================================================
# 6. Build the RAG prompt
# ============================================================

prompt = f"""
You are OpsPilotAI, a DevOps troubleshooting assistant.

Use the provided knowledge-base context to answer the user's question.

Knowledge-base context:
{context}

User question:
{question}

Answer using the provided context.
"""


# ============================================================
# 7. Connect to Azure OpenAI
# ============================================================

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]

client = OpenAI(
    api_key=api_key,
    base_url=endpoint.rstrip("/") + "/"
)


# ============================================================
# 8. Send the RAG prompt to GPT-4.1-mini
# ============================================================

response = client.responses.create(
    model=deployment,
    input=prompt
)


# ============================================================
# 9. Display final answer
# ============================================================

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(response.output_text)

print("\n" + "=" * 60)
print("SOURCES")
print("=" * 60)

for source in sources:
    print(f"Source: {source['source']}")
    print(f"Section: {source['section']}")
    print(f"Subsection: {source['subsection']}")
    print()