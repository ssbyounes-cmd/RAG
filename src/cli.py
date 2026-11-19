import bm25s
from src.index import build_index
from src.search import search, search_data
from src.models import MinimalSource


class CLI:
    def index(self, max_chunk_size: int = 2000):
        """
        Indexes the text files in the specified path using the BM25 algorithm and saves the index to disk."""
        build_index(max_chunk_size)

    def search(self, query, k):
        """
        Searches the indexed text files for the specified query and returns the top k results."""
        result = search(query, k)
        print(f"Top {k} results for query '{query}':")
        for idx, item in enumerate(result):
            print(f"{idx + 1}. Path: {item.file_path}, First ID: {item.first_character_index}, Last ID: {item.last_character_index}")

    def search_dataset(self, queries: str, k: int, output: str):
        search_data(queries, k, output)
