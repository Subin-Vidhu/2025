#!/bin/bash
sqlite3 linktree.db << 'END_SQL'
INSERT INTO links (id, title, url, created_at, updated_at, is_active) VALUES
('1', 'GitHub Profile', 'https://github.com/yourusername', datetime('now'), datetime('now'), 1),
('2', 'LinkedIn', 'https://linkedin.com/in/yourusername', datetime('now'), datetime('now'), 1),
('3', 'Portfolio Website', 'https://yourportfolio.com', datetime('now'), datetime('now'), 1),
('4', 'Twitter', 'https://twitter.com/yourusername', datetime('now'), datetime('now'), 1),
('5', 'Blog', 'https://yourblog.com', datetime('now'), datetime('now'), 1);
END_SQL