from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

SITE_PASSWORD = "CAUFEILDBEAR45"
STUDENT_LOGIN = {"username": "student", "password": "CaulfeildStudents1957"}
TEACHER_LOGIN = {"username": "teacher", "password": "CTECHERS1957"}

DATA_FILE = "classroom_data.json"
CLASS_FILE = "sorted_classes.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(CLASS_FILE):
    with open(CLASS_FILE, "w") as f:
        json.dump({}, f)

def load_data(file):
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["site_password"] == SITE_PASSWORD:
            return redirect(url_for("login"))
        else:
            return render_template("index.html", error="Incorrect password.")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == STUDENT_LOGIN["username"] and password == STUDENT_LOGIN["password"]:
            return redirect(url_for("student"))
        elif username == TEACHER_LOGIN["username"] and password == TEACHER_LOGIN["password"]:
            return redirect(url_for("teacher"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        code_name = request.form["code_name"]
        grade_last_year = request.form["grade_last_year"]
        works_well_with = request.form["works_well_with"]
        teacher_personality = request.form["teacher_personality"]

        data = load_data(DATA_FILE)
        data.append({
            "code_name": code_name,
            "grade_last_year": grade_last_year,
            "works_well_with": works_well_with,
            "teacher_personality": teacher_personality
        })
        save_data(DATA_FILE, data)

        return render_template("student.html", success=True)
    return render_template("student.html")

@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if request.method == "POST":
        data = load_data(DATA_FILE)
        sorted_classes = {}
        class_size = 28

        grades = {}
        for student in data:
            grade = student["grade_last_year"]
            if grade not in grades:
                grades[grade] = []
            grades[grade].append(student)

        class_number = 1
        for grade, students in grades.items():
            sorted_classes[grade] = []
            for i in range(0, len(students), class_size):
                sorted_classes[grade].append({
                    "class_name": f"{grade}-Class-{class_number}",
                    "students": students[i:i]()
