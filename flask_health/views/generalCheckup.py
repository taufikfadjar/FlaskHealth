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
                order.getOrderStatus(2),
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

    if request.method == "POST" and id != "":
        orderResult.desc = request.form["desc"]

        if orderResult.order_steps < 2:
            orderResult.order_steps = 2

        if order.order_steps == 2:
            orderResult.order_status = request.form["order_status"]

        orderResult.updated_by = session.get("username")
        orderResult.updated_at = datetime.datetime.now()

        db.session.merge(orderResult)
        db.session.commit()

        catalogCheckUpIds = []
        for catalogCheckUp in catalogCheckUpList:
            catalogCheckUpIds.append(catalogCheckUp.id)

        Treatment.query.filter(
            and_(
                Treatment.order_id == orderResult.id,
                Treatment.catalog_id.in_(catalogCheckUpIds),
            )
        ).delete()

        db.session.commit()

        for catalogCheckUp in catalogCheckUpList:

            if len(request.form[catalogCheckUp.id]) > 0:
                newTreatment = Treatment()
                newTreatment.catalog_id = catalogCheckUp.id
                newTreatment.id = str(uuid.uuid1())
                newTreatment.order_id = orderResult.id
                newTreatment.treatment_date = datetime.datetime.now()
                newTreatment.value = request.form[catalogCheckUp.id]
                newTreatment.quantity = 1
                newTreatment.isDeleted = False
                newTreatment.created_by = session.get("username")
                newTreatment.created_at = datetime.datetime.now()
                db.session.merge(newTreatment)

        db.session.commit()

        flash("A general checkup has been updated.")
        return redirect(url_for("checkUpList"))

    if orderResult.desc == None:
        orderResult.desc = ""

    return render_template(
        "generalCheckup/entries.html",
        catalogCheckUpList=catalogCheckUpList,
        orderResult=orderResult,
        patientResult=patientResult,
        doctorResult=doctorResult,
        orderStatusList=orderStatusList,
    )
