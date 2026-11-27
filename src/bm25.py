import re
import math

import bm25s

bm25s.BM25.retrieve()

STOPWORDS = {
    "the", "a", "an", "is", "in", "it", "of", "and", "to", "for", 
    "with", "on", "as", "by", "this", "that", "are", "be", "or", 
    "from", "at", "which", "but", "not", "have", "has", "was", "were"
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9_]{2,}", text.lower()) # r"[a-zA-Z0-9_]+" splitting by -> one or more consecutive words until none are found, r"[a-zA-Z0-9_]{2,}" two or more consecutive words until none are found
    tokens = [word for word in words if word not in STOPWORDS]
    return tokens

def index(chunks: list[dict]) -> dict:
    inverse_index = {}
    docs_length = {}

    all_docs = len(chunks)

    for i, chunk in enumerate(chunks):
        tokenized = tokenize(chunk["text"])
        docs_length[str(i)] = len(tokenized)
        for token in tokenized:
            if token not in inverse_index:
                inverse_index[token] = {}
            if str(i) not in inverse_index[token]:
                inverse_index[token][str(i)] = 1
            else:
                inverse_index[token][str(i)] += 1

    # 2. Calculate Average Document Length (avgdl)
    # in order to calcu this,, we need len() of each document / all_docs
    avgdl = sum(doc_len for doc_len in docs_length.values()) / all_docs


    # 3. Calculate Inverse Document Frequency (IDF) for each token
    idf = {}
    # idf(tk) = log (1 + (N - df + 0.5 / df + 0.5))
    for token, freq in inverse_index.items():
        perfile = len(freq)
        # inverse_index[token]["idf"] = math.log(1 + ((all_docs - perfile + 0.5) / (perfile + 0.5)))
        idf[token] = math.log(1 + ((all_docs - perfile + 0.5) / (perfile + 0.5)))


    bm25_index = {
        "inverse_index": inverse_index,
        "docs_length": docs_length,
        "idf": idf,
        "avgdl": avgdl,
        "all_docs": all_docs
    }
    return bm25_index


def retreive(query: str, k: int, bm25_index: dict):
    tokenized_q = tokenize(query)
    scores = {}
    k1, b = 1.5, 0.75
    avgdl = bm25_index["avgdl"]
    for token in tokenized_q:
        if token not in bm25_index["inverse_index"]:
            continue
        chunks_freq = bm25_index["inverse_index"][token] # Dict[chunk_id: token_count] 
        token_idf = bm25_index["idf"][token]

        # For each token in query:
        # We acquire its IDF
        # We retrieve all chunks where the token was mentioned on.
        # For each chunk we count its score based on the token IDF * (token frequency on the chunk)
        # The score of the chunk can increase if other tokens in query are also mentioned in the same chunk


        for chunk, freq in chunks_freq.items():
            chunk_len = bm25_index["docs_length"][chunk]
            score = token_idf * ((freq * (k1 + 1)) / (freq + k1 * (1 - b + b*(chunk_len/avgdl))))
            if chunk not in scores:
                scores[chunk] = score
            else:
                scores[chunk] += score
            
    # result is scores of each chunk ("0", "1", "2"...) and their corresponding score based on the query
    # sorting the scores in descending order and returning the top k results
    top_sorted = sorted(scores.items(), key=lambda x:x[1], reverse=True) # sorting the second element of items() return sets of {key, val}

    result = [top_sorted[x] for x in range(k)]
    print(result)
    return result

    # return { for i, chunk in enumerate(scores)}


        




# After chunking >> a file chunks.json would be saved immediately contaning chunks and their metadata (frst_id, last_id, path)
## Tokenization >> 
# returning a list of strings that present each token as a string/word.
# passing a list of chunks would normally result in receiving a list of lists [["cat", "sleep"],["dreamt", "running"]...]
# next is the IDF and Inverse indexing so we take each word and calculate its IDF (its overall weight based on the chunks) and TF (how frequent it is across chunks)
