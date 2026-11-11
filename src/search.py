import bm25s
import json
from src.models import MinimalSource
from src.models import MinimalSearchResults

def search(query: str, k: int):
    with open("data/processed/chunks.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    # lst_chunks = [chunk["text"] for chunk in json_data]
    retriever = bm25s.BM25.load("data/processed", load_corpus=False)
    # retriever.corpus = lst_chunks
    query_tokens = bm25s.tokenize(query)
    docs, _ = retriever.retrieve(query_tokens, k=k)
    
    # Create a list of the top k search results
    topk: list[dict] = []
    for chunk_id in docs[0]:
        matched_chunk = json_data[chunk_id]
        source = MinimalSource(**matched_chunk["source"])

        topk.append({"path": source.file_path, "first_id": source.first_character_index, "last_id": source.last_character_index})
    # We need to retrieve the indices of the chunks as well from the saved up chunks.json

    return topk
