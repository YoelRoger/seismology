from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel
from main.models import UserModel
from main.authentication import admin_required
from main.utilities.sensor_sockets import check_sensor
from termcolor import cprint


class Sensor(Resource):

    # Obtener recurso
    # @admin_required
    def get(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    # Eliminar recurso
    @admin_required
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
    @admin_required
    def put(self, id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(sensor, key, value)
        db.session.add(sensor)
        try:
            db.session.commit()
            return sensor.to_json(), 201
        except Exception as error:
            return str(error), 400


class Sensors(Resource):
    # Obtener recursoS
    # @admin_required
    def get(self):
        page = 1
        per_page = 15
        max_per_page = 15
        # FILTROS
        filters = request.get_json().items()
        sensors = db.session.query(SensorModel)

        for key, value in filters:
            if key == "name":
                sensors = sensors.filter(SensorModel.name.like("%" + value + "%"))
            if key == "status":
                sensors = sensors.filter(SensorModel.status == value)
            if key == "active":
                sensors = sensors.filter(SensorModel.active == value)
            if key == "user_email":
                sensors = sensors.join(SensorModel.user).filter(UserModel.email.like("%" + value + "%"))
            if key == "userId":
                sensors = sensors.join(SensorModel.user).filter(UserModel.id == value)

        # ORDENAMIENTO

            if key == "sort_by":
                if value == "name.desc":
                    sensors = sensors.order_by(SensorModel.name.desc())
                if value == "name.asc":
                    sensors = sensors.order_by(SensorModel.name.asc())
                if value == "active.desc":
                    sensors = sensors.order_by(SensorModel.active.desc())
                if value == "active.asc":
                    sensors = sensors.order_by(SensorModel.active.asc())
                if value == "status.desc":
                    sensors = sensors.order_by(SensorModel.status.desc())
                if value == "status.asc":
                    sensors = sensors.order_by(SensorModel.status.asc())
                if value == "user.email.desc":
                    sensors = sensors.join(SensorModel.user).order_by(UserModel.email.desc())
                if value == "user.email.asc":
                    sensors = sensors.join(SensorModel.user).order_by(UserModel.email.asc())

            # PAGINACION
            if key == "page":
                page = int(value)
            if key == "per_page":
                per_page = int(value)

        sensors = sensors.paginate(page, per_page, True, max_per_page)
        return jsonify({'Sensors': [sensor.to_json() for sensor in sensors.items],
                        'total': sensors.total,
                        'pages': sensors.pages,
                        'page': page,
                        'per_page': per_page
                        })
    # Insertar recurso
    # @admin_required
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        try:
            db.session.add(sensor)
            db.session.commit()
        except Exception as error:
            return str(error), 400
        return sensor.to_json(), 201


class SensorsInfo(Resource):
    # obtener lista de recursos
    def get(self):
        sensors = db.session.query(SensorModel)
        return jsonify({'Sensors': [sensor.to_json_public() for sensor in sensors],

                        })


class SensorStatus(Resource):
    def get(self, id):
        cprint("++++++++++++++++++++++++++++", "yellow")
        check_sensor(id)
        return "", 200