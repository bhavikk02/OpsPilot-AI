from pathlib import Path
import re


# Path to our knowledge-base document
file_path = Path("docs/nginx.md")

# Read the Markdown file
text = file_path.read_text(encoding="utf-8")

print("File loaded successfully!")
print("Characters:", len(text))


# Find Markdown headings
headings = re.findall(r"^(#+)\s+(.*)$", text, re.MULTILINE)

print("\nHeadings found:")

for level, title in headings:
    print(f"Level {len(level)}: {title}")

# Split the document into lines
lines = text.splitlines()

chunks = []

document_title = None
current_section = None
current_subsection = None
current_content = []


def save_chunk():
    """Create and save a structured chunk."""

    if not current_content:
        return

    content = "\n".join(current_content).strip()

    if not content:
        return

    chunk_text = ""

    if document_title:
        chunk_text += document_title + "\n"

    if current_section:
        chunk_text += current_section + "\n"

    if current_subsection:
        chunk_text += current_subsection + "\n"

    chunk_text += "\n" + content

    metadata = {
        "source": file_path.name,
        "category": "nginx",
        "section": current_section.replace("## ", "") if current_section else "",
        "subsection": (
            current_subsection.replace("### ", "")
            if current_subsection
            else ""
        )
    }

    chunks.append({
        "text": chunk_text.strip(),
        "metadata": metadata
    })


for line in lines:

    # Level 1 heading = document title
    if line.startswith("# ") and not line.startswith("## "):
        document_title = line

    # Level 2 heading = section
    elif line.startswith("## ") and not line.startswith("### "):

        save_chunk()

        current_section = line
        current_subsection = None
        current_content = []

    # Level 3 heading = subsection
    elif line.startswith("### "):

        save_chunk()

        current_subsection = line
        current_content = []

    # Normal content
    else:
        current_content.append(line)


# Save the final chunk
save_chunk()


# Display structured chunks
print("\nStructured chunks created:", len(chunks))

for index, chunk in enumerate(chunks, start=1):

    print(f"\n{'=' * 60}")
    print(f"CHUNK {index}")
    print(f"{'=' * 60}")

    print("\nTEXT:")
    print(chunk["text"])

    print("\nMETADATA:")
    print(chunk["metadata"])