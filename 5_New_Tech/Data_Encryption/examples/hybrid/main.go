package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"

	"medical_encryption/pkg/asymmetric"
	"medical_encryption/pkg/hybrid"
)

// formatBytes converts bytes to human-readable format
func formatBytes(bytes int64) string {
	const unit = 1024
	if bytes < unit {
		return fmt.Sprintf("%d B", bytes)
	}
	div, exp := int64(unit), 0
	for n := bytes / unit; n >= unit; n /= unit {
		div *= unit
		exp++
	}
	return fmt.Sprintf("%.1f %cB", float64(bytes)/float64(div), "KMGTPE"[exp])
}

// printProgress prints a detailed progress bar with byte information
func printProgress(info hybrid.ProgressInfo) {
	width := 40
	filled := int(info.Progress * float64(width) / 100)
	bar := strings.Repeat("█", filled) + strings.Repeat("░", width-filled)

	processed := formatBytes(info.BytesProcessed)
	total := formatBytes(info.TotalBytes)

	// Clear the line first
	fmt.Print("\r\033[K")

	if info.Progress == 100 {
		// For 100% progress, print with newline
		fmt.Printf("%s [%s] %.1f%% (%s/%s)\n",
			info.Stage, bar, info.Progress, processed, total)
	} else {
		// For ongoing progress, print without newline
		fmt.Printf("%s [%s] %.1f%% (%s/%s)",
			info.Stage, bar, info.Progress, processed, total)
	}
}

func main() {
	// Create directory for storing keys if it doesn't exist
	keysDir := "keys"
	if err := os.MkdirAll(keysDir, 0755); err != nil {
		log.Fatalf("Failed to create keys directory: %v", err)
	}

	// Generate RSA key pair
	privateKey, publicKey, err := asymmetric.GenerateKeyPair(asymmetric.DefaultKeySize)
	if err != nil {
		log.Fatalf("Failed to generate key pair: %v", err)
	}

	// Read a sample DICOM file
	inputFile := filepath.Join("test_data", "1.2.840.113619.2.55.3.2831200001.555.1636080662.303.1.dcm")
	data, err := os.ReadFile(inputFile)
	if err != nil {
		log.Fatalf("Failed to read file: %v", err)
	}
	fmt.Printf("Original file size: %s\n", formatBytes(int64(len(data))))

	fmt.Println("\nEncrypting file...")
	startTime := time.Now()

	// Encrypt the DICOM file using hybrid encryption
	encryptedData, err := hybrid.Encrypt(publicKey, data, printProgress)
	if err != nil {
		log.Fatalf("Failed to encrypt: %v", err)
	}

	// Serialize the encrypted data
	fmt.Println("\nSerializing encrypted data...")
	serializedData := hybrid.SerializeEncryptedData(encryptedData, printProgress)

	// Save the encrypted data
	encryptedFile := inputFile + ".hybrid"
	if err := os.WriteFile(encryptedFile, serializedData, 0644); err != nil {
		log.Fatalf("Failed to write encrypted file: %v", err)
	}

	encryptionTime := time.Since(startTime)
	fmt.Printf("\nEncrypted file saved to: %s\n", encryptedFile)
	fmt.Printf("Encrypted file size: %s\n", formatBytes(int64(len(serializedData))))
	fmt.Printf("Encrypted AES key size: %s\n", formatBytes(int64(len(encryptedData.EncryptedAESKey))))
	fmt.Printf("Encryption time: %v\n", encryptionTime)
	fmt.Printf("Encryption speed: %.2f MB/s\n",
		float64(len(data))/1048576/encryptionTime.Seconds())

	// Read back the encrypted file
	fmt.Println("\nReading encrypted file...")
	encryptedBytes, err := os.ReadFile(encryptedFile)
	if err != nil {
		log.Fatalf("Failed to read encrypted file: %v", err)
	}

	// Deserialize the encrypted data
	fmt.Println("\nDeserializing data...")
	deserializedData, err := hybrid.DeserializeEncryptedData(encryptedBytes, printProgress)
	if err != nil {
		log.Fatalf("Failed to deserialize data: %v", err)
	}

	// Decrypt the data
	fmt.Println("\nDecrypting file...")
	startTime = time.Now()
	decryptedData, err := hybrid.Decrypt(privateKey, deserializedData, printProgress)
	if err != nil {
		log.Fatalf("Failed to decrypt: %v", err)
	}

	// Save the decrypted data
	decryptedFile := inputFile + ".dec"
	if err := os.WriteFile(decryptedFile, decryptedData, 0644); err != nil {
		log.Fatalf("Failed to write decrypted file: %v", err)
	}

	decryptionTime := time.Since(startTime)
	fmt.Printf("\nDecrypted file saved to: %s\n", decryptedFile)
	fmt.Printf("Decrypted file size: %s\n", formatBytes(int64(len(decryptedData))))
	fmt.Printf("Decryption time: %v\n", decryptionTime)
	fmt.Printf("Decryption speed: %.2f MB/s\n",
		float64(len(decryptedData))/1048576/decryptionTime.Seconds())

	// Verify the decryption by comparing file sizes
	if len(data) != len(decryptedData) {
		fmt.Printf("Warning: Size mismatch! Original: %s, Decrypted: %s\n",
			formatBytes(int64(len(data))), formatBytes(int64(len(decryptedData))))
	} else {
		fmt.Printf("Success! File sizes match: %s\n", formatBytes(int64(len(data))))
	}

	// Print the encryption overhead
	overhead := float64(len(serializedData)-len(data)) / float64(len(data)) * 100
	fmt.Printf("Encryption overhead: %.2f%%\n", overhead)
	fmt.Printf("Total processing time: %v\n", encryptionTime+decryptionTime)
}
