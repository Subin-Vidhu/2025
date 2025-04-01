## How to install Go on Ubunutu WSL

```sh
sudo apt install golang-go
```

## How to Build And Run

```sh
go build -o linktree-clone
./linktree-clone
```

## Run without building

```sh
go run main.go
```

## Create SQlite Table and Seed Data

run the following commands to create and seed an sqlite database called links.db

```sh
sqlite3 links.db <<EOF
CREATE TABLE links (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT NOT NULL
);

INSERT INTO links (title, url) VALUES ('GitHub', 'https://github.com');
INSERT INTO links (title, url) VALUES ('Google', 'https://google.com');
EOF
```

```sh
sqlite3 links.db <<EOF
INSERT INTO links (title, url) VALUES ('ExamPro Training Inc', 'https://www.exampro.co');
EOF
```
