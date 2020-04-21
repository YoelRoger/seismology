from .. import db
from . import SensorModel


class Seism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id', ondelete='RESTRICT'), nullable=False)
    # ondelete  = RESTRICTED para no permitir eliminar sensores con sismos guardados
    # relacion con sensores < seism
    sensor = db.relationship('Sensor', back_populates="seisms", uselist=False, single_parent=True)

    def __repr__(self):
        return '<User:  %r %r %r %r %r>' % (self.id, self.datetime, self.magnitude, self.verified, self.sensorid)

    # CONVERTIR A JSON
    def to_json(self):
        # agrego verificacion para no pasar id a sensores inexistentes en json
        self.sensor = db.session.query(SensorModel).get_or_404(self.sensorId)
        seism_json = {
            'id': self.id,
            'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'dept': int(self.depth),
            'magnitude': str(self.magnitude),
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'verified': bool(self.verified),
            'sensor': self.sensor.to_json()  # paso el sensor completo asociado tambien
        }
        return seism_json

    @staticmethod
    def from_json(seism_json):
        id = seism_json.get('id')
        datetime = datetime.strptime(seism_json.get('datetime'), "%Y-%m-%d %H:%M:%S")
        depth = seism_json.get('depth')
        latitude = seism_json.get('latitude')
        magnitude = seism_json.get('magnitude')
        longitude = seism_json.get('longitude')
        verified = seism_json.get('verified')
        sensorId = seism_json.get('sensorId')  # ahora tambien recibe la clave foranea
        return Seism(id=id,
                     dt=datetime,
                     depth=depth,
                     latitude=latitude,
                     longitude=longitude,
                     magnitude=magnitude,
                     verified=verified,
                     sensorId=sensorId)
