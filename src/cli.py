import bm25s
from src.parser import parse_files


class CLI:
    def index(self, path):
        """
        Indexes the text files in the specified path using the BM25 algorithm and saves the index to disk."""
        corpus = parse_files(path)
        all_chunks = [chunk["text"] for chunk in corpus]
        corpus_tokens = bm25s.tokenize(all_chunks)  # Tokenizing the chunks of text in the corpus
        retriever = bm25s.BM25(corpus=all_chunks)
        retriever.index(corpus_tokens)
        retriever.save("data/processed/")