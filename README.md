# 🛡️ CryptexPy: Your Personal Password Manager 📝

Welcome to CryptexPy, a fortress for your passwords. Imagine having a personal password manager where you can store all your sensitive information and no one but you holds the key. That's what CryptexPy is all about!

## 🌟 Features

- **Fort Knox for your files**: With several layers of protection, your email and passwords are safe and secure.
- **Ideal for secrets**: Perfect for storing passwords.

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

4. Install MySQL and set up your credentials.

## 🎮 How to Use

* Start the script with:

```
cd src
python3 cryptex.py
```

## 🔍 Additional information

- You will need mysql user and password to estabilish connection.
- Commands:
  - `-quit` - exit the script.
  - `-register` - register your account
  - `-login` - login  to your account
  - `-logout` - logout from your account
  - `-enter` - enter your account
  - `-read` - read and edit your .txt file in decrypted format.
  - `-reset` - reset your encrypted key and get a new one.
- When you run `-read` for the first time, the key will be generated.
- You will be only able to see decrypted data with the correct key. If the key is lost, there is currently no option to recover the data.
- You can reset key with the `-reset` command which require old encrypted key.
