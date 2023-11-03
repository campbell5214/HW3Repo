from flask import Flask, render_template, jsonify
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Database connection
db_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="ident",
    host="127.0.0.1",
    port="5433"
)


@app.route('/api/update_basket_a')
def update_basket_a():
    # Insert a new row into basket_a
    try:
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry')")
        db_conn.commit()
        return "Success!"
    except Exception as e:
        db_conn.rollback()
        return str(e)
    finally:
        cursor.close

@app.route('/api/unique')
def unique_fruits():
    try:
        cursor = db_conn.cursor()
        # Fetch unique fruits from basket_a and basket_b
        cursor.execute("SELECT DISTINCT fruit_a FROM basket_a")
        unique_fruits_a = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT fruit_b FROM basket_b")
        unique_fruits_b = [row[0] for row in cursor.fetchall()]

        cursor.close()

        return render_template('unique.html', fruits_a=unique_fruits_a, fruits_b=unique_fruits_b)
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
