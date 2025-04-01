package main

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
)

// Link represents a social media or external link
type Link struct {
	ID          string    `json:"id"`
	Title       string    `json:"title"`
	URL         string    `json:"url"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
	IsActive    bool      `json:"is_active"`
}

var db *sql.DB

func initDB() {
	var err error
	db, err = sql.Open("sqlite3", "./linktree.db")
	if err != nil {
		log.Fatal(err)
	}

	// Create links table if it doesn't exist
	createTableSQL := `
	CREATE TABLE IF NOT EXISTS links (
		id TEXT PRIMARY KEY,
		title TEXT NOT NULL,
		url TEXT NOT NULL,
		created_at DATETIME NOT NULL,
		updated_at DATETIME NOT NULL,
		is_active BOOLEAN NOT NULL DEFAULT TRUE
	);`

	_, err = db.Exec(createTableSQL)
	if err != nil {
		log.Fatal(err)
	}
}

func respondWithJSON(w http.ResponseWriter, code int, payload interface{}) {
	response, _ := json.Marshal(payload)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write(response)
}

func respondWithError(w http.ResponseWriter, code int, message string) {
	respondWithJSON(w, code, map[string]string{"error": message})
}

// Handlers
func createLink(w http.ResponseWriter, r *http.Request) {
	var link Link
	if err := json.NewDecoder(r.Body).Decode(&link); err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid request payload")
		return
	}

	link.ID = time.Now().Format("20060102150405")
	link.CreatedAt = time.Now()
	link.UpdatedAt = time.Now()
	link.IsActive = true

	_, err := db.Exec(
		"INSERT INTO links (id, title, url, created_at, updated_at, is_active) VALUES (?, ?, ?, ?, ?, ?)",
		link.ID, link.Title, link.URL, link.CreatedAt, link.UpdatedAt, link.IsActive,
	)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusCreated, link)
}

func getLinks(w http.ResponseWriter, r *http.Request) {
	rows, err := db.Query("SELECT id, title, url, created_at, updated_at, is_active FROM links WHERE is_active = true")
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}
	defer rows.Close()

	var links []Link
	for rows.Next() {
		var link Link
		err := rows.Scan(&link.ID, &link.Title, &link.URL, &link.CreatedAt, &link.UpdatedAt, &link.IsActive)
		if err != nil {
			respondWithError(w, http.StatusInternalServerError, err.Error())
			return
		}
		links = append(links, link)
	}

	respondWithJSON(w, http.StatusOK, links)
}

func getLink(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	var link Link
	err := db.QueryRow(
		"SELECT id, title, url, created_at, updated_at, is_active FROM links WHERE id = ?",
		params["id"],
	).Scan(&link.ID, &link.Title, &link.URL, &link.CreatedAt, &link.UpdatedAt, &link.IsActive)

	if err == sql.ErrNoRows {
		respondWithError(w, http.StatusNotFound, "Link not found")
		return
	} else if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusOK, link)
}

func updateLink(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	var updatedLink Link
	if err := json.NewDecoder(r.Body).Decode(&updatedLink); err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid request payload")
		return
	}

	result, err := db.Exec(
		"UPDATE links SET title = ?, url = ?, updated_at = ? WHERE id = ?",
		updatedLink.Title, updatedLink.URL, time.Now(), params["id"],
	)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	if rowsAffected == 0 {
		respondWithError(w, http.StatusNotFound, "Link not found")
		return
	}

	// Get the updated link
	var link Link
	err = db.QueryRow(
		"SELECT id, title, url, created_at, updated_at, is_active FROM links WHERE id = ?",
		params["id"],
	).Scan(&link.ID, &link.Title, &link.URL, &link.CreatedAt, &link.UpdatedAt, &link.IsActive)

	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusOK, link)
}

func deleteLink(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	result, err := db.Exec(
		"UPDATE links SET is_active = false, updated_at = ? WHERE id = ?",
		time.Now(), params["id"],
	)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	if rowsAffected == 0 {
		respondWithError(w, http.StatusNotFound, "Link not found")
		return
	}

	respondWithJSON(w, http.StatusOK, map[string]string{"result": "success"})
}

// Serve static files and handle frontend routes
func serveStaticFile(w http.ResponseWriter, r *http.Request, file string) {
	http.ServeFile(w, r, "static/"+file)
}

func main() {
	initDB()
	defer db.Close()

	router := mux.NewRouter()

	// API routes
	router.HandleFunc("/api/links", getLinks).Methods("GET")
	router.HandleFunc("/api/links", createLink).Methods("POST")
	router.HandleFunc("/api/links/{id}", getLink).Methods("GET")
	router.HandleFunc("/api/links/{id}", updateLink).Methods("PUT")
	router.HandleFunc("/api/links/{id}", deleteLink).Methods("DELETE")

	// Static file server
	router.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("static"))))

	// Frontend routes
	router.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		serveStaticFile(w, r, "index.html")
	})
	router.HandleFunc("/admin", func(w http.ResponseWriter, r *http.Request) {
		serveStaticFile(w, r, "admin.html")
	})

	// Start server
	log.Printf("Server starting on :8080")
	if err := http.ListenAndServe(":8080", router); err != nil {
		log.Fatal(err)
	}
}
