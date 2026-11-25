STOPWORDS = {
    "the", "a", "an", "is", "in", "it", "of", "and", "to", "for", 
    "with", "on", "as", "by", "this", "that", "are", "be", "or", 
    "from", "at", "which", "but", "not", "have", "has", "was", "were"
}


def tokenize(text: str) -> list[str]:
    text = text.replace("_", " ")
    tokens = [word for word in text.split() if word not in STOPWORDS]
    return tokens

def index(tokens: list):
    ...




# After chunking >> a file chunks.json would be saved immediately contaning chunks and their metadata (frst_id, last_id, path)
## Tokenization >> 
# returning a list of strings that present each token as a string/word.
# passing a list of chunks would normally result in receiving a list of lists [["cat", "sleep"],["dreamt", "running"]...]
# next is the IDF and Inverse indexing so we take each word and calculate its IDF (its overall weight based on the chunks) and TF (how frequent it is across chunks)
