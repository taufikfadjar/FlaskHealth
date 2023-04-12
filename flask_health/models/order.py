from flask_health import db


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.String(36), primary_key=True)
    patient_id = db.Column(db.String(36), db.ForeignKey("patient.id"), nullable=False)
    order_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(100))
    total_price = db.Column(db.Integer)
    order_no = db.Column(db.Integer)
    order_steps = db.Column(db.Integer)
    order_status = db.Column(db.String(100))
    order_sub_status = db.Column(db.String(100))
    doctor_id = db.Column(db.String(36), db.ForeignKey("doctor.id"), nullable=False)
    treatments = db.relationship("Treatment", backref="order", lazy=True)
    desc = db.Column(db.Text)
    isDeleted = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.String(100))

    def __repr__(self):
        return "<Entry id:{} order_date:{} order_status:{}>".format(
            self.id, self.order_date, self.order_status
        )
