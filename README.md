# ALX-Final-Project
# CipherGuard - Secure Password Manager

CipherGuard is a secure password manager built primarily in Python, designed to provide robust encryption and local storage for your sensitive passwords. It employs the Blowfish encryption algorithm to ensure the confidentiality of your data. This repository contains the source code and documentation for CipherGuard, developed by Tinashe Matanda.

## Features

- **Strong Encryption**: CipherGuard uses the Blowfish encryption algorithm to securely encrypt and protect your stored passwords.

- **Local Storage**: All your password data is stored locally on your system, ensuring you have full control over your sensitive information.

- **Web Interface**: Access your encrypted password database through a web interface powered by Flask, providing a user-friendly way to manage your passwords.

- **Desktop Application**: A desktop application is also available, allowing you to access your passwords locally without needing a web browser.

- **SQLite Database**: Passwords are stored in an SQLite database, a lightweight and reliable database system.

## Getting Started

### Prerequisites

- Python [Link](https://www.python.org/downloads/)
- Pip (Python Package Installer, usually included with Python)
- Virtualenv (recommended for isolated environment)
  ```bash
  pip install virtualenv
  pip install flask
  pip install Tkinter cryptography crypto
  ```

### Languages used
  Python
  Javascript
  CSS
  HTML
  Jinja
### Installation
  ```bash
  git clone https://github.com/tinashelorenzi/CipherGuard.git
  cd CipherGuard
  flask run
  ```
  Open your browser and visit https://localhost:5000

### Security Considerations
- The Blowfish encryption algorithm used in CipherGuard is designed to be secure, but it's important to stay informed about cryptography best practices and vulnerabilities.
- Make sure to keep your master password secure and do not share it with anyone.
- Regularly back up your encrypted password database to prevent data loss.

### Author
CipherGuard is developed by Tinashe Matanda. Contact: tinashelorenzi@protonmail.com

### License
This project is licensed under the MIT License.
