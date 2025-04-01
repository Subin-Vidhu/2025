# LinkTree Clone

A simple LinkTree clone built with Go and SQLite3, featuring a REST API and a clean, modern UI.

## Prerequisites

- Go 1.21 or higher
- SQLite3

## Installation

1. Clone the repository
2. Install dependencies:
```bash
go mod tidy
```

## Database Setup

The application will automatically create the database and tables when started. However, if you want to manually seed the database, you can use the following commands:

```bash
# Create the database and tables
sqlite3 linktree.db << 'EOF'
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
);

-- Insert default profile
INSERT INTO profile (id, name, bio, avatar_url)
VALUES (1, 'John Doe', 'Software Developer & Tech Enthusiast', 'https://via.placeholder.com/150');

-- Insert sample links
INSERT INTO links (title, url, description)
VALUES 
    ('GitHub', 'https://github.com', 'Check out my projects'),
    ('LinkedIn', 'https://linkedin.com', 'Connect with me');
EOF
```

## Running the Application

```bash
go run main.go
```

The server will start on port 8080 (or the port specified in the PORT environment variable).

## API Endpoints

- `GET /api/profile`: Get the user profile and all links
- `PUT /api/profile`: Update the user profile
- `POST /api/links`: Add a new link

## Example API Usage

### Get Profile
```bash
curl http://localhost:8080/api/profile
```

### Add New Link
```bash
curl -X POST http://localhost:8080/api/links \
  -H "Content-Type: application/json" \
  -d '{"title":"Twitter","url":"https://twitter.com","description":"Follow me"}'
```

### Update Profile
```bash
curl -X PUT http://localhost:8080/api/profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "bio": "Full Stack Developer",
    "avatarUrl": "https://via.placeholder.com/150",
    "links": [
      {
        "title": "Portfolio",
        "url": "https://portfolio.com",
        "description": "My work"
      }
    ]
  }'
```
