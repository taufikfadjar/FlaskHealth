from flask import request, redirect, url_for, render_template, flash, session
from flask_health import app, db
from flask_health.models.doctor import Doctor
import uuid, datetime, copy


@app.route("/doctor", methods=["GET"])
def doctorList():
    doctors = Doctor.query.all()
    copyDoctors = copy.copy(doctors)
    return render_template("doctor/list.html", doctors=copyDoctors)


@app.route("/doctor/entry/", methods=["GET", "POST"])
@app.route("/doctor/entry/<id>", methods=["GET", "POST"])
def doctorEntries(id=""):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST" and id == "":
        newDoctor = Doctor()
        newDoctor.id = str(uuid.uuid1())
        newDoctor.name = request.form["name"]

        newDoctor.isDeleted = False
        newDoctor.created_by = session.get("username")
        newDoctor.created_at = datetime.datetime.now()

        db.session.add(newDoctor)
        db.session.commit()
        flash("A new doctor has been created.")

        return redirect(url_for("doctorList"))

    if request.method == "POST" and id != "":
        doctor = Doctor.query.get(id)
        doctor.name = request.form["name"]

        doctor.updated_by = session.get("username")
        doctor.updated_at = datetime.datetime.now()

        db.session.merge(doctor)
        db.session.commit()

        flash("A doctor has been updated.")
        return redirect(url_for("doctorList"))

    if request.method == "GET" and id != "":
        doctor = Doctor.query.get(id)
        copyDoctor = copy.copy(doctor)

        return render_template("doctor/entries.html", doctor=copyDoctor)

    return render_template("doctor/entries.html")
