package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
)

func initDB() *sql.DB {
	db, err := sql.Open("sqlite3", "./links.db")
	if err != nil {
		panic(err)
	}
	_, err = db.Exec("CREATE TABLE IF NOT EXISTS links (url TEXT, title TEXT)")
	if err != nil {
		panic(err)
	}
	return db
}

var db *sql.DB

func getLinksHandler(w http.ResponseWriter, r *http.Request) {
	rows, err := db.Query("SELECT url, title FROM links")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()
	var links Links
	for rows.Next() {
		var link Link
		err := rows.Scan(&link.URL, &link.Title)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		links = append(links, link)
	}
	if err := rows.Err(); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(links)
}

func addLinkHandler(w http.ResponseWriter, r *http.Request) {
	var newLink Link
	err := json.NewDecoder(r.Body).Decode(&newLink)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	_, err = db.Exec("INSERT INTO links (url, title) VALUES (?, ?)", newLink.URL, newLink.Title)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusCreated)
}

type Link struct {
	URL    string `json:"url"`
	Title  string `json:"title"`
}

type Links []Link

var links Links

func main() {
	http.HandleFunc("/links", getLinksHandler)
	http.HandleFunc("/links/add", addLinkHandler)
	fmt.Println("Server listening on port 8080")
	http.ListenAndServe(":8080", nil)
}
