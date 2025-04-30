package service

import (
	"errors"
	"fmt"
	"razorpay_go/cmd/tester/models"
	"razorpay_go/cmd/tester/repository"

	"github.com/razorpay/razorpay-go"
)

type RefundService struct {
	repo     *repository.Repository
	rzClient *razorpay.Client
}

func NewRefundService(repo *repository.Repository, rzClient *razorpay.Client) *RefundService {
	return &RefundService{
		repo:     repo,
		rzClient: rzClient,
	}
}

// InitiateRefund starts a refund process for a payment
func (s *RefundService) InitiateRefund(paymentID string, amount float64, reason string) (*models.Refund, error) {
	// Get payment details from database
	payment, err := s.repo.GetPaymentByID(paymentID)
	if err != nil {
		return nil, fmt.Errorf("error fetching payment: %v", err)
	}

	// Validate refund amount
	if amount > payment.RefundableAmount {
		return nil, errors.New("refund amount exceeds refundable amount")
	}

	// Convert amount to paise/cents
	amountInPaise := int64(amount * 100)

	// Create refund in Razorpay
	notes := map[string]string{
		"reason": reason,
	}

	rzpRefund, err := s.rzClient.Payment.Refund(paymentID, int(amountInPaise), nil, notes)
	if err != nil {
		return nil, fmt.Errorf("error creating refund in Razorpay: %v", err)
	}

	// Create refund record
	refund := &models.Refund{
		PaymentID: paymentID,
		RefundID:  rzpRefund["id"].(string),
		Amount:    amount,
		Currency:  payment.Currency,
		Status:    rzpRefund["status"].(string),
		Reason:    reason,
		Notes:     fmt.Sprintf("Refund initiated via test interface"),
	}

	// Save refund to database
	err = s.repo.SaveRefund(refund)
	if err != nil {
		return nil, fmt.Errorf("error saving refund: %v", err)
	}

	// Update payment's refundable amount
	newRefundableAmount := payment.RefundableAmount - amount
	err = s.repo.UpdatePaymentRefundableAmount(paymentID, newRefundableAmount)
	if err != nil {
		return nil, fmt.Errorf("error updating refundable amount: %v", err)
	}

	return refund, nil
}

// GetRefundDetails fetches refund details from Razorpay and updates local status
func (s *RefundService) GetRefundDetails(refundID string) (*models.Refund, error) {
	// Fetch refund details from Razorpay
	rzpRefund, err := s.rzClient.Refund.Fetch(refundID, nil, nil)
	if err != nil {
		return nil, fmt.Errorf("error fetching refund from Razorpay: %v", err)
	}

	// Update refund status in database
	err = s.repo.UpdateRefundStatus(refundID, rzpRefund["status"].(string))
	if err != nil {
		return nil, fmt.Errorf("error updating refund status: %v", err)
	}

	// Return updated refund details
	return &models.Refund{
		RefundID: refundID,
		Status:   rzpRefund["status"].(string),
		Amount:   float64(rzpRefund["amount"].(float64)) / 100,
	}, nil
}

// GetRefundsForPayment retrieves all refunds for a payment
func (s *RefundService) GetRefundsForPayment(paymentID string) ([]models.Refund, error) {
	return s.repo.GetRefundsByPaymentID(paymentID)
}
