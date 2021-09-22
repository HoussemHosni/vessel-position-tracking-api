from db import db

class VesselModel(db.Model):
    __tablename__ = 'vessels_positions'

    id = db.Column(db.Integer, primary_key=True)
    vessel_id = db.Column(db.Integer)
    latitude = db.Column(db.Float(precision=7))
    longitude = db.Column(db.Float(precision=7))
    position_time = db.Column(db.String)

    def __init__(self, vessel_id, latitude, longitude, position_time):

        self.vessel_id = vessel_id
        self.latitude = latitude
        self.longitude = longitude
        self.position_time = position_time

    def json(self):
        return {"vessel_id":self.vessel_id, \
                "latitude": self.latitude, \
                "longitude": self.longitude, \
                "position_time": self.position_time}

    @classmethod
    def find_by_vessel_id(cls, vessel_id):
        return cls.query.filter_by(vessel_id=vessel_id).all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

