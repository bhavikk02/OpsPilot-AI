from pathlib import Path

file_path = Path("docs/nginx.md")

content = file_path.read_text(encoding="utf-8")

print(content)