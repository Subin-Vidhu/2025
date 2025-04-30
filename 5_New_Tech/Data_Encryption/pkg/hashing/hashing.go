package hashing

import (
	"crypto/sha256"
	"crypto/sha512"
	"fmt"
	"hash"
)

// HashAlgorithm represents the type of hash algorithm
type HashAlgorithm int

const (
	SHA256 HashAlgorithm = iota
	SHA512
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

// chunkSize defines the size of data chunks for progress reporting
const chunkSize = 1024 * 1024 // 1MB chunks

// calculateHash is a generic function to calculate hash with progress reporting
func calculateHash(data []byte, h hash.Hash, algorithm string, progress ProgressCallback) ([]byte, error) {
	totalSize := int64(len(data))
	processed := int64(0)

	for i := 0; i < len(data); i += chunkSize {
		end := i + chunkSize
		if end > len(data) {
			end = len(data)
		}

		chunk := data[i:end]
		if _, err := h.Write(chunk); err != nil {
			return nil, fmt.Errorf("failed to hash chunk: %v", err)
		}

		processed += int64(len(chunk))
		if progress != nil {
			progress(ProgressInfo{
				Stage:          fmt.Sprintf("Calculating %s", algorithm),
				Progress:       float64(processed) * 100 / float64(totalSize),
				BytesProcessed: processed,
				TotalBytes:     totalSize,
			})
		}
	}

	return h.Sum(nil), nil
}

// CalculateSHA256 calculates the SHA-256 hash of data with progress reporting
func CalculateSHA256(data []byte, progress ProgressCallback) ([]byte, error) {
	return calculateHash(data, sha256.New(), "SHA-256", progress)
}

// CalculateSHA512 calculates the SHA-512 hash of data with progress reporting
func CalculateSHA512(data []byte, progress ProgressCallback) ([]byte, error) {
	return calculateHash(data, sha512.New(), "SHA-512", progress)
}

// VerifyFileIntegrity verifies the integrity of data against a known hash
func VerifyFileIntegrity(data []byte, expectedHash []byte, algorithm HashAlgorithm, progress ProgressCallback) (bool, error) {
	var calculatedHash []byte
	var err error

	switch algorithm {
	case SHA256:
		calculatedHash, err = CalculateSHA256(data, progress)
	case SHA512:
		calculatedHash, err = CalculateSHA512(data, progress)
	default:
		return false, fmt.Errorf("unsupported hash algorithm: %v", algorithm)
	}

	if err != nil {
		return false, fmt.Errorf("failed to calculate hash: %v", err)
	}

	// Compare hashes
	if len(calculatedHash) != len(expectedHash) {
		return false, nil
	}

	// Time-constant comparison to prevent timing attacks
	diff := byte(0)
	for i := 0; i < len(calculatedHash); i++ {
		diff |= calculatedHash[i] ^ expectedHash[i]
	}

	return diff == 0, nil
}
