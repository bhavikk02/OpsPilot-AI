# Retrieved information from ChromaDB
context = """
# Nginx 502 Bad Gateway
## Troubleshooting
### Check Nginx configuration

Run:

nginx -t

This verifies whether the Nginx configuration syntax is valid.
"""

# User's original question
question = "How do I check if my Nginx configuration is valid?"


# Build the RAG prompt
prompt = f"""
You are OpsPilotAI, a DevOps troubleshooting assistant.

Use the provided knowledge-base context to answer the user's question.

Knowledge-base context:
{context}

User question:
{question}

Answer using the provided context.
"""


print("RAG Prompt:")
print(prompt)