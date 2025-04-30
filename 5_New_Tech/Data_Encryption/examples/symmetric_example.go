package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"path/filepath"

	"medical_encryption/pkg/symmetric"
)

func main() {
	// Generate a new encryption key
	key, err := symmetric.GenerateKey()
	if err != nil {
		log.Fatalf("Failed to generate key: %v", err)
	}
	fmt.Printf("Generated Key: %s\n", key)

	// Read a sample DICOM file
	inputFile := filepath.Join("test_data", "1.2.840.113619.2.55.3.2831200001.555.1636080662.303.1.dcm")
	data, err := ioutil.ReadFile(inputFile)
	if err != nil {
		log.Fatalf("Failed to read file: %v", err)
	}

	// Encrypt the DICOM file
	encrypted, err := symmetric.Encrypt(data, key)
	if err != nil {
		log.Fatalf("Failed to encrypt: %v", err)
	}

	// Save the encrypted data
	encryptedFile := inputFile + ".enc"
	err = ioutil.WriteFile(encryptedFile, []byte(encrypted), 0644)
	if err != nil {
		log.Fatalf("Failed to write encrypted file: %v", err)
	}
	fmt.Printf("Encrypted file saved to: %s\n", encryptedFile)

	// Decrypt the data
	decrypted, err := symmetric.Decrypt(encrypted, key)
	if err != nil {
		log.Fatalf("Failed to decrypt: %v", err)
	}

	// Save the decrypted data
	decryptedFile := inputFile + ".dec"
	err = ioutil.WriteFile(decryptedFile, decrypted, 0644)
	if err != nil {
		log.Fatalf("Failed to write decrypted file: %v", err)
	}
	fmt.Printf("Decrypted file saved to: %s\n", decryptedFile)

	// Verify the decryption by comparing file sizes
	originalSize := len(data)
	decryptedSize := len(decrypted)
	if originalSize != decryptedSize {
		fmt.Printf("Warning: Size mismatch! Original: %d bytes, Decrypted: %d bytes\n", originalSize, decryptedSize)
	} else {
		fmt.Printf("Success! File sizes match: %d bytes\n", originalSize)
	}
}
