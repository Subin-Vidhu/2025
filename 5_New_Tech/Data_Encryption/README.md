# Medical Data Encryption System

A comprehensive Go-based encryption system designed specifically for medical DICOM files, providing secure encryption, hashing, and integrity verification with detailed progress reporting.

## Project Overview

This project implements a secure data encryption system with the following features:
- Hybrid encryption (RSA + AES) for optimal security and performance
- Multiple encryption methods (symmetric, asymmetric, hybrid)
- File integrity verification using cryptographic hashing
- Detailed progress reporting with visual progress bars
- Performance metrics tracking
- Minimal encryption overhead (~0.29%)

## Project Structure

```
medical_encryption/
├── pkg/                    # Core packages
│   ├── asymmetric/        # RSA encryption implementation
│   │   └── rsa.go
│   ├── symmetric/         # AES encryption implementation
│   │   └── aes.go
│   ├── hybrid/           # Combined RSA+AES implementation
│   │   └── hybrid.go
│   └── hashing/          # Cryptographic hashing
│       └── hashing.go
├── examples/              # Example implementations
│   ├── hybrid/          # Hybrid encryption example
│   │   └── main.go
│   ├── hashing/         # Hashing and verification example
│   │   └── main.go
│   ├── asymmetric_example.go  # RSA encryption example
│   └── symmetric_example.go   # AES encryption example
├── test_data/            # Sample DICOM files for testing
│   └── *.dcm
├── keys/                 # Directory for key storage
└── go.mod               # Go module definition
```

## Core Components

### 1. Symmetric Encryption (AES-256)
- **Location**: `pkg/symmetric/aes.go`
- **Features**:
  - AES-256 in GCM mode
  - Secure random key generation
  - Authenticated encryption
  - Progress reporting
- **Use Case**: Bulk data encryption

### 2. Asymmetric Encryption (RSA)
- **Location**: `pkg/asymmetric/rsa.go`
- **Features**:
  - 2048-bit RSA key pairs
  - OAEP padding with SHA-256
  - PEM key format support
  - ~245 bytes encryption limit
- **Use Case**: Key encryption and small data

### 3. Hybrid Encryption
- **Location**: `pkg/hybrid/hybrid.go`
- **Features**:
  - Combines RSA and AES benefits
  - RSA for key encryption
  - AES for data encryption
  - Serialization support
  - Detailed progress tracking
- **Performance**:
  - Encryption time: ~2ms
  - Decryption time: ~2ms
  - 0.29% size overhead

### 4. Hashing and Verification
- **Location**: `pkg/hashing/hashing.go`
- **Features**:
  - SHA-256 and SHA-512 support
  - Chunked processing
  - Progress reporting
  - Time-constant comparisons
  - File integrity verification

## Example Usage

### 1. Hybrid Encryption Example
```go
// Read file
data, _ := os.ReadFile("medical_image.dcm")

// Generate key pair
privateKey, publicKey, _ := asymmetric.GenerateKeyPair(2048)

// Encrypt
encrypted, _ := hybrid.Encrypt(publicKey, data, progressCallback)

// Decrypt
decrypted, _ := hybrid.Decrypt(privateKey, encrypted, progressCallback)
```

### 2. File Integrity Verification
```go
// Calculate hash
hash, _ := hashing.CalculateSHA256(data, progressCallback)

// Verify integrity
isValid, _ := hashing.VerifyFileIntegrity(data, hash, hashing.SHA256, progressCallback)
```

## Progress Reporting

All operations provide detailed progress information through callbacks:
```go
type ProgressInfo struct {
    Stage          string  // Current operation
    Progress       float64 // Percentage (0-100)
    BytesProcessed int64   // Processed bytes
    TotalBytes     int64   // Total bytes
    CurrentSpeed   float64 // Speed in MB/s
    TimeRemaining  string  // Estimated time
}
```

Visual progress bars show:
```
Encrypting file... [████████████████████████████████████████] 100.0% (105.5 KB/105.5 KB)
```

## Performance Metrics

Tested with 105.5 KB DICOM file:

1. **Hybrid Encryption**:
   - Encryption: ~2ms (41.27 MB/s)
   - Decryption: ~2ms (49.33 MB/s)
   - Size overhead: 0.29%

2. **Hashing**:
   - SHA-256: ~0.5ms (198.52 MB/s)
   - SHA-512: <0.1ms
   - Verification: ~0.5ms

## Security Features

1. **Encryption**:
   - AES-256-GCM for authenticated encryption
   - RSA-2048 with OAEP padding
   - Secure random key generation
   - PEM format key storage

2. **Hashing**:
   - SHA-256 and SHA-512 support
   - Time-constant comparisons
   - Chunked processing

3. **Best Practices**:
   - No key reuse
   - Secure key storage
   - Authenticated encryption
   - Time-constant operations

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medical_encryption.git
   ```

2. Install dependencies:
   ```bash
   go mod download
   ```

3. Run examples:
   ```bash
   go run examples/hybrid/main.go    # Hybrid encryption
   go run examples/hashing/main.go   # Hashing and verification
   ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Considerations

- Store private keys securely
- Use strong passwords for key encryption
- Regularly verify file integrity
- Keep the system and dependencies updated
- Follow medical data protection regulations 