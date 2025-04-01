package main

import (
    "github.com/gin-gonic/gin"
    "github.com/joho/godotenv"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
    "log"
    "net/http"
    "os"
)

type Link struct {
    ID   uint   `json:"id" gorm:"primaryKey"`
    Name string `json:"name"`
    URL  string `json:"url"`
}

func main() {
    err := godotenv.Load()
    if err != nil {
        log.Fatal("Error loading .env file")
    }

    db, err := gorm.Open(sqlite.Open("links.db"), &gorm.Config{})
    if err != nil {
        log.Fatal("Failed to connect to database")
    }

    db.AutoMigrate(&Link{})

    r := gin.Default()

    r.GET("/links", func(c *gin.Context) {
        var links []Link
        db.Find(&links)
        c.JSON(http.StatusOK, gin.H{
            "profile": map[string]string{
                "name":  "John Doe",
                "email": "john.doe@example.com",
            },
            "links": links,
        })
    })

    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    r.Run(":" + port)
}