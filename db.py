import sqlite3

def connect():
    return sqlite3.connect("school.db")


def init_db():
    con = connect()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student TEXT,
        date TEXT,
        homework INTEGER,
        lesson INTEGER,
        fine INTEGER,
        plus INTEGER
    )
    """)

    con.commit()
    con.close()


def add_grade(student, date, homework, lesson, fine, plus):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO grades (student, date, homework, lesson, fine, plus)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (student, date, homework, lesson, fine, plus))

    con.commit()
    con.close()


def get_all():
    con = connect()
    cur = con.cursor()

    cur.execute("SELECT * FROM grades ORDER BY date DESC")
    data = cur.fetchall()

    con.close()
    return data