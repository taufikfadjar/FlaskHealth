from flask import request, redirect, url_for, render_template, flash, session
from flask_health import app


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            flash("User name is different")
        elif request.form["password"] != app.config["PASSWORD"]:
            flash("Password is different")
        else:
            session["logged_in"] = True
            session["user_name"] = request.form["username"]
            flash("Login successful")
            return redirect(url_for("index"))
    return render_template("account/login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("user_name", None)
    flash("Logged Out")
    return redirect(url_for("index"))
