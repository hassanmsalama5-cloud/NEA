import sqlite3
from flask import Flask, render_template, request, redirect, url_for,session,abort
from datetime import date 
# from werkzeug.security import check_password_hash
app = Flask(__name__)
app.secret_key = "1932ADFV"
DATABASE = "cinema.db"
#CUSTOMER
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
    cur.execute("SELECT * FROM Films WHERE genre = ? AND IsActive = 1", (genre.title(),))
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
        abort(400,"select a screening and at least one seat")
    try:
        seat_ids = [int(seat_id) for seat_id in seat_ids]
    except ValueError:
        abort(400,"invalid seat selection")
    if len(seat_ids) != len(set(seat_ids)):
        abort(400,"duplicate seats selected.")
    total_price = len(seat_ids) * 10.99
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
                (customerID,ScreeningID,bookingDate,numberOfTickets,TotalPrice)
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
        return redirect(url_for("confirmation",booking_id=booking_id))
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

@app.route("/confirmation/<int:booking_id>")
def confirmation(booking_id):
    con = sqlite3.connect(DATABASE)
    con.row_factory= sqlite3.Row

    try:
        cur = con.cursor()
        cur.execute("""
            SELECT B.bookingID,B.bookingDate,
                   B.numberOfTickets,B.totalPrice,
                   S.ScreeningDate,S.ScreeningTime,
                   S.ScreenNumber,F.title
            From bookings B
            Join Screenings S
                ON B.ScreeningID = S.ScreeningID
            Join Films f 
                ON S.filmID = F.filmID
            WHERE B.bookingID=?
            AND B.customerID =?
    """,(booking_id,session.get("customer_id")))
        
        booking = cur.fetchone()

        if booking is None:
            abort(404)

        cur.execute("""
            SELECT seats.seatNumber
            FROM BookingSeats
            Join seats ON  BookingSeats.seatID = seats.seatID
            WHERE BookingSeats.bookingID = ?
            ORDER BY seats.seatNumber
        """,(booking_id,))

        seats = [row["seatNumber"]for row in cur.fetchall()]

        return render_template("confirmation.html",booking=booking,seats=seats)
    finally:
        con.close()
#ADMINISTRATOR SIDE 
@app.route("/admin_signin",methods=["POST","GET"])
def admin_signin():
    error = None
    success = None

    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()

        if not username or  not password:
            error = "please complete all fields"
        else:
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            cur.execute("""
                SElECT AdminID,username,password
                FROM admins
                WHERE username =  ?
        """,(username,))
            admin = cur.fetchone()
            con.close()
            if  admin and admin[2] == password:
                success = "admin logged in successfully"
                session["admin_id"] = admin[0]
                return redirect (url_for("admin_dashboard"))
            else:
                error = "Invalid username or password."
    return render_template("admin_signin.html",error=error,success = success)
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin_signin"))
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cur.execute("SELECT COUNT (*) FROM Films")
    total_films = cur.fetchone()[0]

    cur.execute("SELECT COUNT (*) FROM Screenings")
    total_screenings = cur.fetchone()[0]

    cur.execute("SELECT COUNT (*) FROM Bookings")
    total_bookings = cur.fetchone()[0]

    con.close()
    return render_template("admin_dashboard.html", total_films=total_films, total_screenings=total_screenings, total_bookings=total_bookings)
@app.route("/manage_films")
def manage_films():
    if "admin_id" not in session:
        return redirect(url_for("admin_signin"))
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Films ORDER BY title")
    films = [dict(row) for row in cur.fetchall()]
    con.close()
    return render_template("manage_films.html", films=films)
@app.route("/manage_screenings")
def manage_screenings():
    if "admin_id" not in session:
        return redirect(url_for("admin_signin"))
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
    SELECT 
    S.ScreeningID,
    f.Title,
    S.ScreeningDate,
    S.ScreeningTime,
    S.ScreenNumber
    FROM Screenings S
    JOIN films f 
    ON S.FilmID = f.FilmID
    ORDER BY S.ScreeningDate,S.ScreeningTIME
    """)
    screenings =  [dict(row) for row in cur.fetchall()]
    con.close()
    return render_template("manage_screenings.html", screenings=screenings)
@app.route("/manage_bookings")
def manage_bookings():
    if "admin_id" not in session:
        return redirect(url_for("admin_signin"))
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor ()
    cur.execute("""
    SELECT
    b.bookingID,
    C.username,
    f.title,
    b.bookingDate,
    S.ScreeningDate,
    S.ScreeningTime,
    S.ScreenNumber,
    b.numberOfTickets,
    b.TotalPrice
    FROM bookings b 
    JOIN Customers C 
    ON b.customerID = C.customerID
    JOIN Screenings S
    ON b.screeningID = S.ScreeningID
    JOIN films f 
    ON S.filmID = f.filmID 
    ORDER BY b.bookingDate DESC
