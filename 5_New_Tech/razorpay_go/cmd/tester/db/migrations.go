package db

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq"
)

// InitDB initializes the database and creates necessary tables
func InitDB(connStr string) (*sql.DB, error) {
	log.Printf("Attempting to connect to database...")
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, fmt.Errorf("error opening database: %v", err)
	}

	// Test the connection
	log.Printf("Testing database connection...")
	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("error connecting to the database: %v", err)
	}
	log.Printf("Database connection successful")

	log.Printf("Creating tables...")
	err = createTables(db)
	if err != nil {
		return nil, fmt.Errorf("error creating tables: %v", err)
	}
	log.Printf("Tables created successfully")

	return db, nil
}

func createTables(db *sql.DB) error {
	// Create payments table
	log.Printf("Creating payments table...")
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS payments (
			id SERIAL PRIMARY KEY,
			order_id TEXT NOT NULL,
			payment_id TEXT NOT NULL UNIQUE,
			amount DECIMAL(10,2) NOT NULL,
			currency TEXT NOT NULL,
			status TEXT NOT NULL,
			payment_method TEXT,
			refundable_amount DECIMAL(10,2) NOT NULL,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`)
	if err != nil {
		return fmt.Errorf("error creating payments table: %v", err)
	}
	log.Printf("Payments table created successfully")

	// Create refunds table
	log.Printf("Creating refunds table...")
	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS refunds (
			id SERIAL PRIMARY KEY,
			payment_id TEXT NOT NULL,
			refund_id TEXT NOT NULL UNIQUE,
			amount DECIMAL(10,2) NOT NULL,
			currency TEXT NOT NULL,
			status TEXT NOT NULL,
			reason TEXT,
			notes TEXT,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
		)
	`)
	if err != nil {
		return fmt.Errorf("error creating refunds table: %v", err)
	}
	log.Printf("Refunds table created successfully")

	// Verify tables exist
	var tableCount int
	err = db.QueryRow(`
		SELECT COUNT(*) 
		FROM information_schema.tables 
		WHERE table_schema = 'public' 
		AND table_name IN ('payments', 'refunds')
	`).Scan(&tableCount)
	if err != nil {
		return fmt.Errorf("error verifying tables: %v", err)
	}
	if tableCount != 2 {
		return fmt.Errorf("expected 2 tables, found %d tables", tableCount)
	}
	log.Printf("Verified both tables exist")

	return nil
}
