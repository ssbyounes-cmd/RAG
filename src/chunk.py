static_chunk = []

def chunk_text(text: str, max: int, sep: list[str], id: int=0) -> list[str]:
    # having no separators inside text will just lead to infitite recursion
    if all(x not in content for x in sep):
        return text
    # print(all(x not in text for x in sep))
    # exit(0)

    if sep[id] in text:
        prev, after = text[:text.index(sep[id])], text[text.index(sep[id]):]
        text = after
        # in case we just begin chunking and there is a whole lot of comments top file
        if all(s not in prev for s in sep):
            if len(prev) > max:
                prev = prev[:max]
            static_chunk.append(prev)
    if len(text) > max:
        id += 1
    else:
        static_chunk.append(text)

    if text.strip():
        chunk_text(text, max, id)


with open("type.py", "r") as f:
    content = f.read()

chunk_text(content, 200, ["\nclass ", "\ndef ", "\n\n", "\n", " "])
    