from flask_health import db


class Treatment(db.Model):
    __tablename__ = "treatment"
    id = db.Column(db.String(36), primary_key=True)
    order_id = db.Column(db.String(36), db.ForeignKey("order.id"), nullable=False)
    catalog_id = db.Column(db.String(36), db.ForeignKey("catalog.id"), nullable=False)
    value = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    treatment_date = db.Column(db.DateTime)
    isDeleted = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.String(100))

    def __repr__(self):
        return "<Entry id:{} order_id:{} catalog_id:{} value:{}>".format(
            self.id, self.order_id, self.catalog_id, self.value
        )
