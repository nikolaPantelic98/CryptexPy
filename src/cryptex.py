import os
import re
import tempfile

import bcrypt
import mysql.connector
from getpass import getpass
from cryptography.fernet import Fernet


def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=db_username,
            password=db_password
        )

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cryptex_py")
        cursor.execute("USE cryptex_py")
        cursor.execute("CREATE TABLE IF NOT EXISTS user (username VARCHAR(255), password VARCHAR(255))")
        print("[SUCCESS] Connection established")
    except mysql.connector.Error as error:
        print(f"[ERROR] Failed to create database in MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def register(username, password):
    password_confirm = getpass("Confirm password: ")
    if password != password_confirm:
        print("[WARNING] Passwords do not match. Please try again.")
        return

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=db_username,
            password=db_password,
            database="cryptex_py"
        )

        cursor = connection.cursor()
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, hashed.decode('utf-8')))
        connection.commit()
        print("[SUCCESS] User registered successfully")
    except mysql.connector.Error as error:
        print(f"[ERROR] Failed to register user in MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def login(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=db_username,
            password=db_password,
            database="cryptex_py"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT password FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            print("[SUCCESS] Login completed")
            print(f"[SUCCESS] Welcome {username}!")
            return True
        else:
            print("[WARNING] Login error")
            return False
    except mysql.connector.Error as error:
        print(f"[ERROR] Failed to login user in MySQL: {error}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def encrypt_content(content, key):
    cipher_suite = Fernet(key)
    encrypted_content = cipher_suite.encrypt(content.encode('utf-8'))
    return encrypted_content


def decrypt_content(encrypted_content, key):
    cipher_suite = Fernet(key)
    decrypted_content = cipher_suite.decrypt(encrypted_content).decode('utf-8')
    return decrypted_content


def is_base64(s):
    return re.fullmatch(r'^[A-Za-z0-9+/]+={0,2}$', s) is not None


def read_or_create_file(username):
    os.makedirs('../.src', exist_ok=True)
    file_path = f'../.src/{username}.txt'
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        with open(file_path, 'wb') as file:
            encrypted_content = cipher_suite.encrypt(b'Initial content')
            file.write(encrypted_content)
            print(f"[SUCCESS] File {username}.txt created")
        print(f"Your encryption key is: {key.decode()}")
        print("You will never see this key again.")
    else:
        key_input = getpass("Encryption key: ")
        try:
            key = key_input.encode()
            cipher_suite = Fernet(key)
        except ValueError:
            print("[WARNING] Incorrect key.")
            return
        with open(file_path, 'rb') as file:
            encrypted_content = file.read()
            try:
                content = cipher_suite.decrypt(encrypted_content).decode('utf-8')
                with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tf:
                    tf.write(content.encode())
                    temp_file_name = tf.name
                os.system(f"nano {temp_file_name}")
                with open(temp_file_name, 'r') as tf:
                    updated_content = tf.read()
                os.remove(temp_file_name)
                encrypted_updated_content = cipher_suite.encrypt(updated_content.encode())
                with open(file_path, 'wb') as file:
                    file.write(encrypted_updated_content)
            except:
                print("[WARNING] Incorrect key.")


def reset_key(username):
    file_path = f'../.src/{username}.txt'
    old_key_input = getpass("Encryption key: ")
    try:
        old_key = old_key_input.encode()
        old_cipher_suite = Fernet(old_key)
    except ValueError:
        print("[WARNING] Incorrect encryption key.")
        return
    with open(file_path, 'rb') as file:
        encrypted_content = file.read()
        try:
            content = old_cipher_suite.decrypt(encrypted_content).decode('utf-8')
            new_key = Fernet.generate_key()
            new_cipher_suite = Fernet(new_key)
            encrypted_updated_content = new_cipher_suite.encrypt(content.encode())
            with open(file_path, 'wb') as file:
                file.write(encrypted_updated_content)
            print(f"[SUCCESS] Encryption key reset")
            print(f"Your new encryption key is: {new_key.decode()}")
            print("You will never see this key again.")
        except:
            print("[WARNING] Incorrect encryption key.")


print("Data Source")
db_username = input("User: ")
db_password = getpass("Password: ")
create_database()

try:
    logged_in = False
    username = None
    while True:
        type_key = input(">$ ")
        if type_key == "-quit":
            raise KeyboardInterrupt
        elif type_key == "-register":
            username = input("$ Enter username: ")
            password = getpass("$ Enter password: ")
            register(username, password)
        elif type_key == "-login":
            username = input("$ Enter username: ")
            password = getpass("$ Enter password: ")
            logged_in = login(username, password)
        elif type_key == "-logout" and logged_in:
            logged_in = False
            username = None
            print("[SUCCESS] Logged out")
        elif type_key == "-enter" and logged_in:
            while True:
                type_key2 = input(f"~{username}>$ ")
                if type_key2 == "-quit":
                    raise KeyboardInterrupt
                elif type_key2 == "-logout":
                    logged_in = False
                    username = None
                    print("[SUCCESS] Logged out")
                    break
                elif type_key2 == "-read":
                    read_or_create_file(username)
                elif type_key2 == "-reset":
                    reset_key(username)
except KeyboardInterrupt:
    pass