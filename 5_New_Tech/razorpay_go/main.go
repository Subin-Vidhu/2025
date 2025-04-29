package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	razorpay "github.com/razorpay/razorpay-go"
)

var client *razorpay.Client

func init() {
	// Initialize Razorpay client with provided credentials
	apiKey := "rzp_test_96Yw5IBIzsWSZt"
	apiSecret := "EGkwN8l2dMhGaTR7AP6teXJJ"
	client = razorpay.NewClient(apiKey, apiSecret)
}

func handleWebhook(c *gin.Context) {
	// Read the webhook payload
	var webhookData map[string]interface{}
	if err := c.BindJSON(&webhookData); err != nil {
		log.Printf("Error parsing webhook: %v", err)
		c.JSON(400, gin.H{"error": "Invalid webhook payload"})
		return
	}

	// Log the entire webhook payload for debugging
	log.Printf("Received webhook: %+v\n", webhookData)

	// Process different event types
	eventType, ok := webhookData["event"].(string)
	if !ok {
		c.JSON(400, gin.H{"error": "Event type not found in payload"})
		return
	}

	switch eventType {
	case "payment.authorized":
		log.Printf("Payment authorized: %+v", webhookData)
	case "payment.captured":
		log.Printf("Payment captured: %+v", webhookData)
	case "payment.failed":
		log.Printf("Payment failed: %+v", webhookData)
	case "refund.created":
		log.Printf("Refund created: %+v", webhookData)
	default:
		log.Printf("Received event type: %s", eventType)
	}

	c.JSON(200, gin.H{"status": "success"})
}

func main() {
	// Initialize Gin router
	r := gin.Default()

	// Webhook endpoint
	r.POST("/api/razorpay/webhook", handleWebhook)

	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server starting on port %s", port)
	log.Printf("Webhook URL: http://117.216.46.51:8080/api/razorpay/webhook")
	if err := r.Run(":" + port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
