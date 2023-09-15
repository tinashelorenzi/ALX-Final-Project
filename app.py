from flask import Flask, render_template, request, redirect, session, jsonify
import os, sqlite3
import database_handler
from cipherguard import encrypt_pass,decrypt_pass
from cs50 import SQL


app = Flask(__name__)
app.secret_key = 'William Shakespear'  # Set your secret key here

@app.route("/")
def index():
    if not os.path.exists("vault/database.db"):
        return redirect("/create")
    else:
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        password = request.form["password"]

        if database_handler.authenticate(password):
            session['authenticated'] = True
            return redirect("/dashboard")
        else:
            return "Login failed"

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match"

        # Encrypt the password using the cipherguard module
        encrypted_pass = encrypt_pass(password, "b9b93345e2f29458c62a5c822259d83852683c1c50715a01f3bf07499d37f777")

        # Create the database file and encrypt it with the password
        with open("vault/database.db", "wb") as f:
            database_handler.create_tables()
            database_handler.inserter_to_db("master", "name", encrypted_pass)

        return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    category = request.args.get("category", "master")
    db = SQL("sqlite:///vault/database.db")
    if session.get('authenticated'):
        if not session.get('started'):
            category = "master"
            session['started'] = True
            
        passwords = db.execute("SELECT * FROM passcodes WHERE category = ?", (category,))
        return render_template("dashboard.html", passwords=passwords, category=category)
    else:
        return redirect("/")

@app.route("/get_data")
def get_data():
    if session.get('authenticated'):
        category = request.args.get("category")
        data = database_handler.get_table_data(category)  # Modify this to fetch data from your database
        return jsonify(data)
    else:
        return jsonify([])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/append", methods=["POST","GET"])
def append():
    if session.get('authenticated'):
        if request.method == 'GET':
            return render_template('create_pass.html')
        if request.method == 'POST':
            name = request.form['name']
            url = request.form['url']
            category = request.form['category']
            password = encrypt_pass(request.form['password'],"66896d5b0ab9a5e32767332d974a0c6f03f25bba01d77c0f6806f75214032c804177e4d4f2e745632ca67d51b42fbc9f75a4ffb599d81fbd6c54d969371de34c")

            # Connect to the SQLite database
            conn = sqlite3.connect('vault/database.db')
            cursor = conn.cursor()

            # Insert data into the 'passcodes' table
            query = "INSERT INTO passcodes (name, url, category, password) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (name, url, category, password))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Redirect to a success page or back to the form
            return redirect(('/append'))  # Change 'success_page' to the actual route
    else:
        return redirect("/")
    
@app.route('/delete_password', methods=['POST'])
def delete_password():
    if request.method == 'POST':
        password_id = request.form['password_id']

        # Connect to the SQLite database
        conn = sqlite3.connect('vault/database.db')
        cursor = conn.cursor()

        # Delete the password by its ID
        query = "DELETE FROM passcodes WHERE id = ?"
        cursor.execute(query, (password_id,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Redirect back to the dashboard
        return redirect('/dashboard')
@app.route('/decrypt_password', methods=['POST'])
def decrypt():
    password = request.form['password']
    dec = decrypt_pass(password,"66896d5b0ab9a5e32767332d974a0c6f03f25bba01d77c0f6806f75214032c804177e4d4f2e745632ca67d51b42fbc9f75a4ffb599d81fbd6c54d969371de34c")
    return(dec)

if __name__ == "__main__":
    app.run(debug=True, port=4444)
