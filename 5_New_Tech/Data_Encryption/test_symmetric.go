package main

import (
	"fmt"
	"log"

	"medical_encryption/pkg/symmetric"
)

func main() {
	// Generate a random key
	key, err := symmetric.GenerateKey()
	fmt.Println("key", key)
	if err != nil {
		log.Fatal(err)
	}

	// Encrypt some data
	plaintext := []byte("Hello, World!")
	encrypted, err := symmetric.Encrypt(plaintext, key)
	fmt.Println("plaintext", plaintext)
	fmt.Println("encrypted", encrypted)
	if err != nil {
		log.Fatal(err)
	}

	// Decrypt the data
	decrypted, err := symmetric.Decrypt(encrypted, key)
	fmt.Println("decrypted", decrypted)
	fmt.Println("decrypted string", string(decrypted))
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(decrypted)) // Output: Hello, World!
}
