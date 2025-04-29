package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/razorpay/razorpay-go"
)

// Test mode keys - replace these with your test mode keys from Razorpay Dashboard
const (
	keyID     = "rzp_test_96Yw5IBIzsWSZt"
	keySecret = "EGkwN8l2dMhGaTR7AP6teXJJ"
)

// PaymentState tracks the state of payments
type PaymentState struct {
	Status    string
	UpdatedAt time.Time
}

// Global payment state tracker
var (
	paymentStates = make(map[string]PaymentState)
	stateMutex    sync.RWMutex
)

// Update payment state
func updatePaymentState(orderID string, status string) {
	stateMutex.Lock()
	defer stateMutex.Unlock()
	paymentStates[orderID] = PaymentState{
		Status:    status,
		UpdatedAt: time.Now(),
	}
}

// Get payment state
func getPaymentState(orderID string) (PaymentState, bool) {
	stateMutex.RLock()
	defer stateMutex.RUnlock()
	state, exists := paymentStates[orderID]
	return state, exists
}

type OrderRequest struct {
	Amount   float64 `json:"amount"`
	Currency string  `json:"currency"`
}

type OrderResponse struct {
	OrderID     string  `json:"orderId"`
	Amount      float64 `json:"amount"`
	Currency    string  `json:"currency"`
	KeyID       string  `json:"keyId"`
	CallbackURL string  `json:"callbackUrl"`
}

func createOrder(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req OrderRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, fmt.Sprintf("Error decoding request: %v", err), http.StatusBadRequest)
		return
	}

	log.Printf("Creating order with amount: %v %s", req.Amount, req.Currency)
	log.Printf("Using key ID: %s", keyID)
	log.Printf("Using secret (first 4 chars): %s", keySecret[:4])

	client := razorpay.NewClient(keyID, keySecret)

	// Validate amount
	if req.Amount <= 0 {
		http.Error(w, "Amount must be greater than 0", http.StatusBadRequest)
		return
	}

	// Convert amount to paise/cents
	amountInPaise := int64(req.Amount * 100)
	log.Printf("Amount in paise: %d", amountInPaise)

	data := map[string]interface{}{
		"amount":   amountInPaise,
		"currency": req.Currency,
		"notes": map[string]interface{}{
			"test_mode": "true",
		},
	}

	log.Printf("Sending order request to Razorpay: %+v", data)
	order, err := client.Order.Create(data, nil)
	if err != nil {
		log.Printf("Error from Razorpay: %v", err)
		http.Error(w, fmt.Sprintf("Error creating order: %v", err), http.StatusInternalServerError)
		return
	}

	log.Printf("Order created successfully: %+v", order)

	response := OrderResponse{
		OrderID:     order["id"].(string),
		Amount:      order["amount"].(float64),
		Currency:    order["currency"].(string),
		KeyID:       keyID,
		CallbackURL: "http://localhost:3002/payment/callback",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func handlePaymentCallback(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		log.Printf("Error parsing form: %v", err)
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

	// Create Razorpay client
	client := razorpay.NewClient(keyID, keySecret)

	event := r.FormValue("event")
	orderId := r.FormValue("razorpay_order_id")
	log.Printf("Payment callback received. Event: %s, Order ID: %s", event, orderId)

	// Check if payment was already failed or cancelled
	if state, exists := getPaymentState(orderId); exists {
		if state.Status == "failed" || state.Status == "cancelled" {
			log.Printf("Payment already marked as %s, ignoring %s event", state.Status, event)
			response := map[string]interface{}{
				"status":  state.Status,
				"message": fmt.Sprintf("Payment was already %s", state.Status),
			}
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(response)
			return
		}
	}

	switch event {
	case "payment.success":
		paymentId := r.FormValue("razorpay_payment_id")
		signature := r.FormValue("razorpay_signature")

		log.Printf("Verifying payment - Payment ID: %s, Order ID: %s", paymentId, orderId)
		log.Printf("Received signature: %s", signature)

		// Verify payment signature
		data := orderId + "|" + paymentId
		h := hmac.New(sha256.New, []byte(keySecret))
		h.Write([]byte(data))
		expectedSignature := hex.EncodeToString(h.Sum(nil))
		log.Printf("Expected signature: %s", expectedSignature)

		if signature != expectedSignature {
			log.Printf("Signature verification failed")
			updatePaymentState(orderId, "failed")
			http.Error(w, "Invalid payment signature", http.StatusBadRequest)
			return
		}

		log.Printf("Signature verification successful")

		// Fetch payment details
		payment, err := client.Payment.Fetch(paymentId, map[string]interface{}{}, map[string]string{})
		if err != nil {
			log.Printf("Error fetching payment: %v", err)
			updatePaymentState(orderId, "failed")
			http.Error(w, "Error fetching payment details", http.StatusInternalServerError)
			return
		}

		log.Printf("Payment details fetched successfully: %+v", payment)

		// Check payment status
		if status, ok := payment["status"].(string); ok {
			if status != "captured" {
				log.Printf("Payment not captured. Status: %s", status)
				updatePaymentState(orderId, "failed")
				response := map[string]interface{}{
					"status":  "failed",
					"message": fmt.Sprintf("Payment not captured. Status: %s", status),
				}
				w.Header().Set("Content-Type", "application/json")
				json.NewEncoder(w).Encode(response)
				return
			}
		}

		updatePaymentState(orderId, "success")
		response := map[string]interface{}{
			"status":  "success",
			"message": "Payment successful",
			"data":    payment,
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)

	case "payment.failed":
		errorCode := r.FormValue("error_code")
		errorDesc := r.FormValue("error_description")
		log.Printf("Payment failed - Error Code: %s, Description: %s", errorCode, errorDesc)

		updatePaymentState(orderId, "failed")
		response := map[string]interface{}{
			"status":  "failed",
			"message": fmt.Sprintf("Payment failed: %s", errorDesc),
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)

	case "payment.cancelled":
		log.Printf("Payment cancelled for order: %s", orderId)

		updatePaymentState(orderId, "cancelled")
		response := map[string]interface{}{
			"status":  "cancelled",
			"message": "Payment cancelled by user",
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)

	default:
		http.Error(w, "Unknown event type", http.StatusBadRequest)
	}
}

func handleIndex(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Get absolute path to the template
	workingDir, err := os.Getwd()
	if err != nil {
		http.Error(w, fmt.Sprintf("Error getting working directory: %v", err), http.StatusInternalServerError)
		return
	}

	templatePath := filepath.Join(workingDir, "cmd", "tester", "templates", "index.html")
	tmpl, err := template.ParseFiles(templatePath)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error parsing template: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/html")
	if err := tmpl.Execute(w, nil); err != nil {
		http.Error(w, fmt.Sprintf("Error executing template: %v", err), http.StatusInternalServerError)
		return
	}
}

func main() {
	port := "3002"

	http.HandleFunc("/", handleIndex)
	http.HandleFunc("/order/create", createOrder)
	http.HandleFunc("/payment/callback", handlePaymentCallback)

	log.Printf("Starting Razorpay test payment server on http://localhost:%s", port)
	log.Printf("Using test mode - Make sure to replace the API keys with your test mode keys")

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
