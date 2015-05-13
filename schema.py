import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sample.db")

with sqlite3.connect(db_path) as connection:
    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS userdata(
        username TEXT, email TEXT)""")
    c.execute('INSERT INTO userdata values("admin", "admin@admin.com")')
    c.execute('INSERT INTO userdata values("mitul", "mitul@gmail.com")')
