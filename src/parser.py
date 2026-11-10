from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language, MarkdownTextSplitter
from src.models import MinimalSource
from typing import Any
from tqdm import tqdm


def parse_files(files_path, max_chunk_size: int = 1000) -> list[dict[str, Any]]:
    files = Path(files_path)
    register: list[dict[str, Any]] = []
    files = [f for f in files.rglob("*") if f.suffix in [".md", ".txt", ".py"]]
    for file in tqdm(files, desc="Indexing", unit="file"):
        # Split the file content into chunks
        if file.suffix in [".md", ".txt"]:
            splitter = MarkdownTextSplitter(chunk_size=max_chunk_size, chunk_overlap=0)
        else:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON, chunk_size=max_chunk_size, chunk_overlap=0
            )
        register.extend(chunk_file(file, splitter))
    return register


def chunk_file(file: Path, splitter:RecursiveCharacterTextSplitter
                | MarkdownTextSplitter) -> list[dict[str, Any]]:
    try:
        file_content = file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    chunks = splitter.create_documents([file_content])
    file_chunks: list[dict[str, Any]] = []
    last_idx = 0
    for chunk in chunks:
        first_idx = file_content.find(chunk.page_content.strip(), last_idx)
        if first_idx == -1:
            first_idx = last_idx
        last_idx = first_idx + len(chunk.page_content)
        source = MinimalSource(
            file_path=str(file),
              first_character_index=first_idx,
                last_character_index=last_idx)
        file_chunks.append({"text": chunk.page_content.strip(), "source": source})

    return file_chunks





