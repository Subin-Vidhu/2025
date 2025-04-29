package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"time"
)

const webhookURL = "http://117.216.46.51:8080/api/razorpay/webhook"

type WebhookRequest struct {
	Event     string  `json:"event"`
	PaymentID string  `json:"paymentId"`
	Amount    float64 `json:"amount"`
	Currency  string  `json:"currency"`
}

func simulateWebhookEvent(event, paymentID string, amount float64, currency string) (map[string]interface{}, error) {
	status := getStatusForEvent(event)
	payload := map[string]interface{}{
		"entity":     "event",
		"account_id": "acc_123456",
		"event":      event,
		"contains":   []string{"payment"},
		"payload": map[string]interface{}{
			"payment": map[string]interface{}{
				"entity": map[string]interface{}{
					"id":       paymentID,
					"amount":   amount,
					"currency": currency,
					"status":   status,
				},
			},
		},
		"created_at": time.Now().Unix(),
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("error marshaling payload: %v", err)
	}

	resp, err := http.Post(webhookURL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("error sending webhook: %v", err)
	}
	defer resp.Body.Close()

	var response map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, fmt.Errorf("error decoding response: %v", err)
	}

	return response, nil
}

func getStatusForEvent(event string) string {
	switch event {
	case "payment.authorized":
		return "authorized"
	case "payment.captured":
		return "captured"
	case "payment.failed":
		return "failed"
	case "refund.created":
		return "refund_initiated"
	case "refund.processed":
		return "refund_processed"
	case "refund.failed":
		return "refund_failed"
	default:
		return "unknown"
	}
}

func handleSimulate(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req WebhookRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, fmt.Sprintf("Error decoding request: %v", err), http.StatusBadRequest)
		return
	}

	response, err := simulateWebhookEvent(req.Event, req.PaymentID, req.Amount, req.Currency)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error simulating webhook: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func handleIndex(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Use relative path for development
	templatePath := "cmd/tester/templates/index.html"
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
	http.HandleFunc("/simulate", handleSimulate)

	log.Printf("Starting webhook tester on http://localhost:%s", port)
	log.Printf("Targeting webhook URL: %s", webhookURL)

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
