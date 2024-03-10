import os
import bcrypt
import mysql.connector
from getpass import getpass


def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv('DATASOURCE_USERNAME'),
            password=os.getenv('DATASOURCE_PASSWORD')
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
            user=os.getenv('DATASOURCE_USERNAME'),
            password=os.getenv('DATASOURCE_PASSWORD'),
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
            user=os.getenv('DATASOURCE_USERNAME'),
            password=os.getenv('DATASOURCE_PASSWORD'),
            database="cryptex_py"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT password FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            print("[SUCCESS] Login completed")
            print(f"[SUCCESS] Welcome {username}!")
        else:
            print("[WARNING] Login error")
    except mysql.connector.Error as error:
        print(f"[ERROR] Failed to login user in MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


try:
    while True:
        type_key = input(">>")
        if type_key == "-quit":
            raise KeyboardInterrupt
        elif type_key == "-connect":
            create_database()
            while True:
                type_key2 = input(">>>")
                if type_key2 == "-quit":
                    raise KeyboardInterrupt
                elif type_key2 == "-back":
                    break
                elif type_key2 == "-register":
                    username = input("Enter username: ")
                    password = getpass("Enter password: ")
                    register(username, password)
                elif type_key2 == "-login":
                    username = input("Enter username: ")
                    password = getpass("Enter password: ")
                    login(username, password)
                else:
                    print(type_key2)
        else:
            print(type_key)
except KeyboardInterrupt:
    pass