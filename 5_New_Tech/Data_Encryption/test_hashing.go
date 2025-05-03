package main

import (
	"fmt"
	"log"

	"medical_encryption/pkg/hashing"
)

func main() {
	// Define the input data
	data := []byte("Hello, World!")

	// Define a progress callback function
	progressCallback := func(info hashing.ProgressInfo) {
		fmt.Printf("Progress: %f%%\n", info.Progress)
	}

	// Calculate the SHA-256 hash of the data with progress reporting
	hash, err := hashing.CalculateSHA256(data, progressCallback)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("SHA-256 Hash:", hash)

	// Verify the integrity of the data
	expectedHash := hash // Use the calculated hash as the expected hash
	verified, err := hashing.VerifyFileIntegrity(data, expectedHash, hashing.SHA256, progressCallback)
	if err != nil {
		log.Fatal(err)
	}

	if verified {
		fmt.Println("Data integrity verified")
	} else {
		fmt.Println("Data integrity failed")
	}
}
