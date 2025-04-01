# LinkTree Clone API

A simple API-driven clone of LinkTree built with Go and SQLite3.

## Prerequisites

- Go 1.16 or higher
- SQLite3

## Installation

1. Install the required Go dependencies:
```bash
go get github.com/gorilla/mux
go get github.com/mattn/go-sqlite3
```

2. Run the application:
```bash
go run main.go
```

The server will start on `http://localhost:8080`.

## Database Seeding

To seed the database with some initial data, you can use the following command:

```bash
sqlite3 linktree.db << EOF
INSERT INTO links (id, title, url, created_at, updated_at, is_active) 
VALUES 
('20230101000001', 'GitHub', 'https://github.com', datetime('now'), datetime('now'), 1),
('20230101000002', 'LinkedIn', 'https://linkedin.com', datetime('now'), datetime('now'), 1),
('20230101000003', 'Twitter', 'https://twitter.com', datetime('now'), datetime('now'), 1);
EOF
```

## API Endpoints

- `GET /api/links` - Get all active links
- `POST /api/links` - Create a new link
- `GET /api/links/{id}` - Get a specific link
- `PUT /api/links/{id}` - Update a link
- `DELETE /api/links/{id}` - Soft delete a link

### Example Requests

Create a new link:
```bash
curl -X POST http://localhost:8080/api/links \
  -H "Content-Type: application/json" \
  -d '{"title":"My Website","url":"https://example.com"}'
```

Get all links:
```bash
curl http://localhost:8080/api/links
```

Update a link:
```bash
curl -X PUT http://localhost:8080/api/links/20230101000001 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","url":"https://updated-url.com"}'
```

Delete a link:
```bash
curl -X DELETE http://localhost:8080/api/links/20230101000001
``` 