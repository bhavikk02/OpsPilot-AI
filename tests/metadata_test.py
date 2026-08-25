from pathlib import Path
import chromadb


# Connect to persistent ChromaDB
CHROMA_DIR = Path("chroma_db")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="opspilot_knowledge"
)


# User question
question = "How do I check if my Nginx configuration is valid?"


# Retrieve top 3 results
results = collection.query(
    query_texts=[question],
    n_results=3
)


# Display documents + metadata together
for i in range(len(results["documents"][0])):

    print("\n" + "=" * 60)
    print(f"RESULT {i + 1}")
    print("=" * 60)

    print("\nDocument:")
    print(results["documents"][0][i])

    print("\nMetadata:")
    print(results["metadatas"][0][i])

    print("\nDistance:")
    print(results["distances"][0][i])