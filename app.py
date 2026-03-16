from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

@app.route("/signup", methods=["GET", "POST"])
def signup():
   if request.method == "POST":
      con = sqlite3.connect("database.db")
      cur = con.cursor()
      cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (request.form['username'], request.form['password']))
      con.commit()
      con.close()
      return "signup successful"
   return render_template('signup.html')

@app.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (request.form['username'], request.form['password']))
    result = cur.fetchone()
    if result:
            return "access granted"
    else:
       return "access denied"
   return render_template('index.html')
