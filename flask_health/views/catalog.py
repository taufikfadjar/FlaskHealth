from flask import request, redirect, url_for, render_template, flash, session
from flask_health import app, db
from flask_health.models.catalog import Catalog
import uuid, datetime, copy


@app.route("/catalog", methods=["GET"])
def catalogList():
    catalogs = Catalog.query.all()
    copyCatalogs = copy.copy(catalogs)

    for copyCatalog in copyCatalogs:
        print(copyCatalog)

    return render_template("catalog/list.html", catalogs=copyCatalogs)


@app.route("/catalog/entry/", methods=["GET", "POST"])
@app.route("/catalog/entry/<id>", methods=["GET", "POST"])
def catalogEntries(id=""):
    categoryList = ["General Checkup", "Diagnose", "Prescription", "Action"]

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST" and id == "":
        newCatalog = Catalog()
        newCatalog.id = str(uuid.uuid1())
        newCatalog.name = request.form["name"]
        newCatalog.category = request.form["category"]
        newCatalog.subcategory = request.form["subcategory"]
        newCatalog.desc = request.form["desc"]
        newCatalog.price = request.form["price"]

        try:
            if request.form["billable"] == "on":
                newCatalog.billable = True
        except:
            newCatalog.billable = False

        newCatalog.isDeleted = False
        newCatalog.created_by = session.get("username")
        newCatalog.created_at = datetime.datetime.now()

        db.session.add(newCatalog)
        db.session.commit()
        flash("A new catalog has been created.")

        return redirect(url_for("catalogList"))

    if request.method == "POST" and id != "":
        catalog = Catalog.query.get(id)

        catalog.name = request.form["name"]
        catalog.category = request.form["category"]
        catalog.subcategory = request.form["subcategory"]
        catalog.desc = request.form["desc"]
        catalog.price = request.form["price"]

        try:
            if request.form["billable"] == "on":
                catalog.billable = True
        except:
            catalog.billable = False

        catalog.updated_by = session.get("username")
        catalog.updated_at = datetime.datetime.now()

        db.session.merge(catalog)
        db.session.commit()

        flash("A ctalog has been updated.")
        return redirect(url_for("catalogList"))

    if request.method == "GET" and id != "":
        catalog = Catalog.query.get(id)
        copyCatalog = copy.copy(catalog)

        return render_template(
            "catalog/entries.html", catalog=copyCatalog, categoryList=categoryList
        )

    return render_template("catalog/entries.html", categoryList=categoryList)
