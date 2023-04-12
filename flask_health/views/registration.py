from flask import request, redirect, url_for, render_template, flash, session, json
from flask_health import app, db

from flask_health.models.patient import Patient
from flask_health.models.doctor import Doctor
from flask_health.models.treatment import Treatment
from flask_health.models.order import Order
import uuid, datetime, copy
from flask_health.viewmodels.registration import RegistrationViewModel


@app.route("/registration", methods=["GET"])
def registrationList():
    result = (
        db.session.query(Order, Patient, Doctor)
        .select_from(Order)
        .join(Patient)
        .join(Doctor)
        .all()
    )

    registrationList = []

    for order, patient, doctor in result:
        orderStatus = ""

        if order.order_steps == 1:
            orderStatus = order.order_status
        else:
            orderStatus = "Complete"

        registrationList.append(
            RegistrationViewModel(
                order.id,
                order.order_no,
                order.order_date.strftime("%d/%m/%Y"),
                order.payment_method,
                patient.first_name + " " + patient.last_name,
                doctor.name,
                orderStatus,
            )
        )

    return render_template("registration/list.html", registrationList=registrationList)


@app.route("/registration/entry/", methods=["GET", "POST"])
@app.route("/registration/entry/<id>", methods=["GET", "POST"])
def registrationEntries(id=""):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    paymentMethods = ["Cash", "Insurance"]
    orderStatusList = ["Complete", "Cancel"]
    dateNow = datetime.datetime.now().strftime("%d/%m/%Y")

    patientDict = {}
    for patient in patients:
        patientDict[patient.id] = patient.first_name + " " + patient.last_name

    if request.method == "POST" and id == "":
        getRegistrationDate = datetime.datetime.strptime(
            request.form["order_date"], "%d/%m/%Y"
        )

        count = Order.query.filter(Order.order_date == getRegistrationDate).count()

        newRegistration = Order()
        newRegistration.id = str(uuid.uuid1())
        newRegistration.doctor_id = request.form["doctor_id"]

        newRegistration.order_date = getRegistrationDate

        newRegistration.patient_id = request.form["patient_id"]
        newRegistration.payment_method = request.form["payment_method"]

        newRegistration.isDeleted = False
        newRegistration.created_by = session.get("username")
        newRegistration.created_at = datetime.datetime.now()
        newRegistration.order_steps = 1
        newRegistration.order_status = "Complete"
        newRegistration.order_no = count + 1

        db.session.add(newRegistration)
        db.session.commit()
        flash("A new registration has been created.")

        return redirect(url_for("registrationList"))

    if request.method == "POST" and id != "":
        order = Order.query.get(id)

        order.payment_method = request.form["payment_method"]
        order.doctor_id = request.form["doctor_id"]

        if order.order_steps == 1:
            order.order_status = request.form["order_status"]

        order.updated_by = session.get("username")
        order.updated_at = datetime.datetime.now()

        db.session.merge(order)
        db.session.commit()

        flash("A registration has been updated.")
        return redirect(url_for("registrationList"))

    if request.method == "GET" and id != "":
        order = Order.query.get(id)
        copyOrder = copy.copy(order)
        copyOrder.order_date = copyOrder.order_date.strftime("%d/%m/%Y")

        return render_template(
            "registration/entries.html",
            registration=copyOrder,
            patientDict=patientDict,
            doctors=doctors,
            paymentMethods=paymentMethods,
            orderStatusList=orderStatusList,
            dateNow=dateNow,
        )

    return render_template(
        "registration/entries.html",
        patientDict=patientDict,
        doctors=doctors,
        paymentMethods=paymentMethods,
        orderStatusList=orderStatusList,
        dateNow=dateNow,
    )
