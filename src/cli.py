import bm25s
from src.index import build_index


class CLI:
    def index(self, max_chunk_size: int = 1000):
        """
        Indexes the text files in the specified path using the BM25 algorithm and saves the index to disk."""
        build_index(max_chunk_size)

    def search(self, query, k):
        """
        Searches the indexed text files for the specified query and returns the top k results."""
        pass