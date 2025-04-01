package main

import (
    "encoding/json"
    "log"
    "net/http"
    "github.com/gorilla/mux"
    "database/sql"
    _ "github.com/mattn/go-sqlite3"
)

// Models
type Link struct {
    ID    string `json:"id"`
    Name  string `json:"name"`
    URL   string `json:"url"`
}

type Profile struct {
    Name     string `json:"name"`
    Bio      string `json:"bio"`
    Picture  string `json:"picture"`
    Links    []Link `json:"links"`
}

var profile Profile

// Handlers
func getProfile(w http.ResponseWriter, r *http.Request) {
    // Initialize profile data from SQLite database
    db, err := sql.Open("sqlite3", "profile.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Get profile data
    row := db.QueryRow("SELECT name, bio, picture FROM profiles LIMIT 1")
    err = row.Scan(&profile.Name, &profile.Bio, &profile.Picture)
    if err != nil {
        log.Fatal(err)
    }

    // Get links
    rows, err := db.Query("SELECT id, name, url FROM links")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    profile.Links = []Link{}
    for rows.Next() {
        var link Link
        err = rows.Scan(&link.ID, &link.Name, &link.URL)
        if err != nil {
            log.Fatal(err)
        }
        profile.Links = append(profile.Links, link)
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(profile)
}

func updateProfile(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    var updatedProfile Profile
    json.NewDecoder(r.Body).Decode(&updatedProfile)

    // Open database connection
    db, err := sql.Open("sqlite3", "profile.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Update profile in database
    _, err = db.Exec("UPDATE profiles SET name = ?, bio = ?, picture = ? WHERE rowid = 1",
        updatedProfile.Name, updatedProfile.Bio, updatedProfile.Picture)
    if err != nil {
        log.Fatal(err)
    }

    // Update global profile variable
    profile = updatedProfile
    json.NewEncoder(w).Encode(profile)
}

func addLink(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    var link Link
    err := json.NewDecoder(r.Body).Decode(&link)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // Open database connection
    db, err := sql.Open("sqlite3", "profile.db")
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    defer db.Close()

    // Insert new link into database
    result, err := db.Exec("INSERT INTO links (name, url) VALUES (?, ?)", 
        link.Name, link.URL)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Get the ID of the inserted link
    id, err := result.LastInsertId()
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    link.ID = string(id)

    // Return the newly created link
    json.NewEncoder(w).Encode(link)
}


func deleteLink(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    params := mux.Vars(r)

    // Open database connection
    db, err := sql.Open("sqlite3", "profile.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Delete link from database
    _, err = db.Exec("DELETE FROM links WHERE id = ?", params["id"])
    if err != nil {
        log.Fatal(err)
    }

    // Update links array
    for i, link := range profile.Links {
        if link.ID == params["id"] {
            profile.Links = append(profile.Links[:i], profile.Links[i+1:]...)
            break
        }
    }
    json.NewEncoder(w).Encode(profile.Links)
}

func main() {
    // Initialize router
    router := mux.NewRouter()

    // Routes
    router.HandleFunc("/profile", getProfile).Methods("GET")
    router.HandleFunc("/profile", updateProfile).Methods("PUT")
    router.HandleFunc("/links", addLink).Methods("POST")
    router.HandleFunc("/links/{id}", deleteLink).Methods("DELETE")



    // Start server
    log.Fatal(http.ListenAndServe(":8000", router))
}
