import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "myappdb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASSWORD", "postgrespassword")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({
            "status": "healthy",
            "message": "Connected to PostgreSQL database successfully!",
            "db_version": db_version[0]
        })
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500

@app.route('/healthz')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/readiness')
def readiness():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "ready"}), 200
    except Exception:
        return jsonify({"status": "not ready"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
