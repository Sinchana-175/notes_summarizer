from app import clean_text, split_text

def test_clean_text():
    raw_text = "This is some text.\nIt has line breaks and    extra spaces. - Also a dash."
    expected = "This is some text. It has line breaks and extra spaces. Also a dash."

    assert clean_text(raw_text) == expected

def test_split_text_small():
    text = "Sentence one. Sentence two! Sentence three?"
    chunks = split_text(text, chunk_size=50)

    # "Sentence one." (13) + " Sentence two!" (14) = 27 < 50
    # " Sentence three?" (16) + 27 = 43 < 50
    # So it should all fit in one chunk.
    assert len(chunks) == 1
    assert chunks[0] == "Sentence one. Sentence two! Sentence three?"

def test_split_text_large():
    # Constructing a scenario to force multiple chunks
    s1 = "This is a moderately long sentence." # len 35
    s2 = " This is another moderately long sentence." # len 42
    s3 = " And this is the third sentence that will push it." # len 50

    text = s1 + s2 + s3
    chunks = split_text(text, chunk_size=50)

    # chunk 1: s1 -> len 35. s1 + s2 -> len 77 > 50, so break.
    # chunk 2: s2 -> len 42. s2 + s3 -> len 92 > 50, so break.
    # chunk 3: s3 -> len 50.

    assert len(chunks) == 3
    assert chunks[0] == s1
    assert chunks[1] == s2.strip() # note: the logic splits by spaces and re-joins, leading to stripped leading spaces if it's the first in chunk
