from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language, MarkdownTextSplitter
from src.models import MinimalSource
from typing import Any
from tqdm import tqdm
from src.chunk2 import splitter_python
from src.chunk import splitter_text


def parse_files(files_path, max_chunk_size: int = 2000) -> list[dict[str, Any]]:
    files = Path(files_path)
    register: list[dict[str, Any]] = []
    files = [f for f in files.rglob("*") if f.suffix in [".md", ".txt", ".py"]]
    for file in tqdm(files, desc="Indexing", unit="file"):
        # Split the file content into chunks
        if file.suffix in [".md", ".txt"]:
            splitter = splitter_text()
        else:
            splitter = splitter_python()
        register.extend(chunk_file(file, splitter))
    return register




def chunk_file(file: Path, splitter: MarkdownTextSplitter | RecursiveCharacterTextSplitter | splitter_python | splitter_text) -> list[dict[str, Any]]:
    try:
        file_content = file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    
    if type(splitter) == splitter_text:
        # chunks = splitter.create_documents([file_content])
        seps = ["\n#{1,6} ", "```\n", "\n\\*\\*\\*+\n", "\n---+\n", "\n___+\n", "\n\n", "\n", " "]
        chunks = splitter.textmd_chunker(file_content, seps, 2000)
    else:
        seps = ["\nclass ", "\ndef ", "\n\tdef ", "\n\n", "\n", " ", ""]
        chunks = splitter.chunker(file_content, seps, 2000)

    file_chunks: list[dict[str, Any]] = []
    last_idx = 0
    for chunk in chunks:
        chunk_content = chunk.page_content if type(chunk) != str else chunk

        first_idx = file_content.find(chunk_content, last_idx)
        if first_idx == -1:
            first_idx = last_idx
        last_idx = first_idx + len(chunk_content)
        source = MinimalSource(
            file_path=str(file),
              first_character_index=first_idx,
                last_character_index=last_idx)
        file_chunks.append({"source": source.model_dump(), "text": chunk.page_content.strip() if type(chunk) != str else chunk})

    return file_chunks





