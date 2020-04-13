from .. import db


class Sensor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    # userId = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User: %r %r %r %r %r>' % (self.name, self.ip, self.port, self.status, self.active)

# CONVERTIR A JSON
    def to_json(self):
        sensor_json = {
            'id': self.id,
            'name': str(self.name),
            'ip': str(self.ip),
            'port': int(self.port),
            'status': bool(self.status),
            'active': bool(self.active),
            # 'userId' : int(self.userId)
        }
        return sensor_json

    @staticmethod
    def from_json(sensor_json):
        id = sensor_json.get('id')
        name = sensor_json.get('name')
        ip = sensor_json.get('ip')
        port = sensor_json.get('port')
        status = sensor_json.get('status')
        active = sensor_json.get('active')
        # userId = sensor_json.get('userId')
        return Sensor(id=id,
                      name=name,
                      ip=ip,
                      port=port,
                      status=status,
                      active=active)
