import sqlite3
from flask import Flask, render_template, request, redirect, url_for
# from werkzeug.security import check_password_hash
app = Flask(__name__)
DATABASE = "cinema.db"
@app.route("/")
def home():
    return redirect(url_for("signin"))
@app.route("/signin", methods=["GET", "POST"])
def signin():
   error = None
   success = None
   if request.method == "POST":
      username = request.form.get("username","").strip()
      password = request.form.get("password","").strip()
      if not username or not password:
          error = "Please complete all fields."
      else:
         con = sqlite3.connect(DATABASE)
         cur = con.cursor()
         cur.execute(
    "SELECT * FROM Customers WHERE username=? AND password=?",
    (username, password)
         )
         customer = cur.fetchone()
         con.close()
      if customer:
            success = "Account logged in successfully."
            return redirect(url_for("genre"))
      else:
       error = "Invalid username or password."
   return render_template("signin.html",error=error, success=success)

@app.route("/signup", methods=["GET", "POST"])
def signup():
      error = None
      success = None
      if request.method == "POST":
         username = request.form.get("username","").strip()
         password = request.form.get("password","").strip()
         confirm_password = request.form.get("confirm_password","").strip()
         if not username or not password or not confirm_password:
            error = "Please complete all fields."
         elif password != confirm_password:
               error = "Passwords do not match."
         else:
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            cur.execute("SELECT * FROM Customers WHERE username = ?",(username,))
            existing_customer = cur.fetchone()
            if existing_customer:
                error = "Username already exists."
            else:
                cur.execute("INSERT INTO Customers (username, password) VALUES (?, ?)", (username, password))
                con.commit()
                success = "Account created successfully."
                con.close()
                return redirect(url_for("signin"))
      return render_template('signup.html', error=error, success=success)
@app.route("/genre")
def genre():
    
    return render_template("genre.html")
@app.route("/films/<genre>")
def films(genre):
    valid_genres=["comedy", "action", "horror", "sci-fi", "thriller"]
    if genre not in valid_genres:
        return "invalid genre selected",400
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Films WHERE genre = ?", (genre.title(),))
    films = cur.fetchall()
    con.close()
    return render_template("films.html", genre=genre,films=films)
if __name__ == "__main__":
    app.run(debug=True)