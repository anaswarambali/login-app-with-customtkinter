import sqlite3 as sql
import bcrypt
from tkinter import messagebox


def create():
    try:
        con = sql.connect("login.db")
        con.execute('''CREATE TABLE IF NOT EXISTS login (
                            username char(200) NOT NULL,
                            password char(200) NOT NULL,
                            pin int(4) NOT NULL
                            );''')

        user = bcrypt.hashpw(b'admin', bcrypt.gensalt())
        salted = salting('root').encode('UTF-8')
        pssd = bcrypt.hashpw(salted, bcrypt.gensalt())

        con.execute("INSERT INTO login (username, password, pin) VALUES(?, ?, 1234);", (user, pssd))
        con.commit()
        con.close()
    except sql.IntegrityError:
        print("tables present")
    except Exception:
        print("Errors are the key to success")
    else:
        print("Success")


def check_password(username, password):
    con = sql.connect('login.db')
    con = con.cursor()
    con.execute("select * from login")
    results = con.fetchall()
    count = len(results)
    password = salting(password)

    if count > 0:
        for i in results:
            if bcrypt.checkpw(username.encode('utf-8'), i[0]):
                if bcrypt.checkpw(password.encode('utf-8'), i[1]):
                    return 1
                else:
                    messagebox.showerror("Error", "Wrong password")
                break
        else:
            messagebox.askyesno("User Doesn't Exist", 'Do you want to create')
    else:
        messagebox.showinfo("message", "Wrong username or password")

    return 0


def salting(password):
    salted = ''
    salt = ''
    for i in password:
        if i == 'z':
            salt += 'a'
        elif i == 'Z':
            salt += 'A'
        else:
            salt += chr(ord(i) + 1)

    for i in range(len(password)):
        salted += password[i]
        salted += salt[i]
    return salted


def insert():
    pass


if __name__ == '__main__':

    create()
    salting('root')
    check_password('admin', 'root')
