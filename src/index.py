from src.parser import parse_files
import bm25s
import json
import os
import re


# only apply for code files
def prep(text: str) -> str:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)  # camelCase -> camel Case
    text = text.replace("_", " ")                          # snake_case -> snake case
    return text


def build_index(max_chunk_size):
    corpus = parse_files("data/raw", max_chunk_size)  # Parsing the files in the specified path and creating a corpus of text chunks
    all_chunks = [prep(chunk["text"]) for chunk in corpus]
    corpus_tokens = bm25s.tokenize(all_chunks, show_progress=True, stopwords="en")  # Tokenizing the chunks of text in the corpus
    retriever = bm25s.BM25(corpus=corpus)
    retriever.index(corpus_tokens)
    retriever.save("data/processed/")

    os.makedirs("data/processed", exist_ok=True)
    # with open("data/processed/chunks.json", "w") as f:
    #    json.dump([{"text": chunk["text"], "source": chunk["source"].model_dump()} for chunk in corpus], f, indent=4)
