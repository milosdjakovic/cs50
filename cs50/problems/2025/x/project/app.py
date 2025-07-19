from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    url_for,
    g,
)
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import markdown
import bleach
from datetime import datetime

from lib.db import Database
from lib.helpers import login_required
from db.init_db import init_db

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_path = init_db("main.db")
db = Database(db_path=db_path)


@app.template_filter("markdown")
def render_markdown(text):
    html = markdown.markdown(text, extensions=["fenced_code", "tables", "nl2br"])

    allowed_tags = [
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "strong",
        "em",
        "ul",
        "ol",
        "li",
        "a",
        "code",
        "pre",
        "blockquote",
        "table",
        "thead",
        "tbody",
        "tr",
        "th",
        "td",
        "hr",
        "br",
        "img",
    ]

    allowed_attributes = {
        "a": ["href", "title"],
        "img": ["src", "alt", "title"],
    }

    cleaned_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)

    return cleaned_html


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        if user:
            g.user = user[0]
        else:
            g.user = None


@app.context_processor
def inject_user():
    return dict(user=getattr(g, "user", None))


@app.context_processor
def inject_now():
    return {"now": datetime.now()}


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        security_question_id = request.form.get("security-question")
        security_answer = request.form.get("security-answer")

        if not username:
            flash("Missing username")
            return redirect("/register")

        if not password:
            flash("Missing password")
            return redirect("/register")

        if not confirmation:
            flash("Missing password confirmation")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords do not match")
            return redirect("/register")

        if not security_question_id:
            flash("Missing security question")
            return redirect("/register")

        if not security_answer:
            flash("Missing security answer")
            return redirect("/register")

        username_sanitized = username.lower().strip()

        rows = db.execute("SELECT * FROM users WHERE username = ?", username_sanitized)

        if len(rows) != 0:
            flash("User already exists")
            return redirect("/register")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        user_id = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username_sanitized,
            hashed_password,
        )

        sanitized_security_answer = security_answer.strip().lower()

        db.execute(
            "INSERT INTO user_security_answers (user_id, question_id, answer) VALUES (?, ?, ?)",
            user_id,
            security_question_id,
            sanitized_security_answer,
        )

        session["user_id"] = user_id

        return redirect("/")
    else:
        security_questions = db.execute("SELECT * FROM security_questions")
        return render_template("register.html", security_questions=security_questions)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("Missing username")
            return render_template("login.html")

        elif not password:
            flash("Missing password")
            return render_template("login.html")

        username_sanitized = username.lower().strip()

        rows = db.execute("SELECT * FROM users WHERE username = ?", username_sanitized)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/my-profile")
@login_required
def myProfile():
    user_rows = db.execute("SELECT * FROM users WHERE id = ?", session.get("user_id"))

    if len(user_rows) != 1:
        flash("User not found")
        return redirect("/")

    user = user_rows[0]

    security_questions = db.execute(
        "SELECT * FROM security_questions WHERE id NOT IN (SELECT question_id FROM user_security_answers WHERE user_id = ?)",
        session.get("user_id"),
    )

    return render_template(
        "my-profile.html", user=user, security_questions=security_questions
    )


@app.route("/change-password", methods=["POST"])
def change_password():
    new_password = request.form.get("new-password")
    repeated_new_password = request.form.get("repeated-new-password")

    if not new_password:
        flash("Missing new password")
        return redirect("/my-profile")

    if not repeated_new_password:
        flash("Missing repeated new password")
        return redirect("/my-profile")

    if new_password != repeated_new_password:
        flash("New passwords do not match")
        return redirect("/my-profile")

    user_rows = db.execute("SELECT * FROM users WHERE id = ?", session.get("user_id"))

    current_hash = user_rows[0]["hash"]
    new_hash = generate_password_hash(new_password, method="pbkdf2:sha256")

    if check_password_hash(current_hash, new_password):
        flash("New password is same as current password")
        return redirect("/my-profile")

    db.execute(
        "UPDATE users SET hash = ? WHERE id = ?",
        new_hash,
        session.get("user_id"),
    )

    flash("Password changed successfully")

    return redirect("/my-profile")


