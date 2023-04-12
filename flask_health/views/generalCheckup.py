from flask import request, redirect, url_for, render_template, flash, session, json
from flask_health import app, db
from flask_health.models.patient import Patient
from flask_health.models.doctor import Doctor
from flask_health.models.treatment import Treatment
from flask_health.models.order import Order
from flask_health.models.catalog import Catalog
import uuid, datetime, copy
from flask_health.viewmodels.generalCheckup import GeneralCheckViewModel
from sqlalchemy.sql import and_, or_


@app.route("/checkup", methods=["GET"])
def checkUpList():
    result = (
        db.session.query(Order, Patient, Doctor)
        .select_from(Order)
        .join(Patient)
        .join(Doctor)
        .filter(
            or_(
                Order.order_steps > 1,
                and_(Order.order_steps == 1, Order.order_status == "Complete"),
            )
        )
        .all()
    )

    checkupList = []

    for order, patient, doctor in result:
        checkupList.append(
            GeneralCheckViewModel(
                order.id,
                order.calculate_order_no(),
                order.getFormatOrderDate(),
                patient.first_name + " " + patient.last_name,
                doctor.name,
                "",
                "",
            )
        )
    return render_template("generalCheckup/list.html", checkupList=checkupList)


@app.route("/checkup/entry/<id>", methods=["GET", "POST"])
def checkUpEntries(id=""):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    catalogCheckUpList = (
        db.session.query(Catalog).filter(Catalog.category == "General Checkup").all()
    )

    result = (
        db.session.query(Order, Patient, Doctor)
        .select_from(Order)
        .join(Patient)
        .join(Doctor)
        .filter(Order.id == id)
        .all()
    )

    orderResult = None
    patientResult = None
    doctorResult = None

    for order, patient, doctor in result:
        orderResult = order
        patientResult = patient
        doctorResult = doctor

    return render_template(
        "generalCheckup/entries.html",
        catalogCheckUpList=catalogCheckUpList,
        orderResult=orderResult,
        patientResult=patientResult,
        doctorResult=doctorResult,
    )
