package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
	"github.com/rs/cors"
)

type Link struct {
	ID          string `json:"id"`
	Title       string `json:"title"`
	URL         string `json:"url"`
	Description string `json:"description,omitempty"`
}

type Profile struct {
	Name      string `json:"name"`
	Bio       string `json:"bio"`
	AvatarURL string `json:"avatarUrl"`
	Links     []Link `json:"links"`
}

var db *sql.DB

func initDB() {
	var err error
	db, err = sql.Open("sqlite3", "./linktree.db")
	if err != nil {
		log.Fatal(err)
	}

	// Create tables if they don't exist
	createTables := `
	CREATE TABLE IF NOT EXISTS profile (
		id INTEGER PRIMARY KEY,
		name TEXT NOT NULL,
		bio TEXT,
		avatar_url TEXT
	);
	CREATE TABLE IF NOT EXISTS links (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		url TEXT NOT NULL,
		description TEXT
	);`

	_, err = db.Exec(createTables)
	if err != nil {
		log.Fatal(err)
	}

	// Insert default profile if not exists
	var count int
	err = db.QueryRow("SELECT COUNT(*) FROM profile").Scan(&count)
	if err != nil {
		log.Fatal(err)
	}

	if count == 0 {
		_, err = db.Exec(`
			INSERT INTO profile (id, name, bio, avatar_url)
			VALUES (1, 'John Doe', 'Software Developer & Tech Enthusiast', 'https://via.placeholder.com/150')
		`)
		if err != nil {
			log.Fatal(err)
		}

		// Insert default links
		defaultLinks := []Link{
			{Title: "GitHub", URL: "https://github.com", Description: "Check out my projects"},
			{Title: "LinkedIn", URL: "https://linkedin.com", Description: "Connect with me"},
		}

		for _, link := range defaultLinks {
			_, err = db.Exec(`
				INSERT INTO links (title, url, description)
				VALUES (?, ?, ?)
			`, link.Title, link.URL, link.Description)
			if err != nil {
				log.Fatal(err)
			}
		}
	}
}

func getProfile(w http.ResponseWriter, r *http.Request) {
	var profile Profile
	
	// Get profile data
	err := db.QueryRow(`
		SELECT name, bio, avatar_url
		FROM profile
		WHERE id = 1
	`).Scan(&profile.Name, &profile.Bio, &profile.AvatarURL)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Get links
	rows, err := db.Query(`
		SELECT id, title, url, description
		FROM links
	`)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	for rows.Next() {
		var link Link
		err := rows.Scan(&link.ID, &link.Title, &link.URL, &link.Description)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		profile.Links = append(profile.Links, link)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(profile)
}

func updateProfile(w http.ResponseWriter, r *http.Request) {
	var profile Profile
	if err := json.NewDecoder(r.Body).Decode(&profile); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	tx, err := db.Begin()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Update profile
	_, err = tx.Exec(`
		UPDATE profile
		SET name = ?, bio = ?, avatar_url = ?
		WHERE id = 1
	`, profile.Name, profile.Bio, profile.AvatarURL)
	if err != nil {
		tx.Rollback()
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Delete existing links
	_, err = tx.Exec("DELETE FROM links")
	if err != nil {
		tx.Rollback()
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Insert new links
	for _, link := range profile.Links {
		_, err = tx.Exec(`
			INSERT INTO links (title, url, description)
			VALUES (?, ?, ?)
		`, link.Title, link.URL, link.Description)
		if err != nil {
			tx.Rollback()
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	}

	if err := tx.Commit(); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(profile)
}

func addLink(w http.ResponseWriter, r *http.Request) {
	var newLink Link
	if err := json.NewDecoder(r.Body).Decode(&newLink); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	result, err := db.Exec(`
		INSERT INTO links (title, url, description)
		VALUES (?, ?, ?)
	`, newLink.Title, newLink.URL, newLink.Description)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	id, _ := result.LastInsertId()
	newLink.ID = string(id)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(newLink)
}

func main() {
	// Initialize database
	initDB()
	defer db.Close()

	router := mux.NewRouter()

	// API routes
	router.HandleFunc("/api/profile", getProfile).Methods("GET")
	router.HandleFunc("/api/profile", updateProfile).Methods("PUT")
	router.HandleFunc("/api/links", addLink).Methods("POST")

	// Serve static files
	router.PathPrefix("/").Handler(http.FileServer(http.Dir("static")))

	// Setup CORS
	c := cors.New(cors.Options{
		AllowedOrigins: []string{"*"},
		AllowedMethods: []string{"GET", "POST", "PUT", "DELETE"},
		AllowedHeaders: []string{"Content-Type"},
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, c.Handler(router)))
}