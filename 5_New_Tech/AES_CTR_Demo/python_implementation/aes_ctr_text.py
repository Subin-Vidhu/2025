import os
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Settings
INPUT_TXT = Path('../sample.txt')  # Path to your input text file
OUTPUT_DIR = Path('.')
ENCRYPTED_DIR = OUTPUT_DIR / 'encrypted'
DECRYPTED_PARTS_DIR = OUTPUT_DIR / 'decrypted_parts'
KEY_FILE = OUTPUT_DIR / 'aes_key.bin'
NONCE_FILE = OUTPUT_DIR / 'aes_nonce.bin'

BLOCK_SIZE = 16  # AES block size in bytes
KEY_SIZE = 32    # 256 bits
NONCE_SIZE = 12  # 96 bits (like in your JS)


def save_bytes(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def load_bytes(filename):
    with open(filename, 'rb') as f:
        return f.read()

def encrypt_file(input_path, key, nonce):
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def decrypt_partial(input_path, key, nonce, offset, length):
    # Calculate the counter value for the offset
    initial_value = offset // BLOCK_SIZE
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=initial_value)
    block_offset = offset % BLOCK_SIZE
    with open(input_path, 'rb') as f:
        f.seek(offset - block_offset)
        encrypted_full = f.read(block_offset + length)
    decrypted_full = cipher.decrypt(encrypted_full)
    return decrypted_full[block_offset:block_offset+length]

def main():
    ENCRYPTED_DIR.mkdir(exist_ok=True)
    DECRYPTED_PARTS_DIR.mkdir(exist_ok=True)

    # Generate key and nonce (or load if already exist)
    if not KEY_FILE.exists():
        key = get_random_bytes(KEY_SIZE)
        save_bytes(KEY_FILE, key)
    else:
        key = load_bytes(KEY_FILE)
    if not NONCE_FILE.exists():
        nonce = get_random_bytes(NONCE_SIZE)
        save_bytes(NONCE_FILE, nonce)
    else:
        nonce = load_bytes(NONCE_FILE)

    print(f"Key: {KEY_FILE}, Nonce: {NONCE_FILE}")

    # Encrypt the text file
    if not INPUT_TXT.exists():
        print(f"Input file {INPUT_TXT} not found.")
        return
    print(f"Encrypting {INPUT_TXT.name} ...")
    ciphertext = encrypt_file(INPUT_TXT, key, nonce)
    enc_path = ENCRYPTED_DIR / f"{INPUT_TXT.name}.enc"
    save_bytes(enc_path, ciphertext)
    print(f"Saved encrypted file: {enc_path}")

    # Partial decryption test
    offset = 159  # Change as needed
    length = 753   # Change as needed
    decrypted_part = decrypt_partial(enc_path, key, nonce, offset, length)
    # Compare with original
    with open(INPUT_TXT, 'rb') as f:
        f.seek(offset)
        original_part = f.read(length)
    try:
        # Try to decode as UTF-8 for display
        decrypted_text = decrypted_part.decode('utf-8', errors='replace')
        original_text = original_part.decode('utf-8', errors='replace')
    except Exception:
        decrypted_text = str(decrypted_part)
        original_text = str(original_part)
    print(f"\nDecrypted text (offset {offset}, length {length}):\n{decrypted_text}")
    print(f"Original text (same range):\n{original_text}")
    if decrypted_part == original_part:
        print("\n✅ Partial decryption test PASSED!")
    else:
        print("\n❌ Partial decryption test FAILED!")
    # Save the decrypted part
    part_path = DECRYPTED_PARTS_DIR / f"{INPUT_TXT.name}.decrypted.part"
    save_bytes(part_path, decrypted_part)
    print(f"Saved decrypted part: {part_path}\n")

if __name__ == '__main__':
    main() 