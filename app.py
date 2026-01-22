from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = "clients.db"

# ========================= DATABASE FUNCTIONS ========================= #

def create_clients_table():     # Creates table 
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Level TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Gender TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_all_clients():      # uses SELECT query and returns all clients as a list 
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    conn.close()
    return clients



# ========================= FLASK ROUTES ========================
@app.route('/add')
def add_page():
    return render_template('add.html')


@app.route('/')     # automatically executes this function when the program runs
def index():
    clients = get_all_clients()     # function that returns list of all users is passed as a parameter
    return render_template('index.html', clients=clients)


# ========================= Run App ========================= #

# import os

if __name__ == '__main__':
    create_clients_table()

    # if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    #     add_client("Alice", "Beginner", 25, "Female")
    #     add_client("Ben", "Intermediate", 32, "Male")
    #     add_client("Chloe", "Advanced", 29, "Female")
    #     add_client("David", "Beginner", 40, "Male")
    #     add_client("Ella", "Intermediate", 22, "Female")

    app.run(debug=True)

