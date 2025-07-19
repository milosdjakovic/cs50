import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def render_index(message=None):
    birthdays = db.execute("SELECT * FROM birthdays ORDER BY id DESC")
    return render_template("index.html", birthdays=birthdays, month_names=MONTH_NAMES, message=message)


def is_valid_date(day, month):
    if not 1 <= month <= 12:
        return False
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 1 <= day <= 31
    elif month == 2:
        return 1 <= day <= 29
    else:
        return 1 <= day <= 30


MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


@app.route("/")
def index():
    return render_index()


@app.route("/create", methods=["POST"])
def create():
    name = request.form.get('name')
    day = request.form.get('day')
    month = request.form.get('month')

    # Validate name
    if not name:
        return render_index(message="Name is required.")
    elif len(name) < 2 or len(name) > 100 or not name.isalpha():
        return render_index(message="Name must be between 2 and 100 alphabetic characters.")

    # Validate date
    if not month:
        return render_index(message="Month is required.")
    elif not day:
        return render_index(message="Day is required.")
    elif not is_valid_date(day=int(day), month=int(month)):
        return render_index(message="Date is not valid.")

    db.execute(
        "INSERT INTO birthdays (name, day, month) VALUES (?, ?, ?)", name, day, month)

    return redirect("/")


@app.route("/update", methods=["POST"])
def update():
    id = request.form.get('id')
    birthdays = db.execute("SELECT * FROM birthdays WHERE id = ?", id)
    birthday = birthdays[0]

    name = request.form.get('name')
    day = request.form.get('day')
    month = request.form.get('month')

    # Validate name
    if not name:
        return render_template("update.html", birthday=birthday, message="Name is required.")
    elif len(name) < 2 or len(name) > 100 or not name.isalpha():
        return render_template("update.html", birthday=birthday, message="Name must be between 2 and 100 alphabetic characters.")

    # Validate date
    if not day:
        return render_template("update.html", birthday=birthday, message="Day is required.")
    elif not month:
        return render_template("update.html", birthday=birthday, message="Month is required.")
    elif not is_valid_date(day=int(day), month=int(month)):
        return render_template("update.html", birthday=birthday, message="Date is not valid.")

    db.execute(
        "UPDATE birthdays SET name = ?, day = ?, month = ? WHERE id = ?;", name, day, month, id)

    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get('id')

    db.execute("DELETE FROM birthdays WHERE id = ?;", id)

    return redirect("/")
