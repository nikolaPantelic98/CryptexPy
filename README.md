# 🛡️ CryptexPy: Your Personal Password Manager 📝

Welcome to CryptexPy, a fortress for your digital secrets. In an era where data breaches are common, CryptexPy stands as a beacon of security, offering a personal password manager where you can safely store your sensitive information. Only you hold the key to your digital vault, ensuring that your passwords and secrets remain yours alone.

## 🌟 Features

- **Unbreakable Security**: Leveraging state-of-the-art encryption algorithms, CryptexPy ensures that your data is stored in an impenetrable vault.
- **User-Friendly Interface**: Designed with simplicity in mind, allowing you to easily manage your passwords without any hassle.
- **Secure Sharing**: Safely share your passwords with trusted contacts without ever exposing your data in plaintext.
- **Cross-Platform Compatibility**: CryptexPy can be run on any system that supports Python, making it universally accessible.

## 📚 Requirements

- Python 3: The power behind our script.
- pip3: For installing all the necessary tools.
- MySQL: Our choice of database for storing user credentials.

## 🚀 Getting Started

1. Clone the repository to your local machine:

```
git clone https://github.com/nikolaPantelic98/CryptexPy.git
```

2. Navigate to the directory:

```
cd CryptexPy
```

3. Install the necessary libraries:

```
pip install -r requirements.txt
```

4. Install MySQL and set up your credentials:

- To install MySQL you can visit [this link](https://www.simplilearn.com/tutorials/mysql-tutorial/mysql-workbench-installation).

5. Set up environment variables for MySQL:

- For Linux/Mac:

```
echo 'export CRYPTEX_DB_USER="your_username"' >> ~/.bashrc
```
```
echo 'export CRYPTEX_DB_PASSWORD="your_password"' >> ~/.bashrc
```
```
source ~/.bashrc
```

- For Windows:
```
setx CRYPTEX_DB_USER "your_username"
```
```
setx CRYPTEX_DB_PASSWORD "your_password"
```

* Replace `your_username` and `your_password` with real credentials.
* It is necessary to close and reopen cmd for variables to be available on Windows.

## 🎮 How to Use

* Navigate to the root CryptexPy directory and start the script with:

```
cd src && python3 cryptex.py
```
Follow the prompts to register, login, and manage your passwords.

## 🔒 Security Highlights

**CryptexPy uses a combination of bcrypt for password hashing and Fernet symmetric encryption to secure your data. This dual-layer security ensures that even if unauthorized access to the database is obtained, deciphering your credentials without the unique key is virtually impossible.**

## 🔍 Additional information

- You will need mysql user and password to estabilish connection.
- Commands:
  - `--quit` - Exit the script.
  - `--register` - Register a new account.
  - `--login` - Login to your account.
  - `--logout` - Logout from your account.
  - `--save` - Securely save a new password.
  - `--edit` - Edit data (website, email, password).
  - `--show` - Retrieve and display saved passwords securely.
  - `--help` - Show all necessary information.

- It is possible to execute execution shortcuts in a terminal with one argument - website - in the following way:
 
1. You need to set an alias to execute the script in an easy way:

```
echo 'alias cryptex='\''cd /path_to_cryptex/CryptexPy/src && python3 cryptex.py'\''' >> ~/.bashrc

```

Replace `path_to_cryptex` with the real path on your machine.

2. You can set up terminal auto-complete logic:

```
echo 'source /path_to_cryptex/CryptexPy/cryptex_autocomplete.sh' >> ~/.bashrc
```

Replace `path_to_cryptex` with the real path on your machine.

3. Save edits:

```
source ~/.bashrc
```

4. Simply write `cryptex` in the terminal followed by only one argument - `website`. Example:

```
cryptex reddit
```

5. After that, you need to enter the `username` and `master password` and the terminal will copy the password to the clipboard.


**Your data's security is our top priority, and CryptexPy is continually updated to implement the latest security practices and encryption technologies.**
