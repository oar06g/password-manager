# Password Manager

## Description
This is a simple and secure password manager application built using **PyQt5** and **SQLite**. It allows users to store and manage passwords for different websites securely by encrypting sensitive information using the **AES encryption algorithm**.

The main password for logging into the application is **`haIrySECKw`**. 

## Features
- **Secure Password Storage**: Encrypts passwords before storing them in the database.
- **User Authentication**: A login screen that requires a master password to access the password manager.
- **Add, Update, Delete Entries**: Users can add, update, or delete their stored credentials.
- **Encryption**: All stored data (sitename, username, password, email) is encrypted with a secret key for enhanced security.
- **Database**: Uses SQLite for storing user data and passwords.

## How to Install

1. **Clone the repository**:
   ```bash
   git clone https://github.com/oar06g/password-manager.git
   ```
2. **Install required libraries**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
    run.cmd
   ```