# chunking/chunker.py

import re
from config import MAX_WORDS, OVERLAP_SENTENCES, MAX_OVERLAP_WORDS, MIN_NEW_WORDS

def split_into_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)

def chunk_text(text):
    sentences = split_into_sentences(text)
    return chunk_text_with_overlap(sentences)

def chunk_text_with_overlap(sentences, min_new_words=MIN_NEW_WORDS, max_total_words=MAX_WORDS, overlap_sentences=OVERLAP_SENTENCES, max_overlap_words=MAX_OVERLAP_WORDS):
    chunks = []
    i = 0

    while i < len(sentences):
        new_chunk = []
        new_word_count = 0

        while i < len(sentences):
            sentence = sentences[i].strip()
            if sentence:
                new_chunk.append(sentence)
                new_word_count += len(sentence.split())
            i += 1
            if new_word_count >= min_new_words:
                break

        while i < len(sentences) and new_word_count < (max_total_words - max_overlap_words):
            sentence = sentences[i].strip()
            if sentence:
                new_chunk.append(sentence)
                new_word_count += len(sentence.split())
            i += 1

        new_content = " ".join(new_chunk)

        if not chunks:
            chunks.append(new_content)
            continue

        prev_sentences = split_into_sentences(chunks[-1])
        overlap = []
        word_total = 0
        count = 0

        for s in reversed(prev_sentences):
            words = s.strip().split()
            if count < overlap_sentences:
                if word_total + len(words) <= max_overlap_words:
                    overlap.insert(0, s.strip())
                    word_total += len(words)
                    count += 1
                else:
                    remaining = max_overlap_words - word_total
                    if remaining > 0:
                        truncated = " ".join(words[-remaining:])
                        overlap.insert(0, truncated.strip())
                    break
            else:
                break

        full_chunk = " ".join(overlap + split_into_sentences(new_content))
        chunks.append(full_chunk)

    return chunks