package asymmetric

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/pem"
	"errors"
)

const (
	// DefaultKeySize is the default RSA key size in bits
	DefaultKeySize = 2048
)

// GenerateKeyPair generates a new RSA key pair
func GenerateKeyPair(bits int) (*rsa.PrivateKey, *rsa.PublicKey, error) {
	privateKey, err := rsa.GenerateKey(rand.Reader, bits)
	if err != nil {
		return nil, nil, err
	}
	return privateKey, &privateKey.PublicKey, nil
}

// ExportPublicKeyToPEM exports the public key to PEM format
func ExportPublicKeyToPEM(publicKey *rsa.PublicKey) ([]byte, error) {
	pubKeyBytes, err := x509.MarshalPKIXPublicKey(publicKey)
	if err != nil {
		return nil, err
	}

	pubKeyPEM := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PUBLIC KEY",
		Bytes: pubKeyBytes,
	})
	return pubKeyPEM, nil
}

// ExportPrivateKeyToPEM exports the private key to PEM format
func ExportPrivateKeyToPEM(privateKey *rsa.PrivateKey) []byte {
	privKeyPEM := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: x509.MarshalPKCS1PrivateKey(privateKey),
	})
	return privKeyPEM
}

// ImportPublicKeyFromPEM imports a public key from PEM format
func ImportPublicKeyFromPEM(pubKeyPEM []byte) (*rsa.PublicKey, error) {
	block, _ := pem.Decode(pubKeyPEM)
	if block == nil {
		return nil, errors.New("failed to decode PEM block")
	}

	pub, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		return nil, err
	}

	switch pub := pub.(type) {
	case *rsa.PublicKey:
		return pub, nil
	default:
		return nil, errors.New("key type is not RSA")
	}
}

// ImportPrivateKeyFromPEM imports a private key from PEM format
func ImportPrivateKeyFromPEM(privKeyPEM []byte) (*rsa.PrivateKey, error) {
	block, _ := pem.Decode(privKeyPEM)
	if block == nil {
		return nil, errors.New("failed to decode PEM block")
	}

	priv, err := x509.ParsePKCS1PrivateKey(block.Bytes)
	if err != nil {
		return nil, err
	}

	return priv, nil
}

// Encrypt encrypts data using RSA-OAEP with SHA256
func Encrypt(publicKey *rsa.PublicKey, plaintext []byte) ([]byte, error) {
	hash := sha256.New()
	ciphertext, err := rsa.EncryptOAEP(hash, rand.Reader, publicKey, plaintext, nil)
	if err != nil {
		return nil, err
	}
	return ciphertext, nil
}

// Decrypt decrypts data using RSA-OAEP with SHA256
func Decrypt(privateKey *rsa.PrivateKey, ciphertext []byte) ([]byte, error) {
	hash := sha256.New()
	plaintext, err := rsa.DecryptOAEP(hash, rand.Reader, privateKey, ciphertext, nil)
	if err != nil {
		return nil, err
	}
	return plaintext, nil
}
