import chromadb

# Create ChromaDB client
client = chromadb.Client()

# Create collection
collection = client.create_collection(
    name="opspilot_test"
)

# Add documents
collection.add(
    documents=[
        "Kubernetes pods can enter CrashLoopBackOff when the application repeatedly crashes.",
        "Docker containers may fail to start because of incorrect environment variables.",
        "Nginx 502 Bad Gateway usually indicates a problem communicating with the upstream service."
    ],
    ids=[
        "k8s-001",
        "docker-001",
        "nginx-001"
    ],
    metadatas=[
        {
            "source": "kubernetes.md",
            "category": "kubernetes"
        },
        {
            "source": "docker.md",
            "category": "docker"
        },
        {
            "source": "nginx.md",
            "category": "nginx"
        }
    ]
)

print("Documents added successfully!")
print("Document count:", collection.count())

# Search the collection
results = collection.query(
    query_texts=[
        "My Kubernetes container keeps restarting"
    ],
    n_results=2,
    where={
        "category": "kubernetes"
    }
)

print("\nSearch Results:")
print(results)