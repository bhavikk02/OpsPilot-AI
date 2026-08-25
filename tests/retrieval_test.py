import chromadb


# Connect to our persistent ChromaDB
client = chromadb.PersistentClient(
    path="chroma_db"
)

# Open the existing collection
collection = client.get_collection(
    name="opspilot_knowledge"
)


# User's question
query = "How do I check if my Nginx configuration is valid?"


# Search the vector database
results = collection.query(
    query_texts=[query],
    n_results=3
)


print("\nQuery:")
print(query)

print("\nSearch Results:")

for index, document in enumerate(results["documents"][0], start=1):

    print(f"\n{'=' * 60}")
    print(f"RESULT {index}")
    print(f"{'=' * 60}")

    print("\nDocument:")
    print(document)

    print("\nMetadata:")
    print(results["metadatas"][0][index - 1])

    print("\nDistance:")
    print(results["distances"][0][index - 1])