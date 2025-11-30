from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
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
    current_year = datetime.now().year
    return render_template("home.html", current_year=current_year)

@app.route("/form-validation/", methods=["GET", "POST"])
def form_validation():
    errors = {}
    success_message = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Name validation
        if not name:
            errors["name"] = "Name is required."

        # Email validation
        if not email:
            errors["email"] = "Email is required."
        elif "@" not in email or "." not in email:
            errors["email"] = "Enter a valid email address."

        # Phone validation (simple numeric check)
        if not phone:
            errors["phone"] = "Phone number is required."
        elif not phone.isdigit():
            errors["phone"] = "Phone number must contain only digits."

        # Password validation
        if len(password) < 8:
            errors["password"] = "Password must be at least 8 characters long."

        # Confirm password
        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        # If no errors → success
        if not errors:
            success_message = "Form submitted successfully!"
    
    return render_template(
        "form_validation.html",
        errors=errors,
        success_message=success_message
    )

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

@app.route("/dropdowns/")
def dropdowns():
    countries = {
        "USA": ["New York", "California", "Texas", "Florida"],
        "Canada": ["Ontario", "Quebec", "Alberta", "British Columbia"],
        "Mexico": ["CDMX", "Jalisco", "Nuevo León"],
    }
    return render_template("dropdowns.html", countries=countries)

@app.route("/hover/")
def hover():
    return render_template("hover.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)