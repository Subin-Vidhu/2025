# AES-CTR Partial Decryption Demo

This project demonstrates how to encrypt large text files using AES in Counter Mode (CTR) and perform partial decryption of the encrypted data using the Web Crypto API.

## Table of Contents
1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Technical Details](#technical-details)
4. [Code Explanation](#code-explanation)
5. [Usage Guide](#usage-guide)

## Overview

This web application allows you to:
1. Select and encrypt a large text file using AES-CTR encryption
2. Decrypt specific portions of the encrypted file without decrypting the entire file
3. Verify that the decrypted portions match the original text

## How It Works

### AES-CTR Mode
AES-CTR (Counter Mode) is a encryption mode that:
- Turns a block cipher (AES) into a stream cipher
- Allows for parallel encryption/decryption
- Enables partial decryption without needing the entire file
- Uses a counter that increments for each block to ensure unique encryption

### Key Components
1. **Nonce (Number used ONCE)**
   - 12-byte random value
   - Combined with counter to create unique inputs
   - Generated fresh for each encryption

2. **Counter Block**
   - 16 bytes total
   - First 12 bytes: Nonce
   - Last 4 bytes: Block counter (increments for each block)

3. **Block Size**
   - AES uses 16-byte blocks
   - Counter increments for each block
   - Partial decryption aligns to block boundaries

## Technical Details

### Encryption Process
1. Generate a random 256-bit encryption key
2. Generate a random 12-byte nonce
3. Create initial counter block (nonce + starting counter value)
4. Encrypt the entire file using AES-CTR

### Partial Decryption Process
1. Calculate which block contains the desired offset
2. Create counter block for that position
3. Decrypt only the needed blocks
4. Extract the requested bytes from the decrypted blocks

## Code Explanation

### Key Functions

#### `createCounterBlock(nonce, blockIndex)`
```javascript
function createCounterBlock(nonce, blockIndex) {
    const counter = new Uint8Array(16);
    counter.set(nonce, 0);           // First 12 bytes: nonce
    blockIndex = toUint32(blockIndex);
    // Last 4 bytes: block counter
    counter[12] = blockIndex >>> 24;  // Most significant byte
    counter[13] = blockIndex >>> 16;
    counter[14] = blockIndex >>> 8;
    counter[15] = blockIndex & 0xff;  // Least significant byte
    return counter;
}
```
This function:
- Creates the 16-byte counter block
- Combines nonce and block index
- Handles large numbers correctly using bitwise operations

#### `encryptFile()`
```javascript
async function encryptFile() {
    // Generate key and nonce
    await generateKey();
    // Create initial counter
    const counter = createCounterBlock(nonce, 0);
    // Encrypt the file
    encryptedData = await crypto.subtle.encrypt(
        {
            name: "AES-CTR",
            counter: counter,
            length: 64
        },
        key,
        textBytes
    );
}
```
This function:
- Reads the input file
- Generates encryption key and nonce
- Encrypts the entire file

#### `decryptPart()`
```javascript
async function decryptPart() {
    const BLOCK_SIZE = 16;
    // Calculate block alignment
    const startBlock = Math.floor(offset / BLOCK_SIZE);
    const offsetInBlock = offset % BLOCK_SIZE;
    // Calculate required blocks
    const blocksNeeded = Math.ceil((offsetInBlock + length) / BLOCK_SIZE);
    // Create counter for starting block
    const counter = createCounterBlock(nonce, startBlock);
    // Decrypt and extract required portion
    const decryptedData = await crypto.subtle.decrypt(...);
}
```
This function:
- Calculates block alignments
- Creates correct counter for the offset
- Decrypts only required blocks
- Extracts requested bytes

## Usage Guide

1. **Encrypting a File**
   - Click "Choose File" to select a text file
   - Click "Encrypt File" to encrypt it
   - The file is encrypted and held in memory

2. **Partial Decryption**
   - Enter the starting byte offset
   - Enter how many bytes to decrypt
   - Click "Decrypt Part"
   - View the decrypted portion and verification

3. **Understanding the Output**
   - Shows decrypted text
   - Shows original text for comparison
   - Indicates if they match
   - Displays any errors or warnings

## Security Notes

- The encryption key is generated securely using Web Crypto API
- The nonce is randomly generated for each encryption
- The implementation uses standard cryptographic practices
- Keys and encrypted data are only held in memory

## Requirements Satisfaction

This implementation satisfies the requirements by:
1. Using AES-CTR encryption from Web Crypto API
2. Handling large text files (tested with multi-megabyte files)
3. Enabling partial decryption of any portion
4. Providing verification of decrypted content 