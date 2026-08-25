from pathlib import Path
import chromadb


# ============================================================
# 1. Connect to persistent ChromaDB
# ============================================================

CHROMA_DIR = Path("chroma_db")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="opspilot_knowledge"
)


# ============================================================
# 2. Test question
# ============================================================

question = "How do I create a Kubernetes deployment?"


# ============================================================
# 3. Retrieve top 5 results
# ============================================================

results = collection.query(
    query_texts=[question],
    n_results=5
)


# ============================================================
# 4. Display relevance information
# ============================================================

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for i, (document, metadata, distance) in enumerate(
    zip(documents, metadatas, distances),
    start=1
):

    print("\n" + "=" * 60)
    print(f"RESULT {i}")
    print("=" * 60)

    print("Distance:", distance)

    print("Source:", metadata.get("source"))
    print("Section:", metadata.get("section"))
    print("Subsection:", metadata.get("subsection"))

    print("\nDocument preview:")
    print(document[:200])