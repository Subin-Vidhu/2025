package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    _ "github.com/mattn/go-sqlite3"
)

type Link struct {
    ID        string `json:"id"`
    Title     string `json:"title"`
    URL       string `json:"url"`
    IsActive  bool   `json:"is_active"`
}

var db *sql.DB

func initDB() {
    var err error
    db, err = sql.Open("sqlite3", "./linktree.db")
    if err != nil {
        log.Fatal(err)
    }

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

func getLinksHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
			respondWithError(w, http.StatusMethodNotAllowed, "Method not allowed")
			return
	}

	rows, err := db.Query("SELECT id, title, url, is_active FROM links")
	if err != nil {
			respondWithError(w, http.StatusInternalServerError, "Error fetching links")
			return
	}
	defer rows.Close()

	var links []Link
	for rows.Next() {
			var link Link
			err := rows.Scan(&link.ID, &link.Title, &link.URL, &link.IsActive)
			if err != nil {
					respondWithError(w, http.StatusInternalServerError, "Error scanning links")
					return
			}
			links = append(links, link)
	}

	respondWithJSON(w, http.StatusOK, links)
}

func addLinkHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
			respondWithError(w, http.StatusMethodNotAllowed, "Method not allowed")
			return
	}

	var link Link
	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&link); err != nil {
			respondWithError(w, http.StatusBadRequest, "Invalid request payload")
			return
	}
	defer r.Body.Close()

	// Generate a unique ID
	link.ID = fmt.Sprintf("%d", time.Now().UnixNano())
	link.IsActive = true

	_, err := db.Exec("INSERT INTO links (id, title, url, created_at, updated_at, is_active) VALUES (?, ?, ?, datetime('now'), datetime('now'), ?)",
			link.ID, link.Title, link.URL, link.IsActive)
	if err != nil {
			respondWithError(w, http.StatusInternalServerError, "Error creating link")
			return
	}

	respondWithJSON(w, http.StatusCreated, link)
}

func serveStaticFile(w http.ResponseWriter, r *http.Request, file string) {
	http.ServeFile(w, r, "static/"+file)
}

func main() {
    initDB()
    
    http.HandleFunc("/links", getLinksHandler)
    http.HandleFunc("/links/add", addLinkHandler)
    
    // Serve static files
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        serveStaticFile(w, r, "index.html")
    })
    
    fmt.Println("Server listening on port 8080")
    http.ListenAndServe(":8080", nil)
}
