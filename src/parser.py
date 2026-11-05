from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language, MarkdownTextSplitter


def parse_files(files_path):
    files = Path(files_path)
    Chunks: dict[str, list[str]] = {}
    for file in files.rglob("*"):
        if file.suffix in [".md", ".txt", ".py"]:
            file_content = file.read_text(encoding="utf-8", errors="ignore")
            # Split the file content into chunks
            if file.suffix in [".md", ".txt"]:
                splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=0)
            else:
                splitter = RecursiveCharacterTextSplitter.from_language(
                    language=Language.PYTHON, chunk_size=1000, chunk_overlap=0
                )
            chunks = splitter.create_documents([file_content])
            Chunks[file.name] = [chunk.page_content.strip() for chunk in chunks]
    return Chunks

