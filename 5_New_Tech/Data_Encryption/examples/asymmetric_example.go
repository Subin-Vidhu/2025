package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	"medical_encryption/pkg/asymmetric"
)

func main() {
	// Create directory for storing keys
	keysDir := "keys"
	if err := os.MkdirAll(keysDir, 0755); err != nil {
		log.Fatalf("Failed to create keys directory: %v", err)
	}

	// Generate RSA key pair
	privateKey, publicKey, err := asymmetric.GenerateKeyPair(asymmetric.DefaultKeySize)
	if err != nil {
		log.Fatalf("Failed to generate key pair: %v", err)
	}

	// Export keys to PEM format
	publicPEM, err := asymmetric.ExportPublicKeyToPEM(publicKey)
	if err != nil {
		log.Fatalf("Failed to export public key: %v", err)
	}
	privatePEM := asymmetric.ExportPrivateKeyToPEM(privateKey)

	// Save keys to files
	pubKeyFile := filepath.Join(keysDir, "public.pem")
	privKeyFile := filepath.Join(keysDir, "private.pem")

	if err := os.WriteFile(pubKeyFile, publicPEM, 0644); err != nil {
		log.Fatalf("Failed to save public key: %v", err)
	}
	if err := os.WriteFile(privKeyFile, privatePEM, 0600); err != nil {
		log.Fatalf("Failed to save private key: %v", err)
	}

	fmt.Printf("Keys generated and saved in %s directory\n", keysDir)

	// Example data to encrypt (in practice, this could be a small sensitive field from DICOM)
	sensitiveData := []byte("Patient ID: 12345, DOB: 1990-01-01")
	fmt.Printf("Original data: %s\n", sensitiveData)

	// Encrypt the data
	encryptedData, err := asymmetric.Encrypt(publicKey, sensitiveData)
	if err != nil {
		log.Fatalf("Failed to encrypt: %v", err)
	}
	fmt.Printf("Encrypted data length: %d bytes\n", len(encryptedData))

	// Decrypt the data
	decryptedData, err := asymmetric.Decrypt(privateKey, encryptedData)
	if err != nil {
		log.Fatalf("Failed to decrypt: %v", err)
	}
	fmt.Printf("Decrypted data: %s\n", decryptedData)

	// Demonstrate loading keys from files
	fmt.Println("\nDemonstrating key loading from files...")

	// Load public key
	loadedPubKeyPEM, err := os.ReadFile(pubKeyFile)
	if err != nil {
		log.Fatalf("Failed to read public key file: %v", err)
	}
	loadedPublicKey, err := asymmetric.ImportPublicKeyFromPEM(loadedPubKeyPEM)
	if err != nil {
		log.Fatalf("Failed to import public key: %v", err)
	}

	// Load private key
	loadedPrivKeyPEM, err := os.ReadFile(privKeyFile)
	if err != nil {
		log.Fatalf("Failed to read private key file: %v", err)
	}
	loadedPrivateKey, err := asymmetric.ImportPrivateKeyFromPEM(loadedPrivKeyPEM)
	if err != nil {
		log.Fatalf("Failed to import private key: %v", err)
	}

	// Test encryption/decryption with loaded keys
	newData := []byte("Testing loaded keys")
	encryptedWithLoaded, err := asymmetric.Encrypt(loadedPublicKey, newData)
	if err != nil {
		log.Fatalf("Failed to encrypt with loaded key: %v", err)
	}

	decryptedWithLoaded, err := asymmetric.Decrypt(loadedPrivateKey, encryptedWithLoaded)
	if err != nil {
		log.Fatalf("Failed to decrypt with loaded key: %v", err)
	}

	fmt.Printf("Test with loaded keys successful: %s\n", decryptedWithLoaded)
}
