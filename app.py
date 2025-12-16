from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
import os
import re

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

    # Validation rules
    NAME_MIN = 2
    NAME_MAX = 50
    PHONE_MIN = 10
    PHONE_MAX = 15
    PASSWORD_MIN = 8

    # Allow letters + spaces + hyphen + apostrophe (e.g., O'Neil, Ana-Maria)
    NAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z\s'-]*[A-Za-z]$")

    # Basic email check (better than "@ and .", still simple)
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    # Common typo domains you can flag (optional but great for tests)
    BLOCKED_DOMAINS = {"gamil.com", "gnail.com", "hotnail.com", "yaho.com"}

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # NAME
        if not name:
            errors["name"] = "Full Name is required."
        elif len(name) < NAME_MIN:
            errors["name"] = f"Full Name must be at least {NAME_MIN} characters."
        elif len(name) > NAME_MAX:
            errors["name"] = f"Full Name must be {NAME_MAX} characters or fewer."
        elif not NAME_REGEX.match(name):
            errors["name"] = "Full Name can contain letters, spaces, hyphens (-), and apostrophes (') only."

        # EMAIL
        if not email:
            errors["email"] = "Email is required."
        elif len(email) > 254:
            errors["email"] = "Email is too long."
        elif not EMAIL_REGEX.match(email):
            errors["email"] = "Enter a valid email address (example: name@email.com)."
        else:
            domain = email.split("@")[-1].lower()
            if domain in BLOCKED_DOMAINS:
                errors["email"] = f"Did you mean {email.replace(domain, 'gmail.com')}?"

        # PHONE
        if not phone:
            errors["phone"] = "Phone Number is required."
        elif not phone.isdigit():
            errors["phone"] = "Phone Number must contain digits only (no spaces, dashes, or symbols)."
        elif len(phone) < PHONE_MIN:
            errors["phone"] = f"Phone Number must be at least {PHONE_MIN} digits."
        elif len(phone) > PHONE_MAX:
            errors["phone"] = f"Phone Number must be {PHONE_MAX} digits or fewer."

        # PASSWORD
        if not password:
            errors["password"] = "Password is required."
        elif len(password) < PASSWORD_MIN:
            errors["password"] = f"Password must be at least {PASSWORD_MIN} characters long."
        elif not any(c.isupper() for c in password):
            errors["password"] = "Password must include at least 1 uppercase letter."
        elif not any(c.islower() for c in password):
            errors["password"] = "Password must include at least 1 lowercase letter."
        elif not any(c.isdigit() for c in password):
            errors["password"] = "Password must include at least 1 number."

        # CONFIRM PASSWORD
        if not confirm_password:
            errors["confirm_password"] = "Confirm Password is required."
        elif password and (password != confirm_password):
            errors["confirm_password"] = "Passwords do not match."

        if not errors:
            success_message = "Form submitted successfully!"

    return render_template(
        "form_validation.html",
        errors=errors,
        success_message=success_message,
    )


@app.route("/practice-test-login/", methods=["GET", "POST"])
def login():
    error_general = None
    error_username = None
    error_password = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username:
            error_username = "Username is required."
        if not password:
            error_password = "Password is required."

        if not error_username and not error_password:
            if username != VALID_USERNAME:
                error_general = "Your username is invalid!"
            elif password != VALID_PASSWORD:
                error_general = "Your password is invalid!"
            else:
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("logged_in_successfully"))

    return render_template(
        "login.html",
        error_general=error_general,
        error_username=error_username,
        error_password=error_password,
    )

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