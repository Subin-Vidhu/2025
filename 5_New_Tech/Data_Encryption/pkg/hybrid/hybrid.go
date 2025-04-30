package hybrid

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/binary"
	"errors"
	"fmt"
	"io"
)

// ProgressInfo contains detailed progress information
type ProgressInfo struct {
	Stage          string  // Current operation stage
	Progress       float64 // Overall progress percentage (0-100)
	BytesProcessed int64   // Number of bytes processed
	TotalBytes     int64   // Total bytes to process
	CurrentSpeed   float64 // Processing speed in MB/s (if available)
	TimeRemaining  string  // Estimated time remaining (if available)
}

// ProgressCallback is a function type for reporting progress
type ProgressCallback func(info ProgressInfo)

// EncryptedData represents the complete encrypted package
type EncryptedData struct {
	EncryptedAESKey []byte // RSA encrypted AES key
	Nonce           []byte // AES-GCM nonce
	Ciphertext      []byte // AES encrypted data
}

// Encrypt encrypts data using hybrid encryption with detailed progress reporting
func Encrypt(publicKey *rsa.PublicKey, data []byte, progress ProgressCallback) (*EncryptedData, error) {
	totalBytes := int64(len(data))

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Generating AES key",
			Progress:       0,
			BytesProcessed: 0,
			TotalBytes:     totalBytes,
		})
	}

	// Generate a random AES key (32 bytes for AES-256)
	aesKey := make([]byte, 32)
	if _, err := io.ReadFull(rand.Reader, aesKey); err != nil {
		return nil, err
	}

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Creating cipher",
			Progress:       10,
			BytesProcessed: 32,
			TotalBytes:     totalBytes,
		})
	}

	// Create AES cipher
	block, err := aes.NewCipher(aesKey)
	if err != nil {
		return nil, err
	}

	// Create GCM mode
	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Generating nonce",
			Progress:       20,
			BytesProcessed: 32,
			TotalBytes:     totalBytes,
		})
	}

	// Generate nonce
	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}

	if progress != nil {
		progress(ProgressInfo{
			Stage:          fmt.Sprintf("Encrypting data (%d bytes)", len(data)),
			Progress:       30,
			BytesProcessed: 32 + int64(gcm.NonceSize()),
			TotalBytes:     totalBytes,
		})
	}

	// Encrypt data with AES-GCM
	ciphertext := gcm.Seal(nil, nonce, data, nil)

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Encrypting AES key with RSA",
			Progress:       80,
			BytesProcessed: totalBytes,
			TotalBytes:     totalBytes,
		})
	}

	// Encrypt AES key with RSA
	hash := sha256.New()
	encryptedKey, err := rsa.EncryptOAEP(hash, rand.Reader, publicKey, aesKey, nil)
	if err != nil {
		return nil, err
	}

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Finalizing encryption",
			Progress:       100,
			BytesProcessed: totalBytes,
			TotalBytes:     totalBytes,
		})
	}

	return &EncryptedData{
		EncryptedAESKey: encryptedKey,
		Nonce:           nonce,
		Ciphertext:      ciphertext,
	}, nil
}

// Decrypt decrypts data using hybrid decryption with detailed progress reporting
func Decrypt(privateKey *rsa.PrivateKey, encData *EncryptedData, progress ProgressCallback) ([]byte, error) {
	totalBytes := int64(len(encData.Ciphertext))

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Decrypting AES key",
			Progress:       0,
			BytesProcessed: 0,
			TotalBytes:     totalBytes,
		})
	}

	// Decrypt the AES key using RSA
	hash := sha256.New()
	aesKey, err := rsa.DecryptOAEP(hash, rand.Reader, privateKey, encData.EncryptedAESKey, nil)
	if err != nil {
		return nil, err
	}

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Creating cipher",
			Progress:       20,
			BytesProcessed: int64(len(encData.EncryptedAESKey)),
			TotalBytes:     totalBytes,
		})
	}

	// Create AES cipher
	block, err := aes.NewCipher(aesKey)
	if err != nil {
		return nil, err
	}

	// Create GCM mode
	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	if progress != nil {
		progress(ProgressInfo{
			Stage:          fmt.Sprintf("Decrypting data (%d bytes)", len(encData.Ciphertext)),
			Progress:       40,
			BytesProcessed: int64(len(encData.EncryptedAESKey) + len(encData.Nonce)),
			TotalBytes:     totalBytes,
		})
	}

	// Decrypt the data
	plaintext, err := gcm.Open(nil, encData.Nonce, encData.Ciphertext, nil)
	if err != nil {
		return nil, err
	}

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Finalizing decryption",
			Progress:       100,
			BytesProcessed: totalBytes,
			TotalBytes:     totalBytes,
		})
	}

	return plaintext, nil
}

// SerializeEncryptedData converts EncryptedData to a byte slice with detailed progress reporting
func SerializeEncryptedData(data *EncryptedData, progress ProgressCallback) []byte {
	totalSize := int64(8 + len(data.EncryptedAESKey) + 8 + len(data.Nonce) + 8 + len(data.Ciphertext))

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Calculating sizes",
			Progress:       0,
			BytesProcessed: 0,
			TotalBytes:     totalSize,
		})
	}

	result := make([]byte, totalSize)
	offset := 0

	if progress != nil {
		progress(ProgressInfo{
			Stage:          fmt.Sprintf("Writing encrypted key (%d bytes)", len(data.EncryptedAESKey)),
			Progress:       40,
			BytesProcessed: 8,
			TotalBytes:     totalSize,
		})
	}

	// Write encrypted key length and data
	binary.LittleEndian.PutUint64(result[offset:], uint64(len(data.EncryptedAESKey)))
	offset += 8
	copy(result[offset:], data.EncryptedAESKey)
	offset += len(data.EncryptedAESKey)

	if progress != nil {
		progress(ProgressInfo{
			Stage:          fmt.Sprintf("Writing nonce (%d bytes)", len(data.Nonce)),
			Progress:       60,
			BytesProcessed: int64(offset),
			TotalBytes:     totalSize,
		})
	}

	// Write nonce length and data
	binary.LittleEndian.PutUint64(result[offset:], uint64(len(data.Nonce)))
	offset += 8
	copy(result[offset:], data.Nonce)
	offset += len(data.Nonce)

	if progress != nil {
		progress(ProgressInfo{
			Stage:          fmt.Sprintf("Writing ciphertext (%d bytes)", len(data.Ciphertext)),
			Progress:       80,
			BytesProcessed: int64(offset),
			TotalBytes:     totalSize,
		})
	}

	// Write ciphertext length and data
	binary.LittleEndian.PutUint64(result[offset:], uint64(len(data.Ciphertext)))
	offset += 8
	copy(result[offset:], data.Ciphertext)

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Serialization complete",
			Progress:       100,
			BytesProcessed: totalSize,
			TotalBytes:     totalSize,
		})
	}

	return result
}

// DeserializeEncryptedData converts a byte slice back to EncryptedData with detailed progress reporting
func DeserializeEncryptedData(data []byte, progress ProgressCallback) (*EncryptedData, error) {
	totalBytes := int64(len(data))

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Validating data",
			Progress:       0,
			BytesProcessed: 0,
			TotalBytes:     totalBytes,
		})
	}

	if len(data) < 24 {
		return nil, errors.New("data too short")
	}

	offset := 0

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Reading encrypted key",
			Progress:       20,
			BytesProcessed: 8,
			TotalBytes:     totalBytes,
		})
	}

	// Read encrypted key length and data
	keyLen := binary.LittleEndian.Uint64(data[offset:])
	offset += 8
	if uint64(len(data[offset:])) < keyLen {
		return nil, errors.New("data corrupted: key length")
	}
	encryptedKey := make([]byte, keyLen)
	copy(encryptedKey, data[offset:offset+int(keyLen)])
	offset += int(keyLen)

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Reading nonce",
			Progress:       40,
			BytesProcessed: int64(offset),
			TotalBytes:     totalBytes,
		})
	}

	// Read nonce length and data
	nonceLen := binary.LittleEndian.Uint64(data[offset:])
	offset += 8
	if uint64(len(data[offset:])) < nonceLen {
		return nil, errors.New("data corrupted: nonce length")
	}
	nonce := make([]byte, nonceLen)
	copy(nonce, data[offset:offset+int(nonceLen)])
	offset += int(nonceLen)

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Reading ciphertext",
			Progress:       60,
			BytesProcessed: int64(offset),
			TotalBytes:     totalBytes,
		})
	}

	// Read ciphertext length and data
	ciphertextLen := binary.LittleEndian.Uint64(data[offset:])
	offset += 8
	if uint64(len(data[offset:])) < ciphertextLen {
		return nil, errors.New("data corrupted: ciphertext length")
	}
	ciphertext := make([]byte, ciphertextLen)
	copy(ciphertext, data[offset:offset+int(ciphertextLen)])

	if progress != nil {
		progress(ProgressInfo{
			Stage:          "Deserialization complete",
			Progress:       100,
			BytesProcessed: totalBytes,
			TotalBytes:     totalBytes,
		})
	}

	return &EncryptedData{
		EncryptedAESKey: encryptedKey,
		Nonce:           nonce,
		Ciphertext:      ciphertext,
	}, nil
}
