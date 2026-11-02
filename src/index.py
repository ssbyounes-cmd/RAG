from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

# 1. Prepare some sample markdown content
with open("data/raw/INFO.md", "r") as f:
    markdown_code = f.read()

# 2. Initialize the Python-specific splitter
# We set the chunk size strictly to 2000 as required, or lower for testing.
markdown_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,  # Using MARKDOWN for markdown code as a placeholder
    chunk_size=1000,  # Keeping it small to force a split for this test
    chunk_overlap=0
)

# 3. Create the chunks
markdown_chunks = markdown_splitter.create_documents([markdown_code])



result = []
for i, chunk in enumerate(markdown_chunks):
    # print(f"--- Chunk {i+1} ---")
    # print(chunk.page_content.strip())
    result.append(chunk.page_content.strip())
    # print()