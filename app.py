from flask import Flask
import os
import psycopg2
import redis

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "week4db")
DB_USER = os.getenv("DB_USER", "week4user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "week4pass")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")


def get_database_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def initialize_database():
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL
        )
    """)

    cursor.execute(
        "SELECT COUNT(*) FROM messages"
    )

    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "INSERT INTO messages (message) VALUES (%s)",
            ("Hello from PostgreSQL!",)
        )

    connection.commit()
    cursor.close()
    connection.close()


@app.route("/")
def home():
    try:
        initialize_database()

        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT message FROM messages ORDER BY id DESC LIMIT 1"
        )

        message = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=6379,
            decode_responses=True
        )

        redis_client.set("week4_status", "Redis is connected!")
        redis_status = redis_client.get("week4_status")

        return f"""
        <html>
            <head>
                <title>Week 4 Docker Compose</title>
            </head>
            <body>
                <h1>Week 4 — Multi-Service Docker Compose Stack 🚀</h1>

                <h2>Service Status</h2>

                <p>✅ Flask Web Service: Running</p>
                <p>✅ PostgreSQL: Connected</p>
                <p>✅ Redis: {redis_status}</p>

                <h2>Database Message</h2>
                <p>{message}</p>
            </body>
        </html>
        """

    except Exception as error:
        return f"""
        <h1>Week 4 Docker Compose</h1>
        <p>❌ Service connection error</p>
        <p>{error}</p>
        """, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)