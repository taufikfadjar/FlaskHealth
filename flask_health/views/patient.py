from flask import request, redirect, url_for, render_template, flash, session
from flask_health import app, db
from flask_health.models.patient import Patient
import uuid, datetime, copy


@app.route("/patient/entry/", methods=["GET", "POST"])
@app.route("/patient/entry/<id>", methods=["GET", "POST"])
def patientEntries(id=""):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST" and id == "":
        newPatient = Patient()
        newPatient.id = str(uuid.uuid1())
        newPatient.first_name = request.form["firstname"]
        newPatient.last_name = request.form["lastname"]
        newPatient.sex = request.form["sex"]
        newPatient.birth_place = request.form["birthplace"]
        newPatient.birth_date = datetime.datetime.strptime(
            request.form["birthdate"], "%d/%m/%Y"
        )

        newPatient.isDeleted = False
        newPatient.created_by = session.get("username")
        newPatient.created_at = datetime.datetime.now()

        db.session.add(newPatient)
        db.session.commit()
        flash("A new patient has been created.")

        return redirect(url_for("patientList"))

    if request.method == "POST" and id != "":
        patient = Patient.query.get(id)
        patient.first_name = request.form["firstname"]
        patient.last_name = request.form["lastname"]
        patient.sex = request.form["sex"]
        patient.birth_place = request.form["birthplace"]
        patient.birth_date = datetime.datetime.strptime(
            request.form["birthdate"], "%d/%m/%Y"
        )

        patient.updated_by = session.get("username")
        patient.updated_at = datetime.datetime.now()

        db.session.merge(patient)
        db.session.commit()

        flash("A patient has been updated.")
        return redirect(url_for("patientList"))

    if request.method == "GET" and id != "":
        patient = Patient.query.get(id)
        copyPatient = copy.copy(patient)
        copyPatient.birth_date = copyPatient.birth_date.strftime("%d/%m/%Y")

        return render_template("patient/entries.html", patient=copyPatient)

    return render_template("patient/entries.html")


@app.route("/patient", methods=["GET"])
def patientList():
    patients = Patient.query.all()
    copyPatients = copy.copy(patients)

    for copyPatient in copyPatients:
        if copyPatient.sex == "0":
            copyPatient.sex = "Female"
        else:
            copyPatient.sex = "Male"

        copyPatient.birth_date = copyPatient.birth_date.strftime("%d-%B-%Y")

    return render_template("patient/list.html", patients=copyPatients)


@app.route("/patient/<id>", methods=["POST"])
def getPatientId(id):
    pass
