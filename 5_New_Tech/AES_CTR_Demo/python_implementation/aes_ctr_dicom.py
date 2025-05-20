import os
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

TEST_DATA_DIR = Path('../test_data')
OUTPUT_DIR = Path('.')
ENCRYPTED_DIR = OUTPUT_DIR / 'encrypted'
DECRYPTED_PARTS_DIR = OUTPUT_DIR / 'decrypted_parts'
DECRYPTED_FULL_DIR = OUTPUT_DIR / 'decrypted_full'  # New directory for fully decrypted files
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

def decrypt_full(input_path, key, nonce):
    """Decrypt an entire encrypted file using AES-CTR mode."""
    with open(input_path, 'rb') as f:
        ciphertext = f.read()
    # Create a new cipher instance with initial counter value of 0
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=0)
    # Decrypt the entire file in one operation
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def decrypt_partial(input_path, key, nonce, offset, length):
    with open(input_path, 'rb') as f:
        f.seek(offset)
        # Read enough bytes to cover the requested range
        encrypted_part = f.read(length)
    # Calculate the counter value for the offset
    initial_value = offset // BLOCK_SIZE
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=initial_value)
    # Decrypt from the start of the block, then slice
    block_offset = offset % BLOCK_SIZE
    # Read enough to cover the block alignment
    with open(input_path, 'rb') as f:
        f.seek(offset - block_offset)
        encrypted_full = f.read(block_offset + length)
    decrypted_full = cipher.decrypt(encrypted_full)
    return decrypted_full[block_offset:block_offset+length]

def main():
    # Create output directories if they don't exist
    ENCRYPTED_DIR.mkdir(exist_ok=True)
    DECRYPTED_PARTS_DIR.mkdir(exist_ok=True)
    DECRYPTED_FULL_DIR.mkdir(exist_ok=True)  # Create directory for fully decrypted files

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

    # Encrypt all DICOM files
    for dicom_file in TEST_DATA_DIR.glob('*.dcm'):
        print(f"Encrypting {dicom_file.name} ...")
        ciphertext = encrypt_file(dicom_file, key, nonce)
        enc_path = ENCRYPTED_DIR / f"{dicom_file.name}.enc"
        save_bytes(enc_path, ciphertext)
        print(f"Saved encrypted file: {enc_path}")

        # Test partial decryption
        # Let's try to decrypt bytes 100-199 (100 bytes)
        offset = 100
        length = 100
        decrypted_part = decrypt_partial(enc_path, key, nonce, offset, length)
        # Compare with original
        with open(dicom_file, 'rb') as f:
            f.seek(offset)
            original_part = f.read(length)
        if decrypted_part == original_part:
            print(f"Partial decryption test PASSED for {dicom_file.name} (offset {offset}, length {length})")
        else:
            print(f"Partial decryption test FAILED for {dicom_file.name} (offset {offset}, length {length})")
        # Save the decrypted part
        part_path = DECRYPTED_PARTS_DIR / f"{dicom_file.name}.decrypted.part"
        save_bytes(part_path, decrypted_part)
        print(f"Saved decrypted part: {part_path}")

        # Test full decryption
        print(f"Fully decrypting {enc_path.name} ...")
        decrypted_full_data = decrypt_full(enc_path, key, nonce)
        full_path = DECRYPTED_FULL_DIR / f"{dicom_file.name}.decrypted"
        save_bytes(full_path, decrypted_full_data)
        # Compare with original
        with open(dicom_file, 'rb') as f:
            original_data = f.read()
        if decrypted_full_data == original_data:
            print(f"Full decryption test PASSED for {dicom_file.name}")
        else:
            print(f"Full decryption test FAILED for {dicom_file.name}")
        print(f"Saved fully decrypted file: {full_path}\n")

    print("Looking for DICOM files in:", TEST_DATA_DIR.resolve())
    print("Found files:", list(TEST_DATA_DIR.glob('*.dcm')))

if __name__ == '__main__':
    main() 