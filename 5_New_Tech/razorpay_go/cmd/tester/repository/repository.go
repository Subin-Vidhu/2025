package repository

import (
	"database/sql"
	"fmt"
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
	log.Printf("Fetching payment with ID: %s", paymentID)
	payment := &models.Payment{}
	query := `
		SELECT id, order_id, payment_id, amount, currency, status, 
		       payment_method, refundable_amount, created_at, updated_at 
		FROM payments 
		WHERE payment_id = $1
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
		log.Printf("Error fetching payment: %v", err)
		return nil, err
	}
	log.Printf("Successfully fetched payment: %+v", payment)
	return payment, nil
}

// UpdatePaymentRefundableAmount updates the refundable amount for a payment
func (r *Repository) UpdatePaymentRefundableAmount(paymentID string, newAmount float64) error {
	log.Printf("Updating refundable amount for payment %s to %f", paymentID, newAmount)
	query := `
		UPDATE payments 
		SET refundable_amount = $1, updated_at = $2 
		WHERE payment_id = $3
		RETURNING id
	`
	var id int64
	err := r.db.QueryRow(query, newAmount, time.Now(), paymentID).Scan(&id)
	if err != nil {
		log.Printf("Error updating refundable amount: %v", err)
		return fmt.Errorf("error updating refundable amount: %v", err)
	}

	log.Printf("Successfully updated refundable amount for payment ID %s (internal ID: %d)", paymentID, id)
	return nil
}

// SaveRefund saves a new refund record
func (r *Repository) SaveRefund(refund *models.Refund) error {
	log.Printf("Saving refund record: %+v", refund)
	query := `
		INSERT INTO refunds (
			payment_id, refund_id, amount, currency, status, 
			reason, notes, created_at, updated_at
		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
	`
	result, err := r.db.Exec(
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
	if err != nil {
		log.Printf("Error saving refund: %v", err)
		return err
	}

	rowsAffected, _ := result.RowsAffected()
	log.Printf("Refund saved successfully. Rows affected: %d", rowsAffected)
	return nil
}

// GetRefundsByPaymentID retrieves all refunds for a payment
func (r *Repository) GetRefundsByPaymentID(paymentID string) ([]models.Refund, error) {
	log.Printf("Fetching refunds for payment ID: %s", paymentID)
	query := `
		SELECT id, payment_id, refund_id, amount, currency, status, 
		       reason, notes, created_at, updated_at 
		FROM refunds 
		WHERE payment_id = $1
		ORDER BY created_at DESC
	`
	rows, err := r.db.Query(query, paymentID)
	if err != nil {
		log.Printf("Error fetching refunds: %v", err)
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
			log.Printf("Error scanning refund row: %v", err)
			return nil, err
		}
		refunds = append(refunds, refund)
	}
	log.Printf("Found %d refunds for payment", len(refunds))
	return refunds, nil
}

// UpdateRefundStatus updates the status of a refund
func (r *Repository) UpdateRefundStatus(refundID string, status string) error {
	log.Printf("Updating refund status - ID: %s, Status: %s", refundID, status)
	query := `
		UPDATE refunds 
		SET status = $1, updated_at = $2 
		WHERE refund_id = $3
	`
	result, err := r.db.Exec(query, status, time.Now(), refundID)
	if err != nil {
		log.Printf("Error updating refund status: %v", err)
		return err
	}

	rowsAffected, _ := result.RowsAffected()
	log.Printf("Refund status updated successfully. Rows affected: %d", rowsAffected)
	return nil
}

// ListPayments retrieves all payments from the database
func (r *Repository) ListPayments() ([]models.Payment, error) {
	log.Printf("Fetching all payments")
	query := `
		SELECT id, order_id, payment_id, amount, currency, status, 
			   payment_method, refundable_amount, created_at, updated_at 
		FROM payments 
		ORDER BY created_at DESC
	`
	rows, err := r.db.Query(query)
	if err != nil {
		log.Printf("Error fetching payments: %v", err)
		return nil, err
	}
	defer rows.Close()

	var payments []models.Payment
	for rows.Next() {
		var payment models.Payment
		err := rows.Scan(
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
			log.Printf("Error scanning payment row: %v", err)
			return nil, err
		}
		payments = append(payments, payment)
	}
	log.Printf("Found %d payments", len(payments))
	return payments, nil
}
