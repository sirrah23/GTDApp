from flask import Flask, render_template, redirect, request


app = Flask(__name__)

# Route for handling the login page logic
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect("/home")
    return render_template("login.html", error=error)


# Route for handling the sign up page logic
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    return render_template("signup.html", error=error)
