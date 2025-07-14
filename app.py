from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# PostgreSQLに接続する設定
conn = psycopg2.connect(
    dbname="comment_app",
    user="kaidarei",     # あなたのユーザー名に置き換えてください
    password="",         # パスワードを設定している場合はここに
    host="localhost",
    port="5432"
)

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
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            comment = data.get('comment')
            cur.execute(
                "INSERT INTO comments (username, comment) VALUES (%s, %s)",
                (username, comment)
            )
            conn.commit()
            return jsonify({"message": "コメントを保存しました"}), 201

        else:  # GET
            cur.execute("SELECT * FROM comments ORDER BY created_at DESC")
            comments = cur.fetchall()
            return jsonify(comments)

if __name__ == '__main__':
    app.run(debug=True)