from flask import Flask, render_template, request, redirect, session, flash, url_for
from database.db import users  
import bcrypt

app = Flask(__name__)
app.secret_key = "smarttour_secret_key"  

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        first_name = request.form["firstName"].strip()
        last_name = request.form["lastName"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()
        nationality = request.form["nationality"]
        password = request.form["password"]

        username = first_name + " " + last_name

        # Check if user exists
        if users.find_one({"email": email}):
            flash("Email already registered!", "error")
            return render_template("signup.html")

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Save user
        users.insert_one({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "nationality": nationality,
            "password": hashed_password
        })

        flash("Signup successful! Please sign in.", "success")
        return redirect(url_for("signin"))

    return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = users.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            session["username"] = user["username"]
            session["email"] = user["email"]  # Optional: store more for dashboard
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password!", "error")

    return render_template("signin.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("signin"))

    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
