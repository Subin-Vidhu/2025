from pathlib import Path


def compare_files(file1, file2, context=8):
    path1 = Path(file1)
    path2 = Path(file2)
    if not path1.exists() or not path2.exists():
        print(f"One or both files do not exist: {file1}, {file2}")
        return

    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        chunk_size = 4096
        offset = 0
        while True:
            b1 = f1.read(chunk_size)
            b2 = f2.read(chunk_size)
            if b1 != b2:
                # Find the first differing byte
                for i, (byte1, byte2) in enumerate(zip(b1, b2)):
                    if byte1 != byte2:
                        diff_offset = offset + i
                        print(f"Files differ at byte {diff_offset}: {byte1} (0x{byte1:02x}) != {byte2} (0x{byte2:02x})")
                        # Show context
                        context1 = b1[i:i+context]
                        context2 = b2[i:i+context]
                        print(f"File1 next {context} bytes: {[f'{b:02x}' for b in context1]}")
                        print(f"File2 next {context} bytes: {[f'{b:02x}' for b in context2]}")
                        return
                # If one file is longer
                if len(b1) != len(b2):
                    print(f"Files differ in length at offset {offset}")
                    return
            if not b1:  # End of both files
                break
            offset += chunk_size
    print("✅ Files are identical.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python file_compare.py <file1> <file2>")
    else:
        compare_files(sys.argv[1], sys.argv[2]) 