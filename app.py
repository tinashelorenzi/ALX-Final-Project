from flask import Flask, render_template, request, redirect, session
import os
import database_handler
from cipherguard import encrypt_pass

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set your secret key here

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
  if session.get('authenticated'):
    return render_template("dashboard.html")
  else:
    return redirect("/")

@app.route("/logout")
def logout():
  session.clear()
  return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)
