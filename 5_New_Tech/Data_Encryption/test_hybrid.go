package main

import (
	"crypto/rand"
	"crypto/rsa"
	"fmt"
	"log"
	"medical_encryption/pkg/hybrid"
)

func main() {
	// Generate a new RSA key pair
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	fmt.Println("privateKey", privateKey)
	if err != nil {
		log.Fatal(err)
	}

	publicKey := &privateKey.PublicKey
	fmt.Println("publicKey", publicKey)
	// Encrypt some data
	data := []byte("Hello, World!")
	encryptedData, err := hybrid.Encrypt(publicKey, data, nil)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("encryptedData", encryptedData)
	// Decrypt the data
	decryptedData, err := hybrid.Decrypt(privateKey, encryptedData, nil)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(decryptedData)) // Output: Hello, World!
}
