from flask_health import db


class Doctor(db.Model):
    __tablename__ = "doctor"
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100))
    isDeleted = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.String(100))

    def __repr__(self):
        return "<Entry id:{} name:{} >".format(self.id, self.name)
