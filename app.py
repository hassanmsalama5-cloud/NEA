import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
app = Flask(__name__)
DATABASE = "cinema.db"
@app.route("/signin", methods=["GET", "POST"])
def signin():
   error = None
   if request.method == "POST":
      username = request.form.get("username","").strip()
      password = request.form.get("password","").strip()
   
      if not username or not password:
          error = "Please complete all fields."
      else:
         con = sqlite3.connect(DATABASE)
         cur = con.cursor()
         cur.execute(
      """,
         cur.execute(
    "SELECT * FROM Customers WHERE username=? AND password=?",
    (username, password)
      """,
      )
      customer = cur.fetchone()
      con.close()
      if customer:
            return "access granted"
      else:
       error = "Invalid username or password."
   return render_template("signin.html",error=error)

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

