from flask import request, redirect, url_for, render_template, flash, session, json
from flask_health import app, db

from flask_health.models.patient import Patient
from flask_health.models.doctor import Doctor
from flask_health.models.treatment import Treatment
from flask_health.models.order import Order
from flask_health.models.catalog import Catalog
import uuid, datetime, copy
from flask_health.viewmodels.treatment import TreatmentViewModel
from sqlalchemy.sql import and_, or_


@app.route("/treatment", methods=["GET"])
def treatmentList():
    result = (
        db.session.query(Order, Patient, Doctor)
        .select_from(Order)
        .join(Patient)
        .join(Doctor)
        .filter(
            or_(
                Order.order_steps > 2,
                and_(Order.order_steps == 2, Order.order_status == "Complete"),
            )
        )
        .all()
    )

    treatmentResultList = []

    for order, patient, doctor in result:
        treatmentResultList.append(
            TreatmentViewModel(
                order.id,
                order.calculate_order_no(),
                order.getFormatOrderDate(),
                patient.first_name + " " + patient.last_name,
                doctor.name,
                order.getOrderStatus(3),
            )
        )
    return render_template(
        "treatment/list.html", treatmentResultList=treatmentResultList
    )


@app.route("/treatment/entry/<id>", methods=["GET", "POST"])
def treatmentEntries(id=""):
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

    if request.method == "POST" and id != "":

        orderResult.desc = request.form["desc"]

        if orderResult.order_steps < 3:
            orderResult.order_steps = 3

        if order.order_steps == 3:
            orderResult.order_status = request.form["order_status"]

        orderResult.updated_by = session.get("username")
        orderResult.updated_at = datetime.datetime.now()

        db.session.merge(orderResult)
        db.session.commit()

        Treatment.query.filter(
            and_(
                Treatment.order_id == orderResult.id,
                Treatment.catalog_id.not_in(catalogCheckUpIds),
            )
        ).delete()

        db.session.commit()

        for catalog, quantity in zip(
            request.form.getlist("catalog_id"), request.form.getlist("catalog_quantity")
        ):

            getCatalog = Catalog.query.get(catalog)

            newTreatment = Treatment()
            newTreatment.catalog_id = catalog
            newTreatment.id = str(uuid.uuid1())
            newTreatment.order_id = orderResult.id
            newTreatment.treatment_date = datetime.datetime.now()
            newTreatment.value = int(getCatalog.price) * int(quantity)
            newTreatment.quantity = int(quantity)
            newTreatment.isDeleted = False
            newTreatment.created_by = session.get("username")
            newTreatment.created_at = datetime.datetime.now()
            db.session.merge(newTreatment)

        db.session.commit()

        flash("A treatment has been updated.")
        return redirect(url_for("treatmentList"))

    if orderResult.desc == None:
        orderResult.desc = ""

    getTreatmentresult = (
        db.session.query(Treatment, Catalog)
        .select_from(Treatment)
        .join(Catalog)
        .filter(and_(Treatment.order_id == id, Catalog.category != "General Checkup"))
        .all()
    )

    return render_template(
        "treatment/entries.html",
        catalogCheckUpList=catalogCheckUpList,
        orderResult=orderResult,
        patientResult=patientResult,
        doctorResult=doctorResult,
        orderStatusList=orderStatusList,
        catalogPrescriptionList=catalogPrescriptionList,
        catalogActionList=catalogActionList,
        getTreatmentresult=getTreatmentresult,
    )
