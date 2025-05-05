# AES-CTR DICOM File Encryption & Partial Decryption (Python)

This project demonstrates how to encrypt DICOM files using AES in Counter Mode (CTR) and how to partially decrypt any segment of the encrypted file. It is designed for beginners and uses the [PyCryptodome](https://www.pycryptodome.org/) library.

---

## Table of Contents
- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [How Partial Decryption Works](#how-partial-decryption-works)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Code Explanation](#code-explanation)

---

## Overview

- **Encrypts all DICOM files** in a specified folder using AES-CTR (256-bit key, 96-bit nonce)
- **Saves encrypted files** in an `encrypted/` folder
- **Allows partial decryption** of any byte range from the encrypted file
- **Saves decrypted parts** in a `decrypted_parts/` folder
- **Verifies** that the decrypted part matches the original file

---

## Directory Structure

```
AES_CTR_Demo/
├── python_implementation/
│   ├── aes_ctr_dicom.py
│   ├── requirements.txt
│   ├── aes_key.bin
│   ├── aes_nonce.bin
│   ├── encrypted/
│   │   ├── ...dcm.enc
│   ├── decrypted_parts/
│   │   ├── ...dcm.decrypted.part
├── test_data/
│   ├── ...dcm
```

- Place your DICOM files in the `test_data/` folder.
- Run the script from inside `python_implementation/`.

---

## How It Works

1. **Key and Nonce Generation:**
   - Generates a random 256-bit AES key and 96-bit nonce (or loads them if they already exist).
   - Saves them as `aes_key.bin` and `aes_nonce.bin` for reuse.

2. **Encryption:**
   - Reads each `.dcm` file from `../test_data/`.
   - Encrypts the file using AES-CTR.
   - Saves the encrypted file as `encrypted/<original_name>.enc`.

3. **Partial Decryption & Verification:**
   - Decrypts a specific byte range (default: bytes 100-199) from the encrypted file.
   - Compares the decrypted part to the same range in the original file.
   - Prints whether the test passed or failed.
   - Saves the decrypted part as `decrypted_parts/<original_name>.decrypted.part`.

---

## Usage

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Place DICOM Files
- Put your `.dcm` files in the `test_data/` directory (one level up from `python_implementation/`).

### 3. Run the Script
```bash
cd python_implementation
python aes_ctr_dicom.py
```

### 4. Output
- Encrypted files will appear in `encrypted/`
- Decrypted parts will appear in `decrypted_parts/`
- Console output will show if partial decryption matches the original

---

## How Partial Decryption Works

- **AES-CTR** allows you to decrypt any part of the file independently.
- The script calculates which block to start from, sets the counter, and decrypts only the necessary bytes.
- This is efficient and does not require decrypting the whole file.

**Example:**
- To decrypt bytes 100-199:
  - The script finds the correct block and offset
  - Decrypts just enough data to cover the range
  - Extracts and saves the requested bytes

---

## Security Notes
- The AES key and nonce are generated securely and saved for reuse.
- The same key/nonce are used for all files in this demo (for real applications, use a new nonce per file).
- Encrypted files are the same size as the originals (no padding in CTR mode).
- This script is for educational/demo purposes; for production, use secure key management.

---

## Troubleshooting
- **No files found:**
  - Make sure your `.dcm` files are in the correct `test_data/` directory.
  - Check the `TEST_DATA_DIR` path in the script if you move folders.
- **Permission errors:**
  - Make sure you have write permissions in the `python_implementation/` directory.
- **Partial decryption test failed:**
  - Check that the key and nonce have not changed between encryption and decryption.

---

## Customization
- You can change the `offset` and `length` variables in the script to test other byte ranges.
- You can adapt the script to encrypt/decrypt other file types (not just DICOM).

---

## Code Explanation

Below is a detailed, beginner-friendly explanation of the main Python script (`aes_ctr_dicom.py`):

### 1. **Imports and Constants**
```python
import os
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
```
- **os, pathlib:** For file and folder operations.
- **Crypto.Cipher, Crypto.Random:** From PyCryptodome, used for AES encryption and secure random number generation.

```python
TEST_DATA_DIR = Path('../test_data')
OUTPUT_DIR = Path('.')
ENCRYPTED_DIR = OUTPUT_DIR / 'encrypted'
DECRYPTED_PARTS_DIR = OUTPUT_DIR / 'decrypted_parts'
KEY_FILE = OUTPUT_DIR / 'aes_key.bin'
NONCE_FILE = OUTPUT_DIR / 'aes_nonce.bin'
BLOCK_SIZE = 16  # AES block size in bytes
KEY_SIZE = 32    # 256 bits
NONCE_SIZE = 12  # 96 bits (like in your JS)
```
- **TEST_DATA_DIR:** Where your DICOM files are.
- **ENCRYPTED_DIR, DECRYPTED_PARTS_DIR:** Output folders for results.
- **KEY_FILE, NONCE_FILE:** Where the AES key and nonce are stored.
- **BLOCK_SIZE, KEY_SIZE, NONCE_SIZE:** Standard AES parameters.

### 2. **Helper Functions**

#### `save_bytes(filename, data)`
Saves binary data to a file.

#### `load_bytes(filename)`
Loads binary data from a file.

### 3. **Encryption Function**

#### `encrypt_file(input_path, key, nonce)`
- Reads the entire DICOM file as bytes.
- Creates an AES cipher in CTR mode with the given key and nonce.
- Encrypts the data and returns the ciphertext.

### 4. **Partial Decryption Function**

#### `decrypt_partial(input_path, key, nonce, offset, length)`
- Calculates which AES block contains the requested offset.
- Sets the counter (initial_value) for the cipher to match the block.
- Reads enough encrypted data to cover the requested range (including block alignment).
- Decrypts the data and extracts just the requested bytes.
- Returns the decrypted part.

### 5. **Main Function**

#### `main()`
- **Creates output folders** if they don't exist.
- **Loads or generates** the AES key and nonce, saving them for reuse.
- **For each DICOM file:**
  - Encrypts the file and saves it in `encrypted/`.
  - Decrypts a test range (bytes 100-199) from the encrypted file.
  - Compares the decrypted part to the original file's bytes 100-199.
  - Prints whether the test passed or failed.
  - Saves the decrypted part in `decrypted_parts/`.
- **Prints summary info** about the files processed.

### 6. **Script Entry Point**

```python
if __name__ == '__main__':
    main()
```
- This ensures the script runs the `main()` function when executed directly.

---

### **How the Code Works Together**
- The script is designed to be run as a batch process: it encrypts all DICOM files in the input folder, then tests partial decryption for each.
- The use of AES-CTR allows for efficient, random-access decryption of any part of the file.
- The code is modular, so you can easily adapt it to other file types or change the encryption parameters.

---

**If you want a line-by-line walkthrough or have questions about any part, just ask!**

---

## License
This code is provided for educational purposes. Use at your own risk. 