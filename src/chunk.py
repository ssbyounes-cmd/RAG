from src.chunk2 import splitter_python as force_split


class splitter_text:
    @staticmethod
    def textmd_chunker(text: str, seps: list[str], max: int) -> list[str]:
        result = []
        for sep in seps:
            chunks = text.split(sep)
            if all(len(chunk) <= max for chunk in chunks):
                sep_check = text.startswith(sep)
                break

        chunks = [c if (i == 0 and not sep_check) else sep + c for i, c in enumerate(chunks)]

        for chunk in chunks:
            if result and len(chunk + result[-1]) <= max:
                result[-1] = result[-1] + chunk
            else:
                result.append(chunk)


        # force slicing with max if necessary and overwrite result
        if any(len(chunk) > max for chunk in chunks):
            result = []
            for chunk in chunks:
                if len(chunk) > max:
                    result.extend(force_split.chunk_max(chunk, max))
                else:
                    result.append(chunk)

        return result





# with open("INFO.md", "r") as f:
#     content = f.read()

# res = splitter_text.textmd_chunker(content, [
#                 "\n#{1,6} ",
#                 "```\n",
#                 "\n\\*\\*\\*+\n",
#                 "\n---+\n",
#                 "\n___+\n",
#                 "\n\n",
#                 "\n",
#                 " "
#             ], 1000)

# for i, x in enumerate(res):
#     print(f"CHUNK {i}:\n{x}")
#     print("\n.........................................................................\n")