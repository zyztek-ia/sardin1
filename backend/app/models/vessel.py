from backend.app import db
import datetime

class Vessel(db.Model):
    __tablename__ = 'vessels'

    id = db.Column(db.Integer, primary_key=True)
    mmsi = db.Column(db.String(9), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    vessel_type = db.Column(db.String(50))
    length_m = db.Column(db.Numeric(5, 2))
    beam_m = db.Column(db.Numeric(5, 2))

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    owner = db.relationship('User', backref=db.backref('vessels', lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Vessel {self.name} (MMSI: {self.mmsi})>'
