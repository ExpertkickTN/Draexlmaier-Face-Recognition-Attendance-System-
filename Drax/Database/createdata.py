import sqlite3

connection = sqlite3.connect('AccountSystem.db')
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS AccountDB(ID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, "
            "Email TEXT, Password TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS PASSFORGOT(ID INTEGER PRIMARY KEY, Email TEXT, NewPassword TEXT)")
connection.commit()
connection.close()
