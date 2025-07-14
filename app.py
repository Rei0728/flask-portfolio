from flask import Flask, request, jsonify, render_template
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL環境変数が設定されていません")
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/skill')
def skill():
    return render_template('skill.html')

@app.route('/comment')
def comment():
    return render_template('comment.html')

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        comment = data.get('comment')
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO comments (username, comment) VALUES (%s, %s)",
                    (username, comment)
                )
                conn.commit()
        return jsonify({"message": "コメントを保存しました"}), 201

    else:  # GET
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM comments ORDER BY created_at DESC")
                comments = cur.fetchall()
        return jsonify(comments)

if __name__ == '__main__':
    app.run(debug=True)