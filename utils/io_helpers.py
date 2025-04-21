# utils/io_helpers.py

from pathlib import Path

def save_chunks(filepath, chunks, output_folder):
    base_name = Path(filepath).stem
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    for i, chunk in enumerate(chunks):
        filename = output_path / f"{base_name}_chunk_{i+1:03}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chunk)