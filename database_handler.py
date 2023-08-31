import sqlite3
from Crypto.Cipher import Blowfish
import os
from cipherguard import encrypt_pass

def create_tables():
  """Creates the database tables for the database.db file."""
  conn = sqlite3.connect("vault/database.db")
  cursor = conn.cursor()
  
  cursor.execute("""CREATE TABLE IF NOT EXISTS master (
    name TEXT NOT NULL,
    password TEXT NOT NULL
  )""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS passcodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    category TEXT NOT NULL,
    password TEXT NOT NULL
  )""")

  conn.commit()
  conn.close()

def encrypt_db(file, out, password):
    # Read the contents of the file
    with open(file, 'rb') as f:
        plaintext = f.read()

    # Initialize the Blowfish cipher with the password
    cipher = Blowfish.new(password.encode(), Blowfish.MODE_CBC)

    # Add padding to the plaintext to make its length a multiple of 8 bytes
    block_size = 8
    padded_plaintext = plaintext + (block_size - len(plaintext) % block_size) * b'\0'

    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)

    # Write the encrypted data to the output file
    with open(out, 'wb') as f:
        f.write(ciphertext)

    # Delete the original file
    os.remove(file)

def decrypt_db(file, out, password):
    # Read the encrypted contents of the file
    with open(file, 'rb') as f:
        ciphertext = f.read()

    # Initialize the Blowfish cipher with the password
    cipher = Blowfish.new(password.encode(), Blowfish.MODE_CBC)

    # Decrypt the ciphertext
    decrypted_padded = cipher.decrypt(ciphertext)

    # Remove padding to get the original plaintext
    plaintext = decrypted_padded.rstrip(b'\0')

    # Write the decrypted data to the output file
    with open(out, 'wb') as f:
        f.write(plaintext)

    # Delete the encrypted file
    os.remove(file)
    
def inserter_to_db(table_name, name, password_base64):
    db_file = "vault/database.db"
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Insert data into the table
        query = f"INSERT INTO {table_name} (name, password) VALUES (?, ?)"
        cursor.execute(query, (name, password_base64))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        print("Data inserted successfully.")

    except sqlite3.Error as e:
        print("Error:", e)

def authenticate(password):
    # Encrypt the provided password (you mentioned this function is already available)
    encrypted_pass = encrypt_pass(password, "b9b93345e2f29458c62a5c822259d83852683c1c50715a01f3bf07499d37f777")

    # Connect to the SQLite database
    db_file = "vault/database.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Retrieve the encrypted password from the master table
        query = "SELECT password FROM master WHERE name = ?"
        cursor.execute(query, ("name",))  # Assuming you want to retrieve for a specific entry named "name"
        fetched_data = cursor.fetchone()

        if fetched_data:
            password_base64 = fetched_data[0]

            # Compare encrypted_pass with password_base64
            if encrypted_pass == password_base64:
                return True
            else:
                return False
        else:
            return False

    except sqlite3.Error as e:
        print("Error:", e)
        return False

    finally:
        # Close the connection
        conn.close()
        
def fetch_data(table_name):
    connection = sqlite3.connect("vault/database.db")
    cursor = connection.cursor()

    query = f"SELECT name, password_base64 FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()

    connection.close()
    return data

def get_table_data(table_name):
    conn = sqlite3.connect('vault/database.db')  # Change the path to your database file
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))

    conn.close()
    return data