@app.route("/user/change-username/", methods=["POST"])
@login_required
def change_username():
    new_username = request.form.get("new-username")

    if not new_username:
        flash("Missing new username")
        return redirect("/my-profile")

    user_rows = db.execute("SELECT * FROM users WHERE id = ?", session.get("user_id"))

    current_username = user_rows[0]["username"]

    if current_username == new_username:
        flash("New username is same as current username")
        return redirect("/my-profile")

    db.execute(
        "UPDATE users SET username = ? WHERE id = ?",
        new_username,
        session.get("user_id"),
    )

    session["username"] = new_username
    if hasattr(g, "user") and g.user:
        g.user["username"] = new_username

    flash("Username changed successfully")

    return redirect("/my-profile")


@app.route("/note/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title:
            flash("Missing title")
            return render_template("new.html")

        if not content:
            flash("Missing content")
            return render_template("new.html")

        note_id = db.execute(
            "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
            session.get("user_id"),
            title,
            content,
        )
        print("note_id: ", note_id)

        return redirect(f"/notes/view/{note_id}")
    else:
        return render_template("new.html")


@app.route("/notes/")
@login_required
def notes():
    favorites = db.execute(
        "SELECT n.* FROM notes AS n JOIN user_favorite_notes AS ufn ON n.id = ufn.note_id WHERE trashed_at IS NULL AND n.user_id = ? ORDER BY updated_at DESC",
        session.get("user_id"),
    )
    notes = db.execute(
        "SELECT n.* FROM notes AS n WHERE trashed_at IS NULL AND n.user_id = ? AND n.id NOT IN (SELECT note_id FROM user_favorite_notes WHERE user_id = ?) ORDER BY updated_at DESC",
        session.get("user_id"),
        session.get("user_id"),
    )

    return render_template("notes.html", favorites=favorites, notes=notes)


@app.route("/")
@login_required
def index():
    return redirect("/notes/")


@app.route("/notes/view/<int:id>")
@login_required
def notes_view(id):
    print(f"id = {id}")

    if not id:
        flash("Missing note id")
        return redirect("/")

    note = db.execute("SELECT * FROM notes WHERE id = ?", id)

    if len(note) != 1:
        flash("Note not found")
        return redirect("/")

    note = note[0]
    favorited = db.execute(
        "SELECT * FROM user_favorite_notes WHERE user_id = ? AND note_id = ?",
        session.get("user_id"),
        id,
    )

    return render_template("view.html", note=note, trashed=False, favorited=favorited)


@app.route("/trash/view/<int:id>")
@login_required
def trash_view(id):
    print(f"id = {id}")

    if not id:
        flash("Missing note id")
        return redirect("/")

    note = db.execute("SELECT * FROM notes WHERE id = ?", id)

    if len(note) != 1:
        flash("Note not found")
        return redirect("/")

    note = note[0]

    flash("Note has been moved to trash")

    return render_template("view.html", note=note, trashed=True)


@app.route("/note/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    note = db.execute("SELECT * FROM notes WHERE id = ?", id)

    if len(note) != 1:
        flash("Note not found")
        return redirect("/")

    note = note[0]

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title:
            flash("Missing title")
            return render_template("edit.html", note=note)

        if not content:
            flash("Missing content")
            return render_template("edit.html", note=note)

        db.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            title,
            content,
            id,
        )

        return redirect(f"/notes/view/{id}")
    else:
        return render_template("edit.html", note=note)


@app.route("/trash/", methods=["GET", "POST"])
@login_required
def trash():
    if request.method == "POST":
        id = request.form.get("id")

        if not id:
            flash("Missing note id")
            return redirect("/")

        note = db.execute("SELECT * FROM notes WHERE id = ?", id)

        if len(note) != 1:
            flash("Note not found")
            return redirect("/")

        note = note[0]

        db.execute("UPDATE notes SET trashed_at = CURRENT_TIMESTAMP WHERE id = ?", id)

        flash("Note moved to trash")

        return redirect("/")
    else:
        notes = db.execute("SELECT * FROM notes WHERE trashed_at IS NOT NULL")
        return render_template("trash.html", notes=notes)


@app.route("/note/restore/<int:id>")
@login_required
def restore(id):
    if not id:
        flash("Missing note id")
        return redirect("/trash/")

    note = db.execute("SELECT * FROM notes WHERE id = ?", id)

    if len(note) != 1:
        flash("Note not found")
        return redirect("/trash/")

    note = note[0]

    db.execute("UPDATE notes SET trashed_at = NULL WHERE id = ?", id)

    return redirect("/trash/")


@app.route("/note/delete/", methods=["POST"])
@login_required
def delete():
    id = request.form.get("id")

    if not id:
        flash("Missing note id")
        return redirect("/")

    note = db.execute("SELECT * FROM notes WHERE id = ?", id)

    if len(note) != 1:
        flash("Note not found")
        return redirect("/")

    note = note[0]

    db.execute("DELETE FROM notes WHERE id = ?", id)

    return redirect("/trash/")


@app.route("/recover-account", methods=["GET", "POST"])
def recover_account():
    if request.method == "POST":
        username = request.form.get("username")
        new_password = request.form.get("new-password")
        repeated_new_password = request.form.get("repeated-new-password")
        security_question_id = request.form.get("security-question")
        security_answer = request.form.get("security-answer")

        if not username:
            flash("Missing username")
            return redirect("/recover-account")

        if not new_password:
            flash("Missing new password")
            return redirect("/recover-account")

        if not repeated_new_password:
            flash("Missing repeated new password")
            return redirect("/recover-account")

        if new_password != repeated_new_password:
            flash("New passwords do not match")
            return redirect("/recover-account")

        if not security_question_id:
            flash("Missing security question")
            return redirect("/register")

        if not security_answer:
            flash("Missing security answer")
            return redirect("/register")

        username_sanitized = username.lower().strip()

        users = db.execute("SELECT * FROM users WHERE username = ?", username_sanitized)

        if len(users) != 1:
            flash("User not found")
            return redirect("/recover-account")

        user = users[0]

        sanitized_security_answer = security_answer.strip().lower()

        security_answers = db.execute(
            "SELECT * FROM user_security_answers WHERE user_id = ? AND question_id = ? AND answer = ?",
            user["id"],
            security_question_id,
            sanitized_security_answer,
        )

        if len(security_answers) != 1:
            flash("Invalid security question or answer")
            return redirect("/recover-account")

        hashed_password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.execute(
            "UPDATE users SET hash = ? WHERE username = ?",
            hashed_password,
            username_sanitized,
        )

        flash("Password changed successfully. You can now log in.")
        return redirect("/login")
    else:
        security_questions = db.execute("SELECT * FROM security_questions")
        return render_template(
            "recover-account.html", security_questions=security_questions
        )
        return render_template("recover-account.html")


@app.route("/note/favorite/<int:id>")
@login_required
def favorite(id):
    if not id:
        flash("Missing note id")
        return redirect("/")

    note = db.execute("SELECT * FROM notes WHERE id = ?", id)

    if len(note) != 1:
        flash("Note not found")
        return redirect("/")

    note = note[0]

    db.execute(
        "INSERT INTO user_favorite_notes (user_id, note_id) VALUES (?, ?);",
        session.get("user_id"),
        id,
    )

    return redirect("/notes/view/" + str(id))


@app.route("/note/unfavorite/<int:id>")
@login_required
def unfavorite(id):
    if not id:
        flash("Missing note id")
        return redirect("/")

    note = db.execute("SELECT * FROM notes WHERE id = ?", id)

    if len(note) != 1:
        flash("Note not found")
        return redirect("/")

    note = note[0]

    db.execute(
        "DELETE FROM user_favorite_notes WHERE user_id = ? AND note_id = ?;",
        session.get("user_id"),
        id,
    )

    return redirect("/notes/view/" + str(id))


@app.route("/user/change-security-question/", methods=["POST"])
@login_required
def change_security_question():
    new_security_question_id = request.form.get("new-security-question")
    new_security_answer = request.form.get("new-security-answer")

    if not new_security_question_id:
        flash("Missing new security question")
        return render_template("my-profile.html")

    if not new_security_answer:
        flash("Missing new security answer")
        return render_template("my-profile.html")

    db.execute(
        "UPDATE user_security_answers SET question_id = ?, answer = ? WHERE user_id = ?",
        new_security_question_id,
        new_security_answer,
        session.get("user_id"),
    )

    flash("Security question and answer changed successfully")

    return render_template("my-profile.html")


@app.route("/user/delete-account", methods=["POST"])
@login_required
def delete_account():
    user_id = session.get("user_id")

    if not user_id:
        flash("Missing user id")
        return redirect("/")

    db.execute("DELETE FROM users WHERE id = ?", user_id)
    db.execute("DELETE FROM user_security_answers WHERE user_id = ?", user_id)
    db.execute("DELETE FROM notes WHERE user_id = ?", user_id)

    session.clear()

    return redirect("/login")
