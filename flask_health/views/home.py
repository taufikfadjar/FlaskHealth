from flask import request, redirect, url_for, render_template, flash, session
from flask_health import app


@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home/index.html")
