import os

import mysql.connector


def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv('DATASOURCE_USERNAME'),
            password=os.getenv('DATASOURCE_PASSWORD')
        )

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cryptex_py")
        print("Database created successfully")
    except mysql.connector.Error as error:
        print(f"Failed to create database in MySQL: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


try:
    while True:
        type_key = input(">>")
        if type_key == "-q":
            raise KeyboardInterrupt
        elif type_key == "-r":
            while True:
                type_key2 = input(">>>")
                if type_key2 == "-q":
                    raise KeyboardInterrupt
                elif type_key2 == "-b":
                    break
                elif type_key2 == "-cd":
                    create_database()
                else:
                    print(type_key2)
        else:
            print(type_key)
except KeyboardInterrupt:
    pass