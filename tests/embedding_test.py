import chromadb


# Create ChromaDB client
client = chromadb.Client()

# Create a test collection
collection = client.create_collection(
    name="embedding_test"
)

# Add one document
collection.add(
    documents=[
        "Nginx returns a 502 error when the backend service is unavailable."
    ],
    ids=[
        "test-001"
    ]
)

# Retrieve the embedding
result = collection.get(
    ids=["test-001"],
    include=["embeddings", "documents"]
)

print("Document:")
print(result["documents"][0])

print("\nEmbedding:")
print(result["embeddings"][0])

print("\nEmbedding dimensions:")
print(len(result["embeddings"][0]))