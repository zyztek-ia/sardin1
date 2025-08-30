from backend.app import db
from geoalchemy2.types import Geometry
import datetime

class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessels.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='planned')
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    vessel = db.relationship('Vessel', backref=db.backref('missions', lazy=True))
    creator = db.relationship('User', backref=db.backref('missions_created', lazy=True))

class Waypoint(db.Model):
    __tablename__ = 'waypoints'
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'), nullable=False)
    name = db.Column(db.String(100))
    location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    sequence_order = db.Column(db.Integer, nullable=False)
    arrival_time = db.Column(db.DateTime)

    mission = db.relationship('Mission', backref=db.backref('waypoints', lazy=True, order_by='Waypoint.sequence_order'))

class NoGoZone(db.Model):
    __tablename__ = 'no_go_zones'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    zone_type = db.Column(db.String(50))
    geometry = db.Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    risk_level = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)

class VesselTrackLog(db.Model):
    __tablename__ = 'vessel_track_logs'
    id = db.Column(db.Integer, primary_key=True)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessels.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    speed_knots = db.Column(db.Numeric(5, 2))
    course_deg = db.Column(db.Numeric(5, 2))

class ShipSensorData(db.Model):
    __tablename__ = 'ship_sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessels.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    sensor_type = db.Column(db.String(50), nullable=False) # e.g., 'engine_rpm', 'fuel_level'
    reading = db.Column(db.JSON, nullable=False)

class SonarReading(db.Model):
    __tablename__ = 'sonar_readings'
    id = db.Column(db.Integer, primary_key=True)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessels.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    raw_data = db.Column(db.JSON) # Store raw sonar data as JSON
    processed_data = db.Column(db.JSON) # Store results of AI analysis
