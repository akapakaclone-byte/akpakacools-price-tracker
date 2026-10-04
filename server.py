from flask import Flask, jsonify, send_from_directory
import sqlite3

app = Flask(__name__, static_folder=".")


def get_prices(item):
    connection = sqlite3.connect("prices.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT price, timestamp
        FROM prices
        WHERE LOWER(item) = LOWER(?)
        ORDER BY timestamp ASC
        """,
        (item,)
    )

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "price": row[0],
            "timestamp": row[1]
        }
        for row in rows
    ]


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/prices/<item>")
def prices(item):
    return jsonify(get_prices(item))


if __name__ == "__main__":
    import os
    import subprocess

    subprocess.Popen(["python", "bot.py"])

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )