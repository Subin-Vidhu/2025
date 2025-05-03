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

	"razorpay_go/cmd/tester/db"
	"razorpay_go/cmd/tester/handlers"
	"razorpay_go/cmd/tester/models"
	"razorpay_go/cmd/tester/repository"
	"razorpay_go/cmd/tester/service"

	"github.com/razorpay/razorpay-go"
)

// Test mode keys - replace these with your test mode keys from Razorpay Dashboard
const (
	keyID     = "rzp_test_FX3Nq50Trf2KzB"
	keySecret = "dwPmbHcBQX6JkCvwJlbi8yAk"

	// Database configuration
	dbHost     = "localhost"
	dbPort     = 5432
	dbUser     = "postgres"
	dbPassword = "password"
	dbName     = "razorpay_test"
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

func handlePaymentCallback(w http.ResponseWriter, r *http.Request, repo *repository.Repository, client *razorpay.Client) {
	if err := r.ParseForm(); err != nil {
		log.Printf("Error parsing form: %v", err)
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

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

		log.Printf("Processing successful payment - Payment ID: %s, Order ID: %s", paymentId, orderId)

		// Verify payment signature
		data := orderId + "|" + paymentId
		h := hmac.New(sha256.New, []byte(keySecret))
		h.Write([]byte(data))
		expectedSignature := hex.EncodeToString(h.Sum(nil))

		if signature != expectedSignature {
			log.Printf("Signature verification failed")
			updatePaymentState(orderId, "failed")
			http.Error(w, "Invalid payment signature", http.StatusBadRequest)
			return
		}

		log.Printf("Signature verification successful")

		// Fetch payment details from Razorpay
		payment, err := client.Payment.Fetch(paymentId, nil, nil)
		if err != nil {
			log.Printf("Error fetching payment from Razorpay: %v", err)
			updatePaymentState(orderId, "failed")
			http.Error(w, "Error fetching payment details", http.StatusInternalServerError)
			return
		}

		log.Printf("Payment details fetched from Razorpay: %+v", payment)

		// Store payment details in database
		amount := float64(payment["amount"].(float64)) / 100
		paymentRecord := &models.Payment{
			OrderID:          orderId,
			PaymentID:        paymentId,
			Amount:           amount,
			Currency:         payment["currency"].(string),
			Status:           payment["status"].(string),
			PaymentMethod:    payment["method"].(string),
			RefundableAmount: amount, // Initially, full amount is refundable
		}

		log.Printf("Saving payment record to database: %+v", paymentRecord)
		err = repo.SavePayment(paymentRecord)
		if err != nil {
			log.Printf("Error saving payment to database: %v", err)
			http.Error(w, "Error saving payment details", http.StatusInternalServerError)
			return
		}
		log.Printf("Payment record saved successfully")

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
	// Initialize database connection string
	dbConnStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		dbHost, dbPort, dbUser, dbPassword, dbName)

	log.Printf("Connecting to database with connection string: %s", dbConnStr)

	// Initialize database
	database, err := db.InitDB(dbConnStr)
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}
	defer database.Close()

	// Test query to verify database connection
	var testCount int
	err = database.QueryRow("SELECT COUNT(*) FROM payments").Scan(&testCount)
	if err != nil {
		log.Fatalf("Failed to query database: %v", err)
	}
	log.Printf("Database connection verified. Current payment count: %d", testCount)

	// Initialize repository
	repo := repository.NewRepository(database)

	// Initialize Razorpay client
	client := razorpay.NewClient(keyID, keySecret)

	// Initialize services
	refundService := service.NewRefundService(repo, client)

	// Initialize handlers
	refundHandler := handlers.NewRefundHandler(refundService)

	// Register routes
	http.HandleFunc("/", handleIndex)
	http.HandleFunc("/order/create", createOrder)

	// Register payment callback handler (only once)
	http.HandleFunc("/payment/callback", func(w http.ResponseWriter, r *http.Request) {
		handlePaymentCallback(w, r, repo, client)
	})

	// Refund routes
	http.HandleFunc("/refund/initiate", refundHandler.InitiateRefund)
	http.HandleFunc("/refund/details", refundHandler.GetRefundDetails)
	http.HandleFunc("/refund/list", refundHandler.GetRefundsForPayment)

	log.Printf("Server is running on http://localhost:3002")
	log.Fatal(http.ListenAndServe(":3002", nil))
}
