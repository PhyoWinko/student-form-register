from flask import Flask, render_template, redirect, request, flash, url_for, send_file
import sqlite3
from datetime import datetime
import csv


app = Flask(__name__)
app.secret_key = '50729e032778cf1236bcd1f29abb874f'


def get_db_connection():
    conn = sqlite3.connect('registrations.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    sports = conn.execute('SELECT sport_name from sports')
    sports = sports.fetchall()
    print(sports)
    conn.close()
    return render_template("index.html", sports=sports)

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        year = request.form.get("year")
        roll_no = request.form.get("roll_no")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        sport = request.form.get("sport")
        register_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, year, roll_no, phone_number, email) values (?, ?, ?, ?, ?)', (name, year, roll_no, phone_number, email))
        student_row = conn.execute('SELECT id from students where phone_number = ?', (phone_number,)).fetchone()
        student_id = student_row['id']
        sport_row = conn.execute('SELECT id from sports where sport_name = ?', (sport,)).fetchone() 
        sport_id = sport_row['id']                                                                                              
        conn.execute('INSERT INTO register (student_id, sport_id, register_time) values (?, ?, ?)', (student_id, sport_id, register_time))
        conn.commit()
        conn.close()
        flash("You are successfully registered!")
        return redirect("/")
    
@app.route("/registrants", methods=["GET"])
def registrants():
    conn = get_db_connection()
    registrants = conn.execute("""
        SELECT students.name, students.year, students.roll_no, students.phone_number, students.email, sports.sport_name, register.register_time
        FROM register
        JOIN students ON register.student_id = students.id
        JOIN sports ON register.sport_id = sports.id
    """).fetchall()
    conn.close()
    return render_template("registrants.html", registrants=registrants)

@app.route("/sort_by_sports", methods=["GET"])
def sort_by_sports():
    conn = get_db_connection()
    registrants = conn.execute("""
        SELECT students.name, students.year, students.roll_no, students.phone_number, students.email, sports.sport_name, register.register_time
        FROM register
        JOIN students ON register.student_id = students.id
        JOIN sports ON register.sport_id = sports.id
        order by sport_name asc, students.name asc
    """).fetchall()
    conn.commit()
    conn.close()
    return redirect(url_for("registrants"))

@app.route("/remove_registrant", methods=["GET", "POST"])
def remove_registrant():
    name = request.form.get("name")
    conn = get_db_connection()
    registrants = conn.execute("delete from students where name = ?", (name,))
    conn.commit()
    conn.close()
    return redirect(url_for("registrants"))

@app.route('/download_csv', methods=["GET"])
def download_csv():
    # 1. Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    # 2. Execute a query
    query = """
        SELECT students.name, students.year, students.roll_no, students.phone_number, students.email, sports.sport_name, register.register_time
        FROM register
        JOIN students ON register.student_id = students.id
        JOIN sports ON register.sport_id = sports.id
    """
    cursor.execute(query)

    # Get column headers (optional but good practice)
    headers = [description[0] for description in cursor.description]

    # 3. Write to CSV
    with open('registrants.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)  # Write headers
        csv_writer.writerows(cursor.fetchall()) # Write data rows

    # Close the connection
    conn.close()

    # 6. Send the file as a response
    return send_file("registrants.csv", download_name="registrants.csv", as_attachment=True)