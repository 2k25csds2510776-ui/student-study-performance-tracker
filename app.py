from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# =========================================================
# APP SETUP
# =========================================================

app = Flask(__name__)

app.secret_key = "student_tracker_secret_key"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template("home.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = ?
            AND email = ?
        """, (
            username,
            email
        ))

        user = cursor.fetchone()

        connection.close()

        if user is None:

            return "Username or email is incorrect!"

        if check_password_hash(user[4], password):

            session["user_id"] = user[0]
            session["fullname"] = user[1]
            session["username"] = user[2]

            return redirect(
                url_for("dashboard")
            )

        else:

            return "Password is incorrect!"

    return render_template("login.html")


# =========================================================
# SIGNUP
# =========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        confirm_password = request.form[
            "confirmPassword"
        ]

        branch = request.form["branch"]
        year = request.form["year"]

        # Check passwords
        if password != confirm_password:

            return "Passwords do not match!"

        # Hash password
        hashed_password = generate_password_hash(
            password
        )

        connection = sqlite3.connect(
            "student.db"
        )

        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO users
                (
                    fullname,
                    username,
                    email,
                    password,
                    branch,
                    year
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                fullname,
                username,
                email,
                hashed_password,
                branch,
                year
            ))

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return "Username or email already exists!"

        connection.close()

        return redirect(
            url_for("login")
        )

    return render_template("signup.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    user_id = session["user_id"]

    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    # -----------------------------------------------------
    # AVERAGE MARKS PERCENTAGE
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(marks_obtained) * 100.0 /
                NULLIF(SUM(total_marks), 0),
                0
            )
        FROM marks
        WHERE user_id = ?
    """, (
        user_id,
    ))

    average_marks = cursor.fetchone()[0]


    # -----------------------------------------------------
    # OVERALL ATTENDANCE
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(attended_classes) * 100.0 /
                NULLIF(SUM(total_classes), 0),
                0
            )
        FROM attendance
        WHERE user_id = ?
    """, (
        user_id,
    ))

    attendance_percentage = cursor.fetchone()[0]


    # -----------------------------------------------------
    # PENDING ASSIGNMENTS
    # -----------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM assignments
        WHERE user_id = ?
        AND status = 'Pending'
    """, (
        user_id,
    ))

    pending_assignments = cursor.fetchone()[0]


    # -----------------------------------------------------
    # TOTAL EXAMS
    # -----------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM exams
        WHERE user_id = ?
    """, (
        user_id,
    ))

    total_exams = cursor.fetchone()[0]


    # -----------------------------------------------------
    # TOTAL STUDY HOURS
    # -----------------------------------------------------

    cursor.execute("""
        SELECT COALESCE(SUM(hours), 0)
        FROM study_hours
        WHERE user_id = ?
    """, (
        user_id,
    ))

    total_study_hours = cursor.fetchone()[0]


    connection.close()


    # Round values

    average_marks = round(
        average_marks,
        2
    )

    attendance_percentage = round(
        attendance_percentage,
        2
    )

    total_study_hours = round(
        total_study_hours,
        1
    )


    return render_template(
        "dashboard.html",

        fullname=session["fullname"],

        average_marks=average_marks,

        attendance_percentage=attendance_percentage,

        pending_assignments=pending_assignments,

        total_exams=total_exams,

        total_study_hours=total_study_hours
    )


# =========================================================
# MARKS TRACKER
# =========================================================

@app.route(
    "/marks",
    methods=["GET", "POST"]
)
def marks():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # ADD MARKS
    # -----------------------------------------------------

    if request.method == "POST":

        subject = request.form["subject"]

        marks_obtained = float(
            request.form["marks"]
        )

        total_marks = float(
            request.form["total"]
        )

        semester = int(
            request.form["semester"]
        )


        if marks_obtained < 0:

            return "Marks cannot be negative!"


        if total_marks <= 0:

            return "Total marks must be greater than 0!"


        if marks_obtained > total_marks:

            return "Marks obtained cannot be greater than total marks!"


        connection = sqlite3.connect(
            "student.db"
        )

        cursor = connection.cursor()


        cursor.execute("""
            INSERT INTO marks
            (
                user_id,
                subject,
                marks_obtained,
                total_marks,
                semester
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            subject,
            marks_obtained,
            total_marks,
            semester
        ))


        connection.commit()

        connection.close()


        return redirect(
            url_for("marks")
        )


    # -----------------------------------------------------
    # DISPLAY MARKS
    # -----------------------------------------------------

    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            subject,
            marks_obtained,
            total_marks,
            semester
        FROM marks
        WHERE user_id = ?
        ORDER BY id DESC
    """, (
        session["user_id"],
    ))


    marks_data = cursor.fetchall()


    connection.close()


    return render_template(
        "marks.html",
        marks_data=marks_data
    )


# =========================================================
# DELETE MARK
# =========================================================

@app.route(
    "/delete_mark/<int:mark_id>",
    methods=["POST"]
)
def delete_mark(mark_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        DELETE FROM marks
        WHERE id = ?
        AND user_id = ?
    """, (
        mark_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    return redirect(
        url_for("marks")
    )


# =========================================================
# ATTENDANCE TRACKER
# =========================================================

@app.route(
    "/attendence",
    methods=["GET", "POST"]
)
def attendance():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # ADD ATTENDANCE
    # -----------------------------------------------------

    if request.method == "POST":

        subject = request.form["subject"]

        attended = int(
            request.form["attended"]
        )

        total = int(
            request.form["total"]
        )

        semester = int(
            request.form["semester"]
        )


        if attended < 0:

            return "Classes attended cannot be negative!"


        if total <= 0:

            return "Total classes must be greater than 0!"


        if attended > total:

            return "Classes attended cannot be greater than total classes!"


        connection = sqlite3.connect(
            "student.db"
        )

        cursor = connection.cursor()


        cursor.execute("""
            INSERT INTO attendance
            (
                user_id,
                subject,
                attended_classes,
                total_classes,
                semester
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            subject,
            attended,
            total,
            semester
        ))


        connection.commit()

        connection.close()


        return redirect(
            url_for("attendance")
        )


    # -----------------------------------------------------
    # DISPLAY ATTENDANCE
    # -----------------------------------------------------

    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            subject,
            attended_classes,
            total_classes,
            semester
        FROM attendance
        WHERE user_id = ?
        ORDER BY id DESC
    """, (
        session["user_id"],
    ))


    attendance_data = cursor.fetchall()


    connection.close()


    return render_template(
        "attendence.html",
        attendance_data=attendance_data
    )


# =========================================================
# DELETE ATTENDANCE
# =========================================================

@app.route(
    "/delete_attendance/<int:attendance_id>",
    methods=["POST"]
)
def delete_attendance(attendance_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        DELETE FROM attendance
        WHERE id = ?
        AND user_id = ?
    """, (
        attendance_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    return redirect(
        url_for("attendance")
    )


# =========================================================
# ASSIGNMENT TRACKER
# =========================================================

@app.route(
    "/assignmenttracker",
    methods=["GET", "POST"]
)
def assignment():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # ADD ASSIGNMENT
    # -----------------------------------------------------

    if request.method == "POST":

        subject = request.form["subject"]

        assignment_title = request.form[
            "assignment"
        ]

        due_date = request.form["dueDate"]

        status = request.form["status"]

        semester = int(
            request.form["semester"]
        )


        if status not in [
            "Pending",
            "Completed"
        ]:

            return "Invalid assignment status!"


        connection = sqlite3.connect(
            "student.db"
        )

        cursor = connection.cursor()


        cursor.execute("""
            INSERT INTO assignments
            (
                user_id,
                subject,
                assignment_title,
                due_date,
                status,
                semester
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            subject,
            assignment_title,
            due_date,
            status,
            semester
        ))


        connection.commit()

        connection.close()


        return redirect(
            url_for("assignment")
        )


    # -----------------------------------------------------
    # DISPLAY ASSIGNMENTS
    # -----------------------------------------------------

    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            subject,
            assignment_title,
            due_date,
            status,
            semester
        FROM assignments
        WHERE user_id = ?
        ORDER BY due_date ASC
    """, (
        session["user_id"],
    ))


    assignment_data = cursor.fetchall()


    connection.close()


    return render_template(
        "assignmenttracker.html",
        assignment_data=assignment_data
    )


# =========================================================
# DELETE ASSIGNMENT
# =========================================================

@app.route(
    "/delete_assignment/<int:assignment_id>",
    methods=["POST"]
)
def delete_assignment(assignment_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        DELETE FROM assignments
        WHERE id = ?
        AND user_id = ?
    """, (
        assignment_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    return redirect(
        url_for("assignment")
    )


# =========================================================
# EXAM TRACKER
# =========================================================

@app.route(
    "/exam",
    methods=["GET", "POST"]
)
def exam():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # ADD EXAM
    # -----------------------------------------------------

    if request.method == "POST":

        subject = request.form["subject"]

        exam_name = request.form[
            "examName"
        ]

        exam_date = request.form[
            "examDate"
        ]

        semester = int(
            request.form["semester"]
        )


        connection = sqlite3.connect(
            "student.db"
        )

        cursor = connection.cursor()


        cursor.execute("""
            INSERT INTO exams
            (
                user_id,
                subject,
                exam_name,
                exam_date,
                semester
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            subject,
            exam_name,
            exam_date,
            semester
        ))


        connection.commit()

        connection.close()


        return redirect(
            url_for("exam")
        )


    # -----------------------------------------------------
    # DISPLAY EXAMS
    # -----------------------------------------------------

    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            subject,
            exam_name,
            exam_date,
            semester
        FROM exams
        WHERE user_id = ?
        ORDER BY exam_date ASC
    """, (
        session["user_id"],
    ))


    exam_data = cursor.fetchall()


    connection.close()


    return render_template(
        "exam.html",
        exam_data=exam_data
    )


# =========================================================
# DELETE EXAM
# =========================================================

@app.route(
    "/delete_exam/<int:exam_id>",
    methods=["POST"]
)
def delete_exam(exam_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        DELETE FROM exams
        WHERE id = ?
        AND user_id = ?
    """, (
        exam_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    return redirect(
        url_for("exam")
    )


# =========================================================
# STUDY HOURS TRACKER
# =========================================================

@app.route(
    "/study",
    methods=["GET", "POST"]
)
def study():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # ADD STUDY SESSION
    # -----------------------------------------------------

    if request.method == "POST":

        subject = request.form["subject"]

        topic = request.form["topic"]

        study_date = request.form[
            "studyDate"
        ]

        hours = float(
            request.form["hours"]
        )


        if hours <= 0:

            return "Study hours must be greater than 0!"


        connection = sqlite3.connect(
            "student.db"
        )

        cursor = connection.cursor()


        cursor.execute("""
            INSERT INTO study_hours
            (
                user_id,
                subject,
                topic,
                study_date,
                hours
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            subject,
            topic,
            study_date,
            hours
        ))


        connection.commit()

        connection.close()


        return redirect(
            url_for("study")
        )


    # -----------------------------------------------------
    # DISPLAY STUDY RECORDS
    # -----------------------------------------------------

    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            subject,
            topic,
            study_date,
            hours
        FROM study_hours
        WHERE user_id = ?
        ORDER BY study_date DESC
    """, (
        session["user_id"],
    ))


    study_data = cursor.fetchall()


    # -----------------------------------------------------
    # TOTAL STUDY HOURS
    # -----------------------------------------------------

    cursor.execute("""
        SELECT COALESCE(SUM(hours), 0)
        FROM study_hours
        WHERE user_id = ?
    """, (
        session["user_id"],
    ))


    total_hours = cursor.fetchone()[0]


    connection.close()


    return render_template(
        "study.html",
        study_data=study_data,
        total_hours=total_hours
    )


# =========================================================
# DELETE STUDY SESSION
# =========================================================

@app.route(
    "/delete_study/<int:study_id>",
    methods=["POST"]
)
def delete_study(study_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    connection = sqlite3.connect(
        "student.db"
    )

    cursor = connection.cursor()


    cursor.execute("""
        DELETE FROM study_hours
        WHERE id = ?
        AND user_id = ?
    """, (
        study_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    return redirect(
        url_for("study")
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)