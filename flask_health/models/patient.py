from flask_health import db
from datetime import date


class Patient(db.Model):
    __tablename__ = "patient"
    id = db.Column(db.String(36), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    birth_place = db.Column(db.String(100))
    birth_date = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.String(100))

    def __repr__(self):
        return "<Entry id:{} first_name:{} last_name:{} sex:{} birth_place:{} birth_date:{} isDeleted:{} created_at:{}>".format(
            self.id,
            self.first_name,
            self.last_name,
            self.sex,
            self.birth_place,
            self.birth_date,
            self.isDeleted,
            self.created_at,
        )

    def calculate_age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
