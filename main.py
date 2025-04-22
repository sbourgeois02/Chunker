import os
import argparse
from tqdm import tqdm

from utils.detect_filetype import get_handler_for_file
from chunking.chunker import chunk_text
from utils.io_helpers import save_chunks
from config import INPUT_DIR, OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(description="Chunk documents with overlap.")
    parser.add_argument("-i", "--input_dir", default=INPUT_DIR, help="Directory of input files")
    parser.add_argument("-o", "--output_dir", default=OUTPUT_DIR, help="Directory for output chunks")
    args = parser.parse_args()

    input_files = [
        os.path.join(args.input_dir, f)
        for f in os.listdir(args.input_dir)
        if os.path.isfile(os.path.join(args.input_dir, f))
    ]

    print(f"\n📦 Starting chunking for {len(input_files)} files...\n")

    # Top-level progress bar
    overall_bar = tqdm(total=len(input_files), desc="Overall Progress", position=0, leave=True, unit="file")

    for filepath in input_files:
        try:
            filename = os.path.basename(filepath)
            file_bar = tqdm(total=3, desc=f"{filename}", position=1, leave=False, unit="step")

            handler = get_handler_for_file(filepath)
            file_bar.update(1)

            text = handler.load_text(filepath)
            file_bar.update(1)

            chunks = chunk_text(text)
            save_chunks(filepath, chunks, args.output_dir)
            file_bar.update(1)

            file_bar.close()
            tqdm.write(f"✅ {filename} → {len(chunks)} chunks saved")

            overall_bar.update(1)

        except Exception as e:
            tqdm.write(f"❌ Error processing {filepath}: {e}")

    overall_bar.close()
    print("\n✅ All files processed.\n")


if __name__ == "__main__":
    main()