""")
    bookings = [dict(row) for row in cur.fetchall()]
    con.close()
    return render_template("manage_bookings.html",bookings=bookings)
@app.route("/archive_film/<int:film_id>",methods=["POST"])
def archive_film(film_id):
    error = None
    if "admin_id" not in session:
        return redirect(url_for("admin_signin"))
    con = sqlite3.connect(DATABASE)
    try:
        cur = con.cursor()
        cur.execute("UPDATE Films SET IsActive = 0 WHERE FilmID = ?", (film_id,))
        con.commit()
        con.close()
        return redirect(url_for("manage_films"))
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
@app.route("/edit_film/<int:film_id>",methods=["GET","POST"])
def edit_film(film_id):
    if not "admin_id" in session:
        return redirect(url_for("admin_signin"))
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("SELECT* FROM films where filmID = ?",(film_id,))
        film = cur.fetchone()
        if film is None:
            abort(404)
        if request.method == "POST":
            title = request.form.get("Title","").strip()
            genre = request.form.get("genre","").strip()
            age_rating = request.form.get("ageRating","").strip()
            duration = request.form.get("duration","").strip()
            description = request.form.get("description","").strip()
            if not title or not genre or not age_rating or not duration or not description:
                return render_template(
                    "edit_film.html",
                    film = film, 
                    error = "Please complete all fields."
                )
            try: 
                duration = int(duration)
                if duration <=0:
                 raise ValueError
            except ValueError:
                return render_template(
                    "edit_film.html",
                    film = film,
                    error ="Duration must be a positive integer."
                )
            cur.execute("""
                UPDATE films 
                SET Title = ?,
                    genre = ?,
                    AgeRating =?,
                    Duration =?,
                    description = ?
                WHERE FilmID = ?
                """, (title,
                      genre,
                      age_rating,
                      duration, 
                      description, 
                      film_id
                    ))
            con.commit()
            return redirect(url_for("manage_films"))
        return render_template("edit_film.html",film=film)
    finally:
        con.close()
@app.route("/edit_screening/<int:screening_id>",methods=["GET","POST"])
def edit_screening(screening_id):
    error = None 
    if  "admin_id" not in session:
        return redirect(url_for("admin_signin"))
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("""
            SELECT *
            From Screenings
            Where screeningID =?
            """,(screening_id,))
        screening = cur.fetchone()
        if screening is None:
            abort(404)
        cur.execute("SELECT filmID,Title FROM Films  ORDER BY Title")
        films = cur.fetchall()
        if request.method =="POST":
            film_id = request.form.get("FilmID","").strip()
            screening_date = request.form.get("ScreeningDate","").strip()
            screening_time = request.form.get("ScreeningTime","").strip()
            screen_number = request.form.get("ScreenNumber","").strip()
            if not film_id or not screening_date or not screening_time or not screen_number:
                return render_template(
                    "edit_screening.html",
                    screening =  screening,
                    films = films,
                    error = "Please complete all fields."
                )
            try:
                film_id = int(film_id)
                screen_number = int(screen_number)
                if screen_number <= 0:
                    raise ValueError
            except ValueError:
                return render_template(
                    "edit_screening.html",
                    screening = screening,
                    films = films,
                    error = "please enter a valid film and screen number."
                )
            cur.execute("SELECT FilmID FROM Films WHERE FilmID =?",(film_id,))
            if cur.fetchone() is None:
                abort(400)
            cur.execute("SELECT COUNT (*) FROM Booking WHERE ScreeningID = ?",(screening_id,))
            if cur.fetchone ()[0] > 0:
                return render_template(
                    "edit_screening.html",
                    screening = screening,
                    films = films,
                    error = "This screening has booking cannot be edited"
                )
            cur.execute("""
                UPDATE Screenings
                SET filmID = ?,
                    ScreeningDate = ?,
                    ScreeningTime = ?,
                    ScreenNumber = ?
                WHERE Screening = ?
            """, (
                film_id,
                screening_date,
                screening_time,
                screen_number,
                screening_id
            ))

            con.comitt()
            return redirect (url_for("manage_screenings"))
        
        return render_template(
            "edit_screening.html",
            screening = screening,
            films = films
        )
    finally:
        con.close()
@app.route("/delete_screening/<int:screening_id>", methods = ["POST"])
def delete_screening(screening_id):
    if "admin_id" not in session:
        return redirect(url_for("admin_signin"))
    con = sqlite3.connect(DATABASE)
    try:
        cur = con.cursor()
        cur.execute("""
            SELECT ScreeningID
            FROM Screeings
            WHERE ScreeningID = ?
        """,(screening_id))
        if cur.fetchone() is None:
            abort(404)
        cur.execute("""
            SELECT COUNT(*)
            FROM Bookings
            Where ScreeningID = ?
        """,(screening_id))
        if cur.fetchone()[0] > 0:
            abort(409,"Cannot delete a screening with existing bookings.")
        cur.execute("""
            DELETE FROM Seats
            WHERE ScreeningID = ?
        """,(screening_id))
        cur.execute("""
            DELETE FROM Screenings 
            WHERE ScreeningID = ?
        """,(screening_id))
        con.comitt()

        return redirect(url_for("manage_screenings"))
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
@app.route("/admin_logout")
def admin_logout():
    session.pop("admin_id",None)
    return redirect(url_for("admin_signin"))
if __name__ == "__main__":
    app.run(debug=True)