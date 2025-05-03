package main

import (
	"fmt"
	"log"

	"medical_encryption/pkg/asymmetric"
)

func main() {
	// Generate a new RSA key pair
	privateKey, publicKey, err := asymmetric.GenerateKeyPair(2048)
	if err != nil {
		log.Fatal(err)
	}

	// Export the public key to PEM format
	pubKeyPEM, err := asymmetric.ExportPublicKeyToPEM(publicKey)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(pubKeyPEM))

	// Export the private key to PEM format
	privKeyPEM := asymmetric.ExportPrivateKeyToPEM(privateKey)
	fmt.Println(string(privKeyPEM))

	// Encrypt some data using the public key
	plaintext := []byte("Hello, World!")
	ciphertext, err := asymmetric.Encrypt(publicKey, plaintext)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(ciphertext)

	// Decrypt the data using the private key
	decrypted, err := asymmetric.Decrypt(privateKey, ciphertext)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(decrypted)) // Output: Hello, World!
}
