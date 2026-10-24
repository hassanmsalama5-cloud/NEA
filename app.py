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
         cur.execute("SELECT * FROM Customers WHERE username=? AND password=?", (username, password))
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
    error = None
    valid_genres=["comedy", "action", "horror", "sci-fi", "thriller"]
    if genre not in valid_genres:
        error = "Invalid genre selected"
        return redirect(url_for("genre"))
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Films WHERE genre = ?", (genre.title(),))
    films = cur.fetchall()
    con.close()
    return render_template("films.html", genre=genre,films=films,error=error)
@app.route('/select_screening/<film_id>/<film_name>')
def select_screening(film_id,film_name):
    error = None 
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute("""
        SELECT ScreeningID, ScreeningDate, ScreeningTime, ScreenNumber
        FROM Screenings
        WHERE FilmID = ?
    """, (film_id,))
    screenings = cursor.fetchall()
    if len(screenings) == 0:
        error = "No screenings available for this film."
    con.close()
    return render_template("screenings.html", screenings=screenings, film_name=film_name, error=error)
@app.route('/select_seats/<screening_id>/<film_name>', methods=['GET', 'POST'])
def select_seats(screening_id, film_name):
    error = None
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute("""
        SELECT SeatID, SeatNumber, IsAvailable
        FROM Seats
        WHERE ScreeningID = ?
        ORDER BY SeatNumber
    """, (screening_id,))
    rows = cursor.fetchall()
    con.close()
    seats_by_row = {}
    for seat in rows:
        seat_name = seat["Seatnumber"]
        row_label = seat_name[0]
        seats_by_row.setdefault(row_label, []).append({
            "id": seat["SeatID"],
             "row": row_label,
            "number": seat_name[1:],
            "booked": not bool(seat["IsAvailable"])

        })
    seatslist= []
    for row in sorted(seats_by_row):
        seatslist.append(seats_by_row[row])

    if len(seats_by_row) == 0:
        error = "No seats available for this screening."
    
    return render_template("seats.html", seat_by_row=seatslist, screening_id=screening_id, film_name=film_name,error=error)
if __name__ == "__main__":
    app.run(debug=True)