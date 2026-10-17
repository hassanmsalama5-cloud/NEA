import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
app = Flask(__name__)
DATABASE = "cinema.db"
def signin():
   error = None
   if request.method == "POST":
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM Customers WHERE username=? AND password=?", (request.form['username'], request.form['password']))
    result = cur.fetchone()
    if result:
            return "access granted"
    else:
       return "access denied"
   return render_template('signin.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
   if request.method == "POST":
      con = sqlite3.connect(DATABASE)
      cur = con.cursor()
      cur.execute("INSERT INTO Customers (username, password) VALUES (?, ?)", (request.form['username'], request.form['password']))
      con.commit()
      con.close()
      return "signup successful"
   return render_template('signup.html')

