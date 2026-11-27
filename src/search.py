import bm25s
import json, os
from src.models import MinimalSource, RagDataset
from src.models import AnsweredQuestion, UnansweredQuestion, MinimalSearchResults, StudentSearchResults
from src.index import prep
from src.bm25 import tokenize, retreive



def search(query: str, k: int) -> list[MinimalSource]:
    with open("data/processed/bm25_index.json", "r") as f:
        bm25_index = json.load(f)

    scores = retreive(query, k, bm25_index)

    with open("data/processed/chunks.json", "r") as f:
        chunks: list[dict] = json.load(f)

    topk = []
    for score in scores:
        chunk_id = int(score[0])
        topk.append(MinimalSource(**chunks[chunk_id]["source"]))

    return topk
    




def search_data(dataset_path: str, k: int, save_directory: str):
    ...

    



























































# loading indexed data and creating the retriever

# def load_index():
#     return bm25s.BM25.load("data/processed", load_corpus=True)




# def search(query: str, k: int, retriever=None) -> list[MinimalSource]:
#     if retriever is None:
#         retriever = load_index()

#     query_tokens = bm25s.tokenize([prep(query)], stopwords="en")
#     docs, _ = retriever.retrieve(query_tokens, k=k)

#     # Create a list of the top k search results
#     topk: list[MinimalSource] = []
#     for chunk in docs[0]:
#         source = MinimalSource(**chunk["source"])
#         topk.append(source)

#     return topk


# def search_data(dataset_path: str, k: int, save_directory: str):
#     retreiver = load_index()
#     with open(dataset_path, "r") as f:
#         all_query = json.load(f)
#     ragsets = RagDataset(**all_query)
#     results: list[MinimalSearchResults] = []
#     for query in ragsets.rag_questions:
#         question_id = query.question_id
#         question = query.question
#         minsrc = search(question, k, retreiver)
#         results.append(MinimalSearchResults(question_id=question_id, question=question, retrieved_sources=minsrc))


#     os.makedirs(save_directory, exist_ok=True)

#     with open(save_directory + "search_results.json", "w") as f:
#         json.dump(StudentSearchResults(search_results=results, k=k).model_dump(), f, indent=4)
