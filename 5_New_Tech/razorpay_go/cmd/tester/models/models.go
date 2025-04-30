package models

import (
	"time"
)

// Payment represents a payment transaction
type Payment struct {
	ID               int64     `json:"id"`
	OrderID          string    `json:"order_id"`
	PaymentID        string    `json:"payment_id"`
	Amount           float64   `json:"amount"`
	Currency         string    `json:"currency"`
	Status           string    `json:"status"` // success, failed, cancelled
	PaymentMethod    string    `json:"payment_method"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
	RefundableAmount float64   `json:"refundable_amount"`
}

// Refund represents a refund transaction
type Refund struct {
	ID        int64     `json:"id"`
	PaymentID string    `json:"payment_id"`
	RefundID  string    `json:"refund_id"` // Razorpay refund ID
	Amount    float64   `json:"amount"`
	Currency  string    `json:"currency"`
	Status    string    `json:"status"` // processed, failed, pending
	Reason    string    `json:"reason"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
	Notes     string    `json:"notes"`
}
