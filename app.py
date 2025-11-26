import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "pta-clone-demo-secret")  # use env var in Render
app.permanent_session_lifetime = timedelta(minutes=30)

VALID_USERNAME = "student"
VALID_PASSWORD = "Password123"

@app.route("/")
def root():
    return redirect(url_for("login"))

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

@app.route("/checkboxes/")
def checkboxes():
    return render_template("checkboxes.html")

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port, debug=False)