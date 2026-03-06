from flask import Flask, render_template, request, redirect, session
from database.db import users
import bcrypt

app = Flask(__name__)
app.secret_key = "smarttour_secret_key"


# Home page
@app.route("/")
def home():
    return render_template("home.html")


# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })

        return redirect("/signin")

    return render_template("signup.html")


# Login
@app.route("/signin", methods=["GET", "POST"])
def signin():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):

            session["username"] = user["username"]

            return redirect("/dashboard")

    return render_template("signin.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/signin")

    return render_template("dashboard.html", username=session["username"])


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)