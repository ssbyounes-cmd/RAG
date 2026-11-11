import bm25s
import parser
import json


query = "fastest typer in the word"

# supposedly we already have a saved up bm25 index.
# retriever = bm25s.BM25.load("data/processed/")  # Load the index from disk for later use
# with open("data/processed/corpus.jsonl", "r") as f:
#     content = [json.loads(line) for line in f]
    
# retriever.corpus = [item["text"] for item in content]  # Load the corpus from the saved JSONL file
# query = "What is the class responsible for handling input?"
# query_tokens = bm25s.tokenize(query)
# docs, scores = retriever.retrieve(query_tokens, k=2)
# print(f"Top match: {docs[0, 0]} with score {scores[0, 0]:.2f}")
# print(f"\n\nSecond match: {docs[0, 1]} with score {scores[0, 1]:.2f}")
# exit(0)





corpus = parser.parse_files("data/raw")  # This is a dictionary of file names and their corresponding chunks
all_chunks = [chunk["text"] for chunk in corpus]

# 2. Tokenize the text. 
corpus_tokens = bm25s.tokenize(all_chunks)  # Tokenizing the chunks of text in the corpus
query_tokens = bm25s.tokenize(query)


# 3. Create the BM25 model 
# You can customize the scoring algorithm by supplying a method argument, e.g. method="lucene" or method="bm25l"
retriever = bm25s.BM25(corpus=all_chunks) # Initializing

# 4. Compute and index the matrices
retriever.index(corpus_tokens) # calculates the global Inverse Document Frequency (IDF) weights, and saves them into the retriever object's memory
# meaning putting an IDF score to each word based on the whole chunks and store them

# 5. Query the index

# retriever.save("data/processed/") # Saving the index to disk for later use

# Retrieve the top k results (k=2 here)
docs, scores = retriever.retrieve(query_tokens, k=2) # Calculating TF and the Final Score
# This takes the query tokens and extract scores for each chunk calculating how many times the words got repeated there.
# For each chunk, we take the words in the query and for each word we calculate its TF and multiply it by its IDF.
# Eventually we're gonna have all chunks with a certain score,, we retrieve top k

print(f"Top match: {docs[0, 0]} with score {scores[0, 0]:.2f}")

print(f"\n\nSecond match: {docs[0, 1]} with score {scores[0, 1]:.2f}")













# retriever.index(corpus_tokens)
# meaning putting an IDF score to each word based on the whole chunks and store them

# retriever.retrieve(query_tokens, k=2)
