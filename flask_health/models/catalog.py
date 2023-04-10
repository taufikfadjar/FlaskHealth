from flask_health import db


class Catalog(db.Model):
    __tablename__ = "catalog"
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    subcategory = db.Column(db.String(100))
    desc = db.Column(db.Text)
    price = db.Column(db.Integer)
    billable = db.Column(db.Boolean)
    isDeleted = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.String(100))

    def __repr__(self):
        return "<Entry id:{} name:{} category:{} subcategory:{} billable:{}>".format(
            self.id, self.name, self.category, self.subcategory, self.billable
        )
