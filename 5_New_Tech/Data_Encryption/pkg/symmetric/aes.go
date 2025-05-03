package symmetric

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"io"
)

// KeySize represents the size of the AES-256 key in bytes
const KeySize = 32

// GenerateKey generates a random 32-byte key for AES-256 encryption
func GenerateKey() (string, error) {
	key := make([]byte, KeySize)
	if _, err := io.ReadFull(rand.Reader, key); err != nil {
		return "", err
	}
	return hex.EncodeToString(key), nil
}

// Encrypt encrypts data using AES-256-GCM
func Encrypt(plaintext []byte, keyString string) (string, error) {
	// Convert the hex-encoded key back to bytes
	key, err := hex.DecodeString(keyString)
	if err != nil {
		return "", err
	}

	// Create a new cipher block using AES
	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}

	// Create a new GCM (Galois/Counter Mode) cipher
	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return "", err
	}

	// Generate a random nonce
	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return "", err
	}

	// Encrypt and seal the data
	ciphertext := gcm.Seal(nonce, nonce, plaintext, nil)
	return hex.EncodeToString(ciphertext), nil
}

// Decrypt decrypts data using AES-256-GCM
func Decrypt(encryptedString string, keyString string) ([]byte, error) {
	// Convert the hex-encoded key and ciphertext back to bytes
	key, err := hex.DecodeString(keyString)
	if err != nil {
		return nil, err
	}

	ciphertext, err := hex.DecodeString(encryptedString)
	if err != nil {
		return nil, err
	}

	// Create a new cipher block using AES
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	// Create a new GCM cipher
	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	// Extract the nonce size
	nonceSize := gcm.NonceSize()
	if len(ciphertext) < nonceSize {
		return nil, errors.New("ciphertext too short")
	}

	// Split nonce and ciphertext
	nonce, ciphertext := ciphertext[:nonceSize], ciphertext[nonceSize:]

	// Decrypt the data
	plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return nil, err
	}

	return plaintext, nil
}
