from .. import db


class Seism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.Datetime, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)

    # sensorid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User:  %r %r %r %r %r>' % (self.id, self.datetime, self.magnitude, self.verified, self.sensorid)

    # CONVERTIR A JSON
    def to_json(self):
        seism_json = {
            'id': self.id,
            'datetime': self.dt.strftime("%Y-%m-%d %H:%M:%S"),
            'dept': int(self.depth),
            'magnitude': str(self.magnitude),
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'verified': bool(self.verified),
        }
        return seism_json

    @staticmethod
    def from_json(seism_json):
        id = seism_json.get('id')
        dt = datetime.strptime(seism_json.get('datetime'), "%Y-%m-%d %H:%M:%S")
        depth = seism_json.get('depth')
        latitude = seism_json.get('latitude')
        magnitude = seism_json.get('magnitude')
        longitude = seism_json.get('longitude')
        verified = seism_json.get('verified')
        return Seism(id=id,
                     dt=dt,
                     depth=depth,
                     latitude=latitude,
                     longitude=longitude,
                     magnitude=magnitude)
        # sensorId=sensorId
