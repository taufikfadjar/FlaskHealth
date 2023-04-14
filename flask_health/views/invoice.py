from flask import request, redirect, url_for, render_template, flash, session, json
from flask_health import app, db

from flask_health.models.patient import Patient
from flask_health.models.doctor import Doctor
from flask_health.models.treatment import Treatment
from flask_health.models.order import Order
from flask_health.models.catalog import Catalog
import uuid, datetime, copy
from flask_health.viewmodels.invoice import InvoiceViewModel
from sqlalchemy.sql import and_, or_


@app.route("/invoice", methods=["GET"])
def invoiceList():
    result = (
        db.session.query(Order, Patient, Doctor)
        .select_from(Order)
        .join(Patient)
        .join(Doctor)
        .filter(
            or_(
                Order.order_steps > 3,
                and_(Order.order_steps == 3, Order.order_status == "Complete"),
            )
        )
        .all()
    )

    invoiceResultList = []

    for order, patient, doctor in result:
        invoiceResultList.append(
            InvoiceViewModel(
                order.id,
                order.calculate_order_no(),
                order.getFormatOrderDate(),
                patient.first_name + " " + patient.last_name,
                doctor.name,
                order.getOrderStatus(4),
            )
        )
    return render_template("invoice/list.html", invoiceResultList=invoiceResultList)


@app.route("/invoice/entry/<id>", methods=["GET", "POST"])
def invoiceEntries(id=""):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    catalogCheckUpList = (
        db.session.query(Catalog).filter(Catalog.category == "General Checkup").all()
    )

    catalogPrescriptionList = (
        db.session.query(Catalog).filter(Catalog.category == "Prescription").all()
    )

    catalogActionList = (
        db.session.query(Catalog).filter(Catalog.category == "Action").all()
    )

    orderStatusList = ["Complete", "Cancel"]

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

    catalogCheckUpIds = []
    for catalogCheckUp in catalogCheckUpList:
        catalogCheckUpIds.append(catalogCheckUp.id)

    if orderResult.desc == None:
        orderResult.desc = ""

    getTreatmentresult = (
        db.session.query(Treatment, Catalog)
        .select_from(Treatment)
        .join(Catalog)
        .filter(and_(Treatment.order_id == id, Catalog.category != "General Checkup"))
        .all()
    )

    orderResult.totalPrice = 0
    for treatment, catalog in getTreatmentresult:
        orderResult.totalPrice = orderResult.totalPrice + int(treatment.value)

    return render_template(
        "invoice/entries.html",
        catalogCheckUpList=catalogCheckUpList,
        orderResult=orderResult,
        patientResult=patientResult,
        doctorResult=doctorResult,
        orderStatusList=orderStatusList,
        catalogPrescriptionList=catalogPrescriptionList,
        catalogActionList=catalogActionList,
        getTreatmentresult=getTreatmentresult,
    )
