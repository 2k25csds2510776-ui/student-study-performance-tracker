import sqlite3


# =========================================================
# DATABASE CONNECTION
# =========================================================

connection = sqlite3.connect("student.db")

cursor = connection.cursor()


# =========================================================
# USERS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fullname TEXT NOT NULL,

    username TEXT NOT NULL UNIQUE,

    email TEXT NOT NULL UNIQUE,

    password TEXT NOT NULL,

    branch TEXT NOT NULL,

    year INTEGER NOT NULL
)
""")


# =========================================================
# MARKS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    subject TEXT NOT NULL,

    marks_obtained REAL NOT NULL,

    total_marks REAL NOT NULL,

    semester INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# =========================================================
# ATTENDANCE TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    subject TEXT NOT NULL,

    attended_classes INTEGER NOT NULL,

    total_classes INTEGER NOT NULL,

    semester INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# =========================================================
# ASSIGNMENTS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    subject TEXT NOT NULL,

    assignment_title TEXT NOT NULL,

    due_date TEXT NOT NULL,

    status TEXT NOT NULL,

    semester INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# =========================================================
# EXAMS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS exams (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    subject TEXT NOT NULL,

    exam_name TEXT NOT NULL,

    exam_date TEXT NOT NULL,

    semester INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# =========================================================
# STUDY HOURS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS study_hours (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    subject TEXT NOT NULL,

    topic TEXT NOT NULL,

    study_date TEXT NOT NULL,

    hours REAL NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# =========================================================
# SAVE CHANGES
# =========================================================

connection.commit()


print("Database created/updated successfully.")


# =========================================================
# SHOW ALL TABLES
# =========================================================

print("\nTables currently inside student.db:")


cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")


tables = cursor.fetchall()


for table in tables:

    print(table[0])


# =========================================================
# STUDY HOURS TABLE STRUCTURE
# =========================================================

print("\nStudy Hours table structure:")


cursor.execute(
    "PRAGMA table_info(study_hours)"
)


for column in cursor.fetchall():

    print(column)


# =========================================================
# CLOSE DATABASE
# =========================================================

connection.close()