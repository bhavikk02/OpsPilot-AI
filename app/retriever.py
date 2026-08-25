from pathlib import Path

import chromadb


# ============================================================
# ChromaDB configuration
# ============================================================

CHROMA_DIR = Path("chroma_db")


# ============================================================
# Connect to ChromaDB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_collection(
    name="opspilot_knowledge"
)


# ============================================================
# Retrieve relevant chunks
# ============================================================

def retrieve_chunks(
    question: str,
    n_results: int = 3
):
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        source = metadata.get(
            "source",
            "Unknown"
        )

        section = metadata.get(
            "section",
            "Unknown"
        )

        subsection = metadata.get(
            "subsection",
            "Unknown"
        )

        context_parts.append(
            f"""
SOURCE: {source}
SECTION: {section}
SUBSECTION: {subsection}

{document}
""".strip()
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    return {
        "documents": documents,
        "metadatas": metadatas,
        "distances": distances,
        "context": context
    }