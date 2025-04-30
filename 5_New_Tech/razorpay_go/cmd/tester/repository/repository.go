package repository

import (
	"database/sql"
	"log"
	"razorpay_go/cmd/tester/models"
	"time"
)

type Repository struct {
	db *sql.DB
}

func NewRepository(db *sql.DB) *Repository {
	return &Repository{db: db}
}

// SavePayment saves a new payment record
func (r *Repository) SavePayment(payment *models.Payment) error {
	log.Printf("Saving payment record: %+v", payment)
	query := `
		INSERT INTO payments (
			order_id, payment_id, amount, currency, status, 
			payment_method, refundable_amount, created_at, updated_at
		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
	`
	result, err := r.db.Exec(
		query,
		payment.OrderID,
		payment.PaymentID,
		payment.Amount,
		payment.Currency,
		payment.Status,
		payment.PaymentMethod,
		payment.RefundableAmount,
		time.Now(),
		time.Now(),
	)
	if err != nil {
		log.Printf("Error saving payment: %v", err)
		return err
	}

	rowsAffected, _ := result.RowsAffected()
	log.Printf("Payment saved successfully. Rows affected: %d", rowsAffected)
	return nil
}

// GetPaymentByID retrieves a payment by its Razorpay payment ID
func (r *Repository) GetPaymentByID(paymentID string) (*models.Payment, error) {
	payment := &models.Payment{}
	query := `
		SELECT id, order_id, payment_id, amount, currency, status, 
		       payment_method, refundable_amount, created_at, updated_at 
		FROM payments 
		WHERE payment_id = ?
	`
	err := r.db.QueryRow(query, paymentID).Scan(
		&payment.ID,
		&payment.OrderID,
		&payment.PaymentID,
		&payment.Amount,
		&payment.Currency,
		&payment.Status,
		&payment.PaymentMethod,
		&payment.RefundableAmount,
		&payment.CreatedAt,
		&payment.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}
	return payment, nil
}

// UpdatePaymentRefundableAmount updates the refundable amount for a payment
func (r *Repository) UpdatePaymentRefundableAmount(paymentID string, newAmount float64) error {
	query := `
		UPDATE payments 
		SET refundable_amount = ?, updated_at = ? 
		WHERE payment_id = ?
	`
	_, err := r.db.Exec(query, newAmount, time.Now(), paymentID)
	return err
}

// SaveRefund saves a new refund record
func (r *Repository) SaveRefund(refund *models.Refund) error {
	query := `
		INSERT INTO refunds (
			payment_id, refund_id, amount, currency, status, 
			reason, notes, created_at, updated_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
	`
	_, err := r.db.Exec(
		query,
		refund.PaymentID,
		refund.RefundID,
		refund.Amount,
		refund.Currency,
		refund.Status,
		refund.Reason,
		refund.Notes,
		time.Now(),
		time.Now(),
	)
	return err
}

// GetRefundsByPaymentID retrieves all refunds for a payment
func (r *Repository) GetRefundsByPaymentID(paymentID string) ([]models.Refund, error) {
	query := `
		SELECT id, payment_id, refund_id, amount, currency, status, 
		       reason, notes, created_at, updated_at 
		FROM refunds 
		WHERE payment_id = ?
		ORDER BY created_at DESC
	`
	rows, err := r.db.Query(query, paymentID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var refunds []models.Refund
	for rows.Next() {
		var refund models.Refund
		err := rows.Scan(
			&refund.ID,
			&refund.PaymentID,
			&refund.RefundID,
			&refund.Amount,
			&refund.Currency,
			&refund.Status,
			&refund.Reason,
			&refund.Notes,
			&refund.CreatedAt,
			&refund.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}
		refunds = append(refunds, refund)
	}
	return refunds, nil
}

// UpdateRefundStatus updates the status of a refund
func (r *Repository) UpdateRefundStatus(refundID string, status string) error {
	query := `
		UPDATE refunds 
		SET status = ?, updated_at = ? 
		WHERE refund_id = ?
	`
	_, err := r.db.Exec(query, status, time.Now(), refundID)
	return err
}
