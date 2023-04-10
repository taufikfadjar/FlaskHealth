from flask import request, redirect, url_for, render_template, flash, session, json
from flask_health import app, db

from flask_health.models.patient import Patient
from flask_health.models.doctor import Doctor
from flask_health.models.treatment import Treatment
from flask_health.models.order import Order
import uuid, datetime, copy


@app.route("/registration", methods=["GET"])
def registrationList():
    registrationList = []
    return render_template("registration/list.html", registrationList=registrationList)


@app.route("/registration/entry/", methods=["GET", "POST"])
@app.route("/registration/entry/<id>", methods=["GET", "POST"])
def registrationEntries(id=""):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    orderStatusList = ["Registration", "General Checkup", "Treatment", "Payment"]
    paymentMethods = ["Cash", "Insurance"]
    orderSubStatusList = ["Complete", "Cancel"]
    dateNow = datetime.datetime.now().strftime("%d/%m/%Y")

    patientDict = {}
    for patient in patients:
        patientDict[patient.id] = patient.first_name + " " + patient.last_name

    if request.method == "POST" and id == "":

        getRegistrationDate = datetime.datetime.strptime(
            request.form["order_date"], "%d/%m/%Y"
        )

        count = Order.query.filter_by(
            order_date=getRegistrationDate.strftime("%y-%m-%d")
        ).count()

        newRegistration = Order()
        newRegistration.id = str(uuid.uuid1())
        newRegistration.doctor_id = request.form["doctor_id"]

        newRegistration.order_date = getRegistrationDate

        newRegistration.patient_id = request.form["patient_id"]
        newRegistration.payment_method = request.form["payment_method"]

        newRegistration.isDeleted = False
        newRegistration.created_by = session.get("username")
        newRegistration.created_at = datetime.datetime.now()
        newRegistration.order_status = "Registration"
        newRegistration.order_sub_status = "Complete"
        newRegistration.order_no = count + 1

        db.session.add(newRegistration)
        db.session.commit()
        flash("A new registration has been created.")

        return redirect(url_for("registrationEntries"))

    return render_template(
        "registration/entries.html",
        patientDict=patientDict,
        doctors=doctors,
        orderStatusList=orderStatusList,
        paymentMethods=paymentMethods,
        orderSubStatusList=orderSubStatusList,
        dateNow=dateNow,
    )
