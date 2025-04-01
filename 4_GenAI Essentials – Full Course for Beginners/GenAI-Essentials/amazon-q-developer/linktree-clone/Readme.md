
## Examples of Curls

### Get profile

```sh
curl http://localhost:8000/profile
```

### Update profile

```sh
curl -X PUT http://localhost:8000/profile \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","bio":"Full Stack Developer","picture":"new.jpg","links":[]}'
```

### Add a link

```sh
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"id":"1","name":"ExamPro Training Inc","url":"https://www.exampro.co/"}'
```

### Delete a link

```sh
curl -X DELETE http://localhost:8000/links/1
```

## Create and Seed Sqlite3 Database

```sh
sqlite3 profile.db "
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    bio TEXT,
    picture TEXT
);

CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL
);

INSERT INTO profiles (name, bio, picture)
VALUES ('John Doe', 'Software Developer', 'profile.jpg');

INSERT INTO links (name, url)
VALUES 
    ('GitHub', 'https://github.com/johndoe'),
    ('LinkedIn', 'https://linkedin.com/in/johndoe'),
    ('Twitter', 'https://twitter.com/johndoe');"
```