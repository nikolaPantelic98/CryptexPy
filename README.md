# CryptexPy

Welcome to CryptexPy. This script will fully encode your .txt file.

## Features

- Several layers of protection.
- Ideal for storing passwords and sensitive information.

## Requirements

- python3
- pip3

## Installation

* Clone the repository to your local machine:

```
git clone https://github.com/nikolaPantelic98/CryptexPy.git
```

* Navigate to the directory:

```
cd CryptexPy
```

* Install requirements.txt file:

```
pip install -r requirements.txt
```

* Install mysql and set up credentials.

* Start the script:

```
python3 cryptex.py
```

## Additional information

- You will need mysql user and password to estabilish connection.
- Commands:
  - `-quit` - exit the script.
  - `-register` - register your account
  - `-login` - login  to your account
  - `-logout` - logout from your account
  - `-enter` - enter the account
  - `-read` - read and edit your .txt file in decrypted format.
- When you run `-read` for the first time, the key will be generated.
- You will be only able to see decrypted data with the correct key. If the key is lost, there is currently no option to recover the data.
