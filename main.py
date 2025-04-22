# main.py

import os
import argparse
from utils.detect_filetype import get_handler_for_file
from chunking.chunker import chunk_text
from utils.io_helpers import save_chunks
from config import OUTPUT_DIR,INPUT_DIR

def process_file(filepath, output_dir):
    handler = get_handler_for_file(filepath)
    text = handler.load_text(filepath)
    chunks = chunk_text(text)
    save_chunks(filepath, chunks, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Chunk documents with overlap.")
    parser.add_argument("-i", "--input_dir", default=INPUT_DIR, help="Directory of input files")
    parser.add_argument("-o", "--output_dir", default=OUTPUT_DIR, help="Directory for output chunks")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for filename in os.listdir(args.input_dir):
        filepath = os.path.join(args.input_dir, filename)
        if os.path.isfile(filepath):
            try:
                print(f"Processing {filename}...")
                process_file(filepath, args.output_dir)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()