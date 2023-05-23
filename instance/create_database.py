import sqlite3

database = sqlite3.connect("blog-database.db")
cursor = database.cursor()
cursor.execute("CREATE TABLE blogs (id INTEGER PRIMARY KEY, userID INTEGER, title VARCHAR(250), body VARCHAR(1000) )")