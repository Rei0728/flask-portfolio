-- データベース作成（必要な場合）
CREATE DATABASE comment_app;

-- comment_appに接続
\c comment_app

-- コメントテーブル作成
CREATE TABLE IF NOT EXISTS comments (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  comment TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);