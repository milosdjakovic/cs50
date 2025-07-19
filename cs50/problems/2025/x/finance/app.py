import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.context_processor
def inject_functions():
    return dict(usd=usd)


@app.context_processor
def inject_user_balance():
    user_id = session.get("user_id")
    if user_id:
        return {'session_user': get_logged_in_user_data(user_id)}
    return {}


def get_logged_in_user_data(id):
    users_row = db.execute("SELECT * FROM users WHERE id = ?", id)
    return users_row[0]


def get_user_balance(id):
    rows = db.execute("SELECT cash FROM users WHERE id = ?",
                      id)
    return float(rows[0]["cash"])


def render_index():
    purchases_rows = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0 ORDER BY symbol ASC", session.get("user_id"))

    if len(purchases_rows) == 0:
        flash("No shares purchased.")
        return render_template("index.html", purchases=purchases_rows)

    purchases_data = []
    shares_value = 0.0

    for purchase in purchases_rows:
        quote = lookup(purchase["symbol"])
        quote_price = float(quote["price"])
        total_shares = int(purchase["total_shares"])
        purchases_data.append({
            "symbol": purchase["symbol"],
            "shares": total_shares,
            "price": quote_price
        })
        shares_value = shares_value + (quote_price * total_shares)

    current_balance = get_user_balance(id=session.get("user_id"))

    total = float(current_balance) + shares_value

    return render_template("index.html", purchases=purchases_data, shares_value=shares_value, total=total)


def render_sell(selected_symbol=None):
    purchases_rows = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0 ORDER BY symbol ASC", session.get("user_id"))
    available_symbols = [row['symbol'] for row in purchases_rows]
    return render_template("sell.html", available_symbols=available_symbols, selected_symbol=selected_symbol)


@app.route("/")
@login_required
def index():
    return render_index()


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")

        if not shares:
            return apology("must provide number of shares")

        if not shares.isdigit():
            return apology("must provide number of shares as a positive number")

        quote = lookup(symbol)

        if not quote:
            return apology("share symbol not found")

        current_balance = get_user_balance(id=session.get("user_id"))

        total_cost = float(shares) * float(quote["price"])

        if total_cost > current_balance:
            return apology("not enough funds to complete the purchase")

        new_balance = current_balance - total_cost

        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   new_balance, session.get("user_id"))

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session.get("user_id"), symbol.upper(), int(shares), float(quote["price"]))

        flash(
            f"Purchased {shares} {symbol.upper()} {'share' if int(shares) == 1 else 'shares'} for {usd(float(quote['price']))} each, amounting to {usd(float(quote['price']) * int(shares))}")

        return render_index()
    else:
        symbol = request.args.get("symbol", "")
        return render_template("buy.html", symbol=symbol)


@app.route("/history")
@login_required
def history():
    transactions_rows = db.execute(
        "SELECT * FROM transactions ORDER BY datetime DESC")

    if not transactions_rows:
        flash("No transactions")

    return render_template('history.html', transactions=transactions_rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if not quote:
            return apology("symbol not found")

        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        if not password:
            return apology("must provide password")

        # Ensure repeated password was submitted
        if not confirmation:
            return apology("must provide repeated password")

        # Ensure provided passwords match
        if password != confirmation:
            return apology("passwords must match")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 0:
            return apology("user already exists")

        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   username, hashed_password)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_to_sell = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")

        if not shares_to_sell:
            return apology("must provide shares")

        if not shares_to_sell.isdigit():
            return apology("must provide number of shares as a positive number")

        existing_shares_rows = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol HAVING total_shares > 0 ORDER BY symbol ASC", session.get("user_id"), symbol)

        if not existing_shares_rows:
            return apology("not enough shares to sell")

        total_shares = existing_shares_rows[0]["total_shares"]

        if int(shares_to_sell) > total_shares:
            return apology("not enough shares to sell")

        quote = lookup(symbol)

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session.get("user_id"), symbol.upper(), -int(shares_to_sell), float(quote["price"]))

        sale_total_value = float(quote["price"]) * int(shares_to_sell)

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   sale_total_value,
                   session.get("user_id"))

        flash(
            f"Sold {shares_to_sell} {symbol} {'share' if int(shares_to_sell) == 1 else 'shares'} for {usd(float(quote['price']))} each, amounting to {usd(float(quote['price']) * int(shares_to_sell))}")

        return render_index()
    else:
        symbol = request.args.get("symbol")
        return render_sell(selected_symbol=symbol)

@app.route("/shares", methods=["GET"])
@login_required
def shares():
    symbol = request.args.get("symbol")
    purchases_rows = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol HAVING total_shares > 0 ORDER BY symbol ASC", session.get("user_id"), symbol.upper())

    if not purchases_rows:
        return jsonify([])
    else:
        return jsonify(purchases_rows)


@app.route("/change-password", methods=["GET", "POST"])
def changePassword():
    if request.method == "POST":
        password = request.form.get("password")
        new_password = request.form.get("new-password")
        repeated_new_password = request.form.get("repeated-new-password")

        if not password:
            return apology("must provide current password")

        user_rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session.get("user_id"))

        current_hash = user_rows[0]["hash"]

        if not check_password_hash(current_hash, password):
            return apology("incorrect current password")

        if not new_password:
            return apology("must provide new password")

        if not repeated_new_password:
            return apology("must provide repeated new password")

        if new_password != repeated_new_password:
            return apology("new passwords do not match")

        if password == new_password:
            return apology("new password is same as current password")

        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), session.get("user_id"))

        flash("Password changed successfully")

        return render_template("change-password.html")
    else:
        return render_template("change-password.html")


@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if request.method == "POST":
        amount = request.form.get("amount")

        if not amount:
            # return redirect(url_for('error', message="Must provide an amount"))
            return apology("Must provide an amount")

        if not amount.isdigit() or int(amount) <= 0:
            # return redirect(url_for('error', message="Amount must be a positive number"))
            return apology("Amount must be a positive number")

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   int(amount), session.get("user_id"))

        flash(f"Successfully deposited {usd(int(amount))}")
        return render_template("deposit.html")
    else:
        return render_template("deposit.html")
