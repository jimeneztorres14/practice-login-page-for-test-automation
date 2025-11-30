from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "pta-clone-demo-secret")
app.permanent_session_lifetime = timedelta(minutes=30)

VALID_USERNAME = "student"
VALID_PASSWORD = "Password123"
ALLOWED_EXTENSIONS = {"txt", "png", "jpg", "jpeg", "pdf"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/practice-test-login/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username != VALID_USERNAME:
            error = "Your username is invalid!"
        elif password != VALID_PASSWORD:
            error = "Your password is invalid!"
        else:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("logged_in_successfully"))
    return render_template("login.html", error=error)

@app.route("/logged-in-successfully/")
def logged_in_successfully():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("success.html", username=session.get("username", "student"))

@app.route("/logout/")
def logout():
    session.clear()
    flash("You logged out of the secure area!", "info")
    return redirect(url_for("login"))

@app.route("/checkboxes/")
def checkboxes():
    return render_template("checkboxes.html")

@app.route("/dynamic-loading/")
def dynamic_loading():
    return render_template("dynamic_loading.html")

@app.route("/file-upload/", methods=["GET", "POST"])
def file_upload():
    upload_error = None
    upload_success = None
    filename = None

    if request.method == "POST":
        if "file" not in request.files:
            upload_error = "No file part in the request."
        else:
            file = request.files["file"]
            if file.filename == "":
                upload_error = "No file selected."
            elif not allowed_file(file.filename):
                upload_error = "File type not allowed. Allowed types: txt, png, jpg, jpeg, pdf."
            else:
                filename = secure_filename(file.filename)
                upload_success = f"File '{filename}' uploaded successfully (not actually saved on server)."

    return render_template(
        "file_upload.html",
        upload_error=upload_error,
        upload_success=upload_success,
        filename=filename,
    )

@app.route("/alerts/")
def alerts():
    return render_template("alerts.html")

@app.route("/tables/")
def tables():
    # Simple sample data to render in the table
    users = [
        {"name": "Alice Johnson", "email": "alice@example.com", "role": "Admin", "age": 34},
        {"name": "Bob Smith", "email": "bob@example.com", "role": "User", "age": 27},
        {"name": "Charlie Brown", "email": "charlie@example.com", "role": "Manager", "age": 41},
        {"name": "Diana Prince", "email": "diana@example.com", "role": "User", "age": 29},
        {"name": "Ethan Clark", "email": "ethan@example.com", "role": "Support", "age": 25},
    ]
    return render_template("tables.html", users=users)

@app.route("/iframe/")
def iframe():
    return render_template("iframe.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)