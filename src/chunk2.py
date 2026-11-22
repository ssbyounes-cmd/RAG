
class splitter_python:
    @staticmethod
    def chunk_max(text: str, max: int) -> list[str]:
        static_chunk = []
        if len(text) > max:
            current, rest = text[:max], text[max:]
            static_chunk.append(current)
            if len(rest) > max:
                static_chunk.extend(splitter_python.chunk_max(rest, max))
            else:
                static_chunk.append(rest)
        return static_chunk

    @staticmethod
    def final_merge(chunks: list[str], max):
        i = 0
        while(i < len(chunks) - 1):
            new_chunk = chunks[i] + chunks[i+1]
            if len(new_chunk) > max:
                i += 1
                continue
            chunks.pop(i+1)
            chunks[i] = new_chunk
        return chunks

    @staticmethod
    def chunker(text: str, seps: list[str], max: int, i: int=0) -> list[str]:
        all = []
        sep_start = text.startswith(seps[i])

        chunks = text.split(seps[i])

        chunks = [chunk if (c == 0 and not sep_start) else seps[i] + chunk for c, chunk in enumerate(chunks)]

        chunks = splitter_python.final_merge(chunks, max)

        for chunk in chunks:
            if len(chunk) > max and i + 1 < len(seps):
                all.extend(splitter_python.chunker(chunk, seps, max, i + 1))
            elif len(chunk) > max and i + 1 == len(seps):
                all.extend(splitter_python.chunk_max(chunk, max))
            else:
                all.append(chunk)

        return all





# with open("type.py", "r") as f:
#     content = f.read()


# res = chunker(content, ["\nclass ", "\ndef ", "\n\n", "\n", " "], 1000)


# for i, x in enumerate(res):
#     print(f"CHUNK {i}:\n{x}")
#     print("\n.........................................................................\n")

# all = ""

# all = all.join(x for x in res)


# print(len(all) == len(content))
# print(all == content)

# print(max(len(x) for x in res) < 1000)