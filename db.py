import mysql.connector

def koneksi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bengkelKu"
    )
