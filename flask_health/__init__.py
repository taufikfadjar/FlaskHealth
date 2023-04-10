from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("flask_health.config")


db = SQLAlchemy(app)

from flask_health.views import account, home, patient, doctor, catalog, registration
