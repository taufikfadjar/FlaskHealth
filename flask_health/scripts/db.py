from flask_script import Command
from flask_health import db
from flask_health.models.doctor import Doctor
from flask_health.models.patient import Patient
from flask_health.models.catalog import Catalog
import uuid, datetime
from faker import Faker
import pandas as pd


class InitDB(Command):
    "create database"

    def run(self):
        db.create_all()


class SeedDB(Command):
    "seed database"

    def run(self):

        fake = Faker()

        doctorList = ["Dr. Tirta jayakusuma", "Dr. Alex Budi", "Dr. Santika Cahaya"]
        for doctor in doctorList:
            newDoctor = Doctor()
            newDoctor.name = doctor
            newDoctor.id = str(uuid.uuid1())
            newDoctor.created_by = "System"
            newDoctor.created_at = datetime.datetime.now()
            newDoctor.isDeleted = False
            db.session.add(newDoctor)
        db.session.commit()

        for _ in range(5):
            newPatient = Patient()
            newPatient.id = str(uuid.uuid1())
            newPatient.first_name = fake.first_name_male()
            newPatient.last_name = fake.last_name_male()
            newPatient.sex = 1
            newPatient.birth_place = fake.city()
            newPatient.birth_date = fake.date_between()
            newPatient.created_by = "System"
            newPatient.created_at = datetime.datetime.now()
            newPatient.isDeleted = False
            db.session.add(newPatient)

        for _ in range(5):
            newPatient = Patient()
            newPatient.id = str(uuid.uuid1())
            newPatient.first_name = fake.first_name_female()
            newPatient.last_name = fake.last_name_female()
            newPatient.sex = 0
            newPatient.birth_place = fake.city()
            newPatient.birth_date = fake.date_between()
            newPatient.created_by = "System"
            newPatient.created_at = datetime.datetime.now()
            newPatient.isDeleted = False
            db.session.add(newPatient)

        db.session.commit()

        df = pd.read_excel("DumpMasterData.xlsx", sheet_name="Obat")
        for i in range(len(df)):
            newPrescription = Catalog()
            newPrescription.id = str(uuid.uuid1())
            newPrescription.billable = True
            newPrescription.name = df.loc[i, "Nama"]
            newPrescription.category = "Prescription"
            newPrescription.price = fake.random_int(10000, 1000000)
            newPrescription.created_by = "System"
            newPrescription.created_at = datetime.datetime.now()
            newPrescription.isDeleted = False
            newPrescription.desc = ""
            newPrescription.subcategory = ""
            db.session.add(newPrescription)
        db.session.commit()

        df = pd.read_excel("DumpMasterData.xlsx", sheet_name="TindakanMedis")
        for i in range(len(df)):
            newAction = Catalog()
            newAction.id = str(uuid.uuid1())
            newAction.billable = True
            newAction.name = df.loc[i, "Nama"]
            newAction.category = "Action"
            newAction.price = fake.random_int(10000, 1000000)
            newAction.created_by = "System"
            newAction.created_at = datetime.datetime.now()
            newAction.isDeleted = False
            newAction.desc = ""
            newAction.subcategory = ""
            db.session.add(newAction)
        db.session.commit()

        df = pd.read_excel("DumpMasterData.xlsx", sheet_name="GeneralCheck")

        for i in range(len(df)):
            newCheckUp = Catalog()
            newCheckUp.id = str(uuid.uuid1())
            newCheckUp.billable = False
            newCheckUp.name = df.loc[i, "Nama"]
            newCheckUp.category = "General Checkup"
            newCheckUp.created_by = "System"
            newCheckUp.created_at = datetime.datetime.now()
            newCheckUp.isDeleted = False
            newCheckUp.desc = ""
            newCheckUp.subcategory = ""
            db.session.add(newCheckUp)
        db.session.commit()
