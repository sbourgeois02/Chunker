import re
from pathlib import Path

def split_into_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)

def chunk_text_with_overlap(sentences, min_new_words=250, max_total_words=425, overlap_sentences=2, max_overlap_words=50):
    chunks = []
    i = 0

    while i < len(sentences):
        new_chunk = []
        new_word_count = 0

        # Build new content (must be at least `min_new_words`)
        start_i = i
        while i < len(sentences):
            sentence = sentences[i].strip()
            if sentence:
                new_chunk.append(sentence)
                new_word_count += len(sentence.split())
            i += 1
            if new_word_count >= min_new_words:
                break

        # Fill up to max_total_words (including overlap later)
        while i < len(sentences) and new_word_count < (max_total_words - max_overlap_words):
            sentence = sentences[i].strip()
            if sentence:
                new_chunk.append(sentence)
                new_word_count += len(sentence.split())
            i += 1

        new_content = " ".join(new_chunk)

        # Get overlap from previous chunk
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
                    # Include part of the sentence to cap at 50 words
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

def save_chunks_to_txt(chunks, base_name, output_folder):
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    for i, chunk in enumerate(chunks):
        filename = output_path / f"{base_name}_chunk_{i+1:03}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chunk)

def process_text_file(input_file, output_folder):
    base_name = Path(input_file).stem
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = split_into_sentences(text)
    chunks = chunk_text_with_overlap(sentences)
    save_chunks_to_txt(chunks, base_name, output_folder)

def process_folder(input_folder, output_folder):
    input_path = Path(input_folder)
    for file in input_path.glob("*.txt"):
        print(f"Processing {file.name}...")
        process_text_file(file, output_folder)
    print("All files processed.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python chunker.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    process_folder(input_folder, output_folder)