import re

STOPWORDS = {
    "the", "a", "an", "is", "in", "it", "of", "and", "to", "for", 
    "with", "on", "as", "by", "this", "that", "are", "be", "or", 
    "from", "at", "which", "but", "not", "have", "has", "was", "were"
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9_]{2,}", text.lower()) # r"[a-zA-Z0-9_]+" splitting by -> one or more consecutive words until none are found, r"[a-zA-Z0-9_]{2,}" two or more consecutive words until none are found
    tokens = [word for word in words if word not in STOPWORDS]
    return tokens

def index(chunks: list[dict]):
    inverse_index = {}
    docs_length = {}

    all_docs = len(chunks)

    for i, chunk in enumerate(chunks):
        tokenized = tokenize(chunk["text"])
        docs_length[f"chunk_{i}"] = len(tokenized)
        for token in tokenized:
            if token not in inverse_index:
                inverse_index[token] = {}
            if f"chunk_{i}" not in inverse_index[token]:
                inverse_index[token][f"chunk_{i}"] = 1
            else:
                inverse_index[token][f"chunk_{i}"] += 1

    # 2. Calculate Average Document Length (avgdl)
    # in order to calcu this,, we need len() of each document / all_docs
    avgdl = sum(doc_len for doc_len in docs_length.values()) / all_docs


    # 3. Calculate Inverse Document Frequency (IDF) for each token
    idf = {}
    # print(avgdl)

  
    exit(0)


        




# After chunking >> a file chunks.json would be saved immediately contaning chunks and their metadata (frst_id, last_id, path)
## Tokenization >> 
# returning a list of strings that present each token as a string/word.
# passing a list of chunks would normally result in receiving a list of lists [["cat", "sleep"],["dreamt", "running"]...]
# next is the IDF and Inverse indexing so we take each word and calculate its IDF (its overall weight based on the chunks) and TF (how frequent it is across chunks)
