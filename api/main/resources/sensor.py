from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel


class Sensor(Resource):

    # Obtener recurso
    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    # Eliminar recurso
    def delete(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)
        # db.session.commit() agrego restriccion de mustra para el usuario si elimina un sensor con sismos
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return 'INTENTO ELIMINAR UN SENSOR CON SISMOS ASOCIADOS', 409
        return "DELETE COMPLETE", 204

    # Modificar recurso
    def put(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(sensor, key, value)
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201


class Sensors(Resource):
    # Obtener recursoS
    def get(self):
        #  AGREGAR FILTRO PARA TRAER SENSORES
        filters = request.get_json().items()
        sensors = db.session.query(SensorModel)
        for key, value in filters:
            if key == "userId":
                sensors = sensors.filter(SensorModel.userId == value)
            if key == "status":
                sensors = sensors.filter(SensorModel.status == value)
            if key == 'active':
                sensors = sensors.filter(SensorModel.active == value)
        sensors.all()
        return jsonify({'Sensors': [sensor.to_json() for sensor in sensors]})

    # Insertar recurso
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        db.session.add(sensor)
        db.session.commit()
        return sensor.to_json(), 201
