# Razorpay Payment Integration in Go

This project implements a Razorpay payment integration using Go, demonstrating how to create orders, handle payments, and process callbacks in test mode.

## Features

- Create and process test payments
- Handle payment success, failure, and cancellation events
- Real-time logging of payment events
- Test mode integration with Razorpay
- Modern UI with Bootstrap
- Detailed event logging both client and server-side

## Prerequisites

- Go 1.21 or higher
- Razorpay test mode account and API keys
- Web browser with JavaScript enabled

## Configuration

The application uses Razorpay test mode credentials:
- Key ID: rzp_test_96Yw5IBIzsWSZt
- Server Port: 3002
- Callback URL: http://localhost:3002/payment/callback

## Project Structure

```
razorpay_go/
├── cmd/
│   └── tester/
│       ├── main.go           # Server implementation
│       └── templates/
│           └── index.html    # Payment UI template
├── go.mod
├── go.sum
└── README.md
```

## Setup and Running

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
# From project root
go run cmd/tester/main.go
```

The server will start at `http://localhost:3002`

## Testing Payments

1. Open `http://localhost:3002` in your browser
2. Enter an amount (e.g., 1000) and select currency (INR)
3. Click "Create Payment"

### Test Card Details
- Card Number: 5267 3181 8797 5449
- Expiry: Any future date (e.g., 12/25)
- CVV: Any 3 digits (e.g., 123)
- Name: Any name
- 3D Secure Password: 1234

### Test Scenarios

1. **Successful Payment**:
   - Use the test card details above
   - Complete the payment flow
   - Check success logs in browser and server console

2. **Failed Payment**:
   - Use card number: 4111 1111 1111 1111
   - This will simulate a failed payment
   - Check failure logs

3. **Cancelled Payment**:
   - Start a payment
   - Click the close (X) button on the payment modal
   - Check cancellation logs

## Implementation Details

The application:
1. Creates orders through Razorpay's API
2. Handles payment callbacks and signature verification
3. Processes different payment events (success/failure/cancellation)
4. Provides detailed logging in both UI and server
5. Uses Bootstrap for a responsive UI
6. Implements proper error handling

## Running in Terminal

To run the application from your terminal:

1. Open terminal/command prompt
2. Navigate to project directory:
```bash
cd path/to/razorpay_go
```

3. Start the server:
```bash
go run cmd/tester/main.go
```

4. To stop the server:
   - Press Ctrl+C in the terminal
   - Or close the terminal window

## Security Notes

- This is a test mode implementation
- Replace test API keys with production keys for live deployment
- Use HTTPS in production
- Follow Razorpay's security best practices
- Don't expose API keys in client-side code in production

## Error Handling

The application includes error handling for:
- Invalid payment requests
- Failed order creation
- Payment verification failures
- Server errors
- Client-side errors

## Monitoring

- Check the Response Log in the UI for real-time events
- Server console shows detailed backend logs
- All payment events are logged with timestamps

## Contributing

Feel free to submit issues and enhancement requests! 