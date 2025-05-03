package handlers

import (
	"encoding/json"
	"net/http"
	"razorpay_go/cmd/tester/service"
)

type RefundHandler struct {
	refundService *service.RefundService
}

func NewRefundHandler(refundService *service.RefundService) *RefundHandler {
	return &RefundHandler{
		refundService: refundService,
	}
}

type RefundRequest struct {
	PaymentID string  `json:"payment_id"`
	Amount    float64 `json:"amount"`
	Reason    string  `json:"reason"`
}

// InitiateRefund handles the refund initiation request
func (h *RefundHandler) InitiateRefund(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req RefundRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	refund, err := h.refundService.InitiateRefund(req.PaymentID, req.Amount, req.Reason)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(refund)
}

// GetRefundDetails handles the request to fetch refund details
func (h *RefundHandler) GetRefundDetails(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	refundID := r.URL.Query().Get("refund_id")
	if refundID == "" {
		http.Error(w, "Refund ID is required", http.StatusBadRequest)
		return
	}

	refund, err := h.refundService.GetRefundDetails(refundID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(refund)
}

// GetRefundsForPayment handles the request to fetch all refunds for a payment
func (h *RefundHandler) GetRefundsForPayment(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	paymentID := r.URL.Query().Get("payment_id")
	if paymentID == "" {
		http.Error(w, "Payment ID is required", http.StatusBadRequest)
		return
	}

	refunds, err := h.refundService.GetRefundsForPayment(paymentID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(refunds)
}
