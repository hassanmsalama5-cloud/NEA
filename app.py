import sqlite3
from flask import Flask, render_template, request, redirect, url_for,session,abort
from datetime import date 
# from werkzeug.security import check_password_hash
app = Flask(__name__)
app.secret_key = "1932ADFV"
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
            session["customer_id"] = customer[0]
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
            "booked": not bool(seat["isavailable"])

        })
    seatslist= []
    for row in sorted(seats_by_row):
        seatslist.append(seats_by_row[row])

    if len(seats_by_row) == 0:
        error = "No seats available for this screening."
    
    return render_template("seats.html", seat_by_row=seatslist, screening_id=screening_id, film_name=film_name,error=error)
@app.route("/confirm_booking", methods=['POST'])
def confirm_booking():
    customer_id = session.get("customer_id")
    screening_id = request.form.get("screening_id", type=int)
    seat_ids = request.form.getlist("seat_ids")
    if customer_id is None:
        return redirect(url_for("signin"))
    if not screening_id or not seat_ids:
        abort(400,"select a screening and at least on seat")
    try:
        seat_ids = [int(seat_id) for seat_id in seat_ids]
    except ValueError:
        abort(400,"invalid seat selection")
    if len(seat_ids) != len(set(seat_ids)):
        abort(400,"duplicate seats selected.")
    total_price = len(seat_ids) * 10.00
    con = sqlite3.connect(DATABASE)
    con.execute("PRAGMA foreign_keys = ON")
    try:
        cur = con.cursor()
        cur.execute("BEGIN IMMEDIATE")
        cur.execute("""
            SELECT screeningID
            from Screenings
            where ScreeningID = ?
        """,(screening_id,))
        if cur.fetchone() is None:
            abort(400,"Invalid screening.")
        placeholders = ",".join("?" for _ in seat_ids)
        cur.execute(f"""
            SELECT SeatID
            FROM Seats
            WHERE ScreeningID=?
            AND isavailable = 1
            AND SeatID IN({placeholders})
        """,[screening_id] + seat_ids)

        available_ids = {row[0] for row in cur.fetchall()}

        if available_ids != set(seat_ids):
            abort(409,"One or more seats are no longer available.")
        cur.execute("""
            INSERT INTO Bookings
                (customerID,screeningID,bookingDate,numberOfTickets,TotalPrice)
            Values(?,?,?,?,?)
        """,(
            customer_id,
            screening_id,
            date.today().isoformat(),
            len(seat_ids),
            total_price,
        ))

        booking_id = cur.lastrowid
        for seat_id in seat_ids:
            cur.execute("""
                INSERT INTO BookingSeats(bookingID,seatID)
                VALUES(?,?)
            """,(booking_id,seat_id))
        cur.execute(f"""
                    UPDATE Seats 
                    set isavailable = 0 
                    WHERE ScreeningID=?
                    AND isavailable = 1
                    AND SeatID IN({placeholders})
                """,[screening_id] + seat_ids)
        if cur.rowcount != len(seat_ids):
            abort(409,"Seat availability changed.")
        con.commit()
        return render_template("confirmation.html",booking_id=booking_id)
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
    # def confirmation():

if __name__ == "__main__":
    app.run(debug=True)