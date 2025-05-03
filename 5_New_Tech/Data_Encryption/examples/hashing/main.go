package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"

	"medical_encryption/pkg/hashing"
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
func printProgress(info hashing.ProgressInfo) {
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
	// Read a sample DICOM file
	inputFile := filepath.Join("test_data", "1.2.840.113619.2.55.3.2831200001.555.1636080662.303.1.dcm")
	data, err := os.ReadFile(inputFile)
	if err != nil {
		log.Fatalf("Failed to read file: %v", err)
	}
	fmt.Printf("File size: %s\n", formatBytes(int64(len(data))))

	// Hash with SHA-256
	fmt.Println("\nCalculating SHA-256 hash...")
	startTime := time.Now()
	sha256Hash, err := hashing.CalculateSHA256(data, printProgress)
	if err != nil {
		log.Fatalf("Failed to calculate SHA-256: %v", err)
	}
	sha256Time := time.Since(startTime)
	fmt.Printf("SHA-256 hash: %x\n", sha256Hash)
	fmt.Printf("SHA-256 time: %v\n", sha256Time)
	fmt.Printf("SHA-256 speed: %.2f MB/s\n",
		float64(len(data))/1048576/sha256Time.Seconds())

	// Hash with SHA-512
	fmt.Println("\nCalculating SHA-512 hash...")
	startTime = time.Now()
	sha512Hash, err := hashing.CalculateSHA512(data, printProgress)
	if err != nil {
		log.Fatalf("Failed to calculate SHA-512: %v", err)
	}
	sha512Time := time.Since(startTime)
	fmt.Printf("SHA-512 hash: %x\n", sha512Hash)
	fmt.Printf("SHA-512 time: %v\n", sha512Time)
	fmt.Printf("SHA-512 speed: %.2f MB/s\n",
		float64(len(data))/1048576/sha512Time.Seconds())

	// Calculate and verify file integrity
	fmt.Println("\nVerifying file integrity...")
	startTime = time.Now()
	isValid, err := hashing.VerifyFileIntegrity(data, sha256Hash, hashing.SHA256, printProgress)
	if err != nil {
		log.Fatalf("Failed to verify integrity: %v", err)
	}
	verifyTime := time.Since(startTime)

	if isValid {
		fmt.Println("File integrity verified successfully!")
	} else {
		fmt.Println("Warning: File integrity check failed!")
	}
	fmt.Printf("Verification time: %v\n", verifyTime)
	fmt.Printf("Total processing time: %v\n", sha256Time+sha512Time+verifyTime)
}
