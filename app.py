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

def add_client(name, level, age, gender):   # parameters are taken and used as values to insert a new client into the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (Name, Level, Age, Gender)
        VALUES (?, ?, ?, ?)
    """, (name, level, age, gender))
    conn.commit()
    conn.close()



# ========================= FLASK ROUTES ========================
@app.route('/add')
def add_page():
    return render_template('add.html')


@app.route('/')     # automatically executes this function when the program runs
def index():
    clients = get_all_clients()     # function that returns list of all users is passed as a parameter
    return render_template('index.html', clients=clients)

@app.route('/add_client', methods=['POST'])
def add_client_route():
    name = request.form['Name']     # extracts form values from the submitted form
    level = request.form['Level']
    age = int(request.form['Age'])
    gender = request.form['Gender']

    add_client(name, level, age, gender)    # passes values into the database insert function
    return redirect(url_for('index'))   #redirect back to main window once operation is complete

@app.route('/search_client', methods=['POST'])
def search_client():
    name_query = request.form['SearchName']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE Name LIKE ?", (f"%{name_query}%",))
    results = cursor.fetchall()
    conn.close()


    highlight_ids = [client[0] for client in results]     # Loop through each matching client and save their ID
    all_clients = get_all_clients()                        # Get all clients  

    reordered = sorted(all_clients, key=lambda c: c[0] not in highlight_ids)    # Reorder: matching clients first – key determines how the all_clients list is sorted
    return render_template('index.html', clients=reordered, highlight_ids=highlight_ids)


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

    # conn = sqlite3.connect(DB_PATH)
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM clients WHERE ClientID = x")
    # conn.commit()
    # conn.close()


    app.run(debug=True)

