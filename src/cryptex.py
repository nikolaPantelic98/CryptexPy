import base64
import hashlib
import os

import bcrypt
import cryptography
import mysql.connector
from getpass import getpass
from cryptography.fernet import Fernet


def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("CRYPTEX_DB_USER"),
            password=os.getenv("CRYPTEX_DB_PASSWORD")
        )

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cryptex_py")
        cursor.execute("USE cryptex_py")
        cursor.execute("CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS manager (id INT AUTO_INCREMENT PRIMARY KEY, website VARCHAR(255), email VARCHAR(255), password VARCHAR(255), user_id INT, FOREIGN KEY(user_id) REFERENCES user(id))")
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

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    hashed_key = base64.urlsafe_b64encode(hashlib.sha256(password.encode('utf-8')).digest()).decode('utf-8')
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("CRYPTEX_DB_USER"),
            password=os.getenv("CRYPTEX_DB_PASSWORD"),
            database="cryptex_py"
        )

        cursor = connection.cursor()
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, hashed_password))
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
            user=os.getenv("CRYPTEX_DB_USER"),
            password=os.getenv("CRYPTEX_DB_PASSWORD"),
            database="cryptex_py"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT password FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
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


def save(username, website, email, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("CRYPTEX_DB_USER"),
            password=os.getenv("CRYPTEX_DB_PASSWORD"),
            database="cryptex_py"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT id, password FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            user_id, hashed_account_password = result
            master_password = getpass("$ Enter master password: ")
            if not bcrypt.checkpw(master_password.encode('utf-8'), hashed_account_password.encode('utf-8')):
                print("[WARNING] Master password does not match account password")
                return
            hashed_key = base64.urlsafe_b64encode(hashlib.sha256(master_password.encode('utf-8')).digest())
            cipher_suite = Fernet(hashed_key)
            cipher_text = cipher_suite.encrypt(password.encode())
            cursor.execute("INSERT INTO manager (website, email, password, user_id) VALUES (%s, %s, %s, %s)", (website, email, cipher_text.decode('utf-8'), user_id))
            connection.commit()
            print("[SUCCESS] Data saved successfully")
        else:
            print("[WARNING] User not found")
    except mysql.connector.Error as error:
        print(f"[ERROR] Failed to save data in MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def show(username):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("CRYPTEX_DB_USER"),
            password=os.getenv("CRYPTEX_DB_PASSWORD"),
            database="cryptex_py"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            cursor.execute("SELECT website FROM manager WHERE user_id = %s", (user_id,))
            websites = cursor.fetchall()
            print("Websites:")
            for website in websites:
                print(website[0])
            website = input("$ Enter website: ")
            key = getpass("$ Enter key: ")
            hashed_key = base64.urlsafe_b64encode(hashlib.sha256(key.encode('utf-8')).digest())
            cursor.execute("SELECT email, password FROM manager WHERE user_id = %s AND website = %s", (user_id, website))
            result = cursor.fetchone()
            if result:
                email, password = result
                try:
                    cipher_suite = Fernet(hashed_key)
                    plain_text = cipher_suite.decrypt(password.encode()).decode('utf-8')
                    print(f"Email: {email}")
                    print(f"Password: {plain_text}")
                except cryptography.fernet.InvalidToken:
                    print("[ERROR] Invalid key")
            else:
                print("[WARNING] No data found for this website")
        else:
            print("[WARNING] User not found")
    except mysql.connector.Error as error:
        print(f"[ERROR] Failed to show data in MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


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
            while logged_in:
                type_key2 = input(f"~{username}>$ ")
                if type_key2 == "-quit":
                    raise KeyboardInterrupt
                elif type_key2 == "-logout":
                    logged_in = False
                    username = None
                    print("[SUCCESS] Logged out")
                    break
                elif type_key2 == "-save":
                    website = input("$ Enter website: ")
                    email = input("$ Enter email: ")
                    password = getpass("$ Enter password: ")
                    save(username, website, email, password)
                elif type_key2 == "-show":
                    show(username)
except KeyboardInterrupt:
    pass