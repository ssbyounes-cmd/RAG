import bm25s

# 1. Prepare your data blocks
corpus = [
    "a cat is a feline and likes to purr",
    "a dog is the human's best friend and loves to play",
    "a bird is a beautiful animal that can fly",
]
query = "does the fish purr like a cat?"

# 2. Tokenize the text. 
corpus_tokens = bm25s.tokenize(corpus)
query_tokens = bm25s.tokenize(query)


# 3. Create the BM25 model 
# You can customize the scoring algorithm by supplying a method argument, e.g. method="lucene" or method="bm25l"
retriever = bm25s.BM25(corpus=corpus) # Initializing

# 4. Compute and index the matrices
retriever.index(corpus_tokens) # calculates the global Inverse Document Frequency (IDF) weights, and saves them into the retriever object's memory
# meaning putting an IDF score to each word based on the whole chunks and store them

# 5. Query the index



# Retrieve the top k results (k=2 here)
docs, scores = retriever.retrieve(query_tokens, k=2) # Calculating TF and the Final Score
# This takes the query tokens and extract scores for each chunk calculating how many times the words got repeated there.
# For each chunk, we take the words in the query and for each word we calculate its TF and multiply it by its IDF.
# Eventually we're gonna have all chunks with a certain score,, we retrieve top k

print(f"Top match: {docs[0, 0]} with score {scores[0, 0]:.2f}")













# retriever.index(corpus_tokens)
# meaning putting an IDF score to each word based on the whole chunks and store them

# retriever.retrieve(query_tokens, k=2)
