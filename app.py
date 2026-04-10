from flask import Flask, render_template, request, redirect, session
from db import init_db, add_grade, get_all
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "school_secret"

init_db()

USERS = {
    "teacher@school.com": {"password": "1234", "role": "teacher"},

    "zaza": {"password": "1", "role": "student"},
    "taso": {"password": "1", "role": "student"},
    "giorgi": {"password": "1", "role": "student"},
    "saba": {"password": "1", "role": "student"},
    "qeti": {"password": "1", "role": "student"},
}

STUDENTS = ["zaza", "taso", "giorgi", "saba", "qeti"]


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email not in USERS:
            error = "❌ Email არასწორია"
        elif USERS[email]["password"] != password:
            error = "❌ პაროლი არასწორია"
        else:
            session["user"] = email
            session["role"] = USERS[email]["role"]

            return redirect("/teacher" if USERS[email]["role"] == "teacher" else "/student")

    return render_template("login.html", error=error)


@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if session.get("role") != "teacher":
        return redirect("/login")

    if request.method == "POST":

        fine = max(0, min(5, int(request.form["fine"])))
        plus = max(0, min(2, int(request.form["plus"])))

        homework = max(0, min(10, int(request.form["homework"])))
        lesson = max(0, min(10, int(request.form["lesson"])))

        add_grade(
            request.form["student"],
            request.form["date"],
            homework,
            lesson,
            fine,
            plus
        )

    return render_template("teacher.html", students=STUDENTS, data=get_all())


@app.route("/delete/<int:grade_id>")
def delete(grade_id):
    if session.get("role") != "teacher":
        return redirect("/login")

    con = sqlite3.connect("school.db")
    cur = con.cursor()
    cur.execute("DELETE FROM grades WHERE id=?", (grade_id,))
    con.commit()
    con.close()

    return redirect("/teacher")


@app.route("/student")
def student():
    if session.get("role") != "student":
        return redirect("/login")

    user = session["user"]
    data = [r for r in get_all() if r[1] == user]

    return render_template("student.html", data=data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)