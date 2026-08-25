from pathlib import Path

import chromadb


# ============================================================
# 1. Paths
# ============================================================

DOCS_DIR = Path("docs")
CHROMA_DIR = Path("chroma_db")


# ============================================================
# 2. Connect to persistent ChromaDB
# ============================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

try:
    client.delete_collection(
        name="opspilot_knowledge"
    )
except Exception:
    pass

collection = client.get_or_create_collection(
    name="opspilot_knowledge"
)


# ============================================================
# 3. Find all Markdown documents
# ============================================================

documents = list(DOCS_DIR.glob("*.md"))

print(f"Documents found: {len(documents)}")

for document in documents:
    print(f" - {document}")


# ============================================================
# 4. Process each document
# ============================================================

all_chunks = []
all_metadatas = []
all_ids = []


for file_path in documents:

    print("\n" + "=" * 60)
    print(f"Processing: {file_path}")
    print("=" * 60)

    text = file_path.read_text(encoding="utf-8")

    print("Characters:", len(text))


    # --------------------------------------------------------
    # Split document into meaningful sections
    # --------------------------------------------------------

    lines = text.splitlines()

    document_title = ""
    current_section = ""
    current_subsection = ""

    current_chunk = []

    chunks = []


    # --------------------------------------------------------
    # Helper function
    # --------------------------------------------------------

    def save_chunk():

        if not current_chunk:
            return

        chunk_text = "\n".join(current_chunk).strip()

        # Check whether the chunk contains actual content
        # beyond Markdown headings and blank lines.
        content_lines = [
            line.strip()
            for line in current_chunk
            if line.strip()
            and not line.strip().startswith("#")
        ]

        # Skip heading-only chunks
        if not content_lines:
            return

        chunks.append({
            "text": chunk_text,
            "section": current_section,
            "subsection": current_subsection
        })


    # --------------------------------------------------------
    # Process each line
    # --------------------------------------------------------

    for line in lines:

        # ----------------------------------------------------
        # Level 1 heading = document title
        # ----------------------------------------------------

        if line.startswith("# ") and not line.startswith("## "):

            document_title = line.replace("# ", "").strip()

            # Do NOT create a chunk here.
            # The title will be included with actual sections.

            continue


        # ----------------------------------------------------
        # Level 2 heading = section
        # ----------------------------------------------------

        elif line.startswith("## "):

            # Save previous chunk only if it has actual content
            save_chunk()

            current_section = line.replace("## ", "").strip()
            current_subsection = ""

            current_chunk = [
                f"# {document_title}",
                line
            ]


        # ----------------------------------------------------
        # Level 3 heading = subsection
        # ----------------------------------------------------

        elif line.startswith("### "):

            # Save previous chunk only if it has actual content
            save_chunk()

            current_subsection = line.replace("### ", "").strip()

            current_chunk = [
                f"# {document_title}",
                f"## {current_section}",
                line
            ]


        # ----------------------------------------------------
        # Normal content
        # ----------------------------------------------------

        else:

            current_chunk.append(line)


    # --------------------------------------------------------
    # Add final chunk
    # --------------------------------------------------------

    save_chunk()


    # --------------------------------------------------------
    # Add chunks to global lists
    # --------------------------------------------------------

    print("Chunks created:", len(chunks))

    category = file_path.stem.lower()

    for index, chunk in enumerate(chunks):

        chunk_id = f"{category}_{index}"

        metadata = {
            "source": file_path.name,
            "category": category,
            "section": chunk["section"],
            "subsection": chunk["subsection"]
        }

        all_chunks.append(chunk["text"])
        all_metadatas.append(metadata)
        all_ids.append(chunk_id)


# ============================================================
# 5. Store everything in ChromaDB
# ============================================================

if all_chunks:

    collection.add(
        documents=all_chunks,
        metadatas=all_metadatas,
        ids=all_ids
    )


# ============================================================
# 6. Display final result
# ============================================================

print("\n" + "=" * 60)
print("INGESTION COMPLETE")
print("=" * 60)

print("Total chunks stored:", len(all_chunks))
print("Collection count:", collection.count())