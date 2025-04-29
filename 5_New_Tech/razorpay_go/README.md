# Razorpay Webhook Implementation in Go

This project implements Razorpay webhooks using Go and the Gin web framework.

## Prerequisites

- Go 1.21 or higher
- Razorpay account (Test credentials configured)

## Configuration

The following credentials are configured:
- Razorpay Key: rzp_test_96Yw5IBIzsWSZt
- Webhook URL: http://117.216.46.51:8080/api/razorpay/webhook
- Alert Email: radium@aramisimaging.com

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd razorpay_go
```

2. Install dependencies:
```bash
go mod download
```

3. Run the application:
```bash
go run main.go
```

## Webhook Events

The application listens for the following Razorpay events:
- payment.authorized
- payment.failed
- payment.captured
- payment.dispute.created
- refund.failed
- refund.created

## Webhook Endpoint

The webhook endpoint is available at:
```
POST http://117.216.46.51:8080/api/razorpay/webhook
```

## Implementation Details

The application:
1. Sets up a webhook with Razorpay during startup using test credentials
2. Provides an endpoint to receive webhook events
3. Processes different types of payment events
4. Logs the webhook data for monitoring

## Security

Remember to:
- This setup uses test credentials - replace with production credentials for live deployment
- The webhook secret is set to "12345" - use a more secure secret in production
- Use HTTPS in production
- Follow Razorpay's security best practices

## Error Handling

The application includes basic error handling for:
- Invalid webhook payloads
- Missing configuration
- Webhook setup failures
- Server startup issues

## Contributing

Feel free to submit issues and enhancement requests! 