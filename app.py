from urllib import response

from flask import Flask, render_template, request, redirect, session, flash, url_for
from database.db import users  
import bcrypt
from flask import jsonify
import requests

app = Flask(__name__)
app.secret_key = "smarttour_secret_key"  

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        print("FORM DATA:", request.form)


        first_name = request.form.get("firstName", "").strip()
        last_name = request.form.get("lastName", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        nationality = request.form.get("nationality", "")
        password = request.form.get("password", "")

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

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        print("LOGIN:", email)

        user = users.find_one({"email": email})
        print("USER:", user)

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            session["username"] = user["username"]
            session["email"] = user["email"]
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

@app.route("/explore")
def explore():
    if "username" not in session:
        return redirect(url_for("signin"))
    return render_template("explore.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

@app.route("/get_places")
def get_places():

    lat = request.args.get("lat")
    lon = request.args.get("lon")
    place_type = request.args.get("type")

    API_KEY = "945de15324b84f16884cdaee5a2acc85"

    categories = {
        "Restaurants": "catering.restaurant",
        "Hotels": "accommodation.hotel",
        "Hospitals": "healthcare.hospital",
        "Police": "service.police",
        "ATM": "service.financial.atm",
        "Tourist Places": "tourism.sights",
        "Bus Stations": "public_transport.bus",
        "Railway Stations": "public_transport.train",
        "Airports": "airport"
    }

    category = categories.get(place_type, "tourism")

    url = (
        f"https://api.geoapify.com/v2/places"
        f"?categories={category}"
        f"&filter=circle:{lon},{lat},5000"
        f"&limit=15"
        f"&apiKey={API_KEY}"
    )

    print("URL:", url)
    response = requests.get(url)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text[:500])

    data = response.json()

    places = []

    for place in data.get("features", []):
        props = place.get("properties", {})

        places.append({
            "name": props.get("name", "Unknown Place"),
            "address": props.get("formatted", "")
        })

    return jsonify(places)



if __name__ == "__main__":
    app.run(debug=True)
