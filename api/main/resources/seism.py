from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel
from main.models import SensorModel
from random import uniform, randint  # importado para metodo POST
import time, datetime  # importado para metodo POST
from main.auth.decorators import admin_required


# Recurso dato sismo
class VerifiedSeism(Resource):
    # Obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if seism.verified:
            return seism.to_json()
        else:
            return "ACCESS DENIED", 403


# Recurso dato sismoS
class VerifiedSeisms(Resource):
    # Obtener recurso

    def get(self):
        page = 1
        per_page = 25
        max_per_page = 10000

        # FILTROS sismos verificados
        filters = request.get_json().items()
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)

        for key, value in filters:
            if key == "from_date":
                value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
                seisms = seisms.filter(SeismModel.datetime >= value)
            if key == "to_date":
                value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
                seisms = seisms.filter(SeismModel.datetime <= value)
            if key == "magnitude_min":
                seisms = seisms.filter(SeismModel.magnitude >= value)
            if key == "magnitude_max":
                seisms = seisms.filter(SeismModel.magnitude <= value)
            if key == "depth_min":
                seisms = seisms.filter(SeismModel.depth >= value)
            if key == "depth_max":
                seisms = seisms.filter(SeismModel.depth <= value)
            if key == "sensor_name":
                seisms = seisms.join(SeismModel.sensor).filter(SensorModel.name.like("%" + str(value) + "%"))
            if key == "sensorId":
                seisms = seisms.join(SeismModel.sensor).filter(SensorModel.id == value)

            # ORDENAMIENTO

            if key == "sort_by":
                if value == "datetime.desc":
                    seisms = seisms.order_by(SeismModel.datetime.desc())
                if value == "datetime.asc":
                    seisms = seisms.order_by(SeismModel.datetime.asc())
                if value == "sensor.name.desc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
                if value == "sensor.name.asc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())
                if value == "magnitude.desc":
                    seisms = seisms.order_by(SeismModel.magnitude.desc())
                if value == "magnitude.asc":
                    seisms = seisms.order_by(SeismModel.magnitude.asc())
                if value == "depth.desc":
                    seisms = seisms.order_by(SeismModel.depth.desc())
                if value == "depth.asc":
                    seisms = seisms.order_by(SeismModel.depth.asc())

            # PAGINACION
            if key == "page":
                page = int(value)
            if key == "per_page":
                per_page = int(value)

        seisms = seisms.paginate(page, per_page, True, max_per_page)  # True para no mostrar error
        return jsonify({'Verified-Seisms': [seism.to_json() for seism in seisms.items],
                        'total': seisms.total,
                        'pages': seisms.pages,
                        'page': page,
                        'per_page': per_page})


# Agrego POST para facilitar el testeo y creacion de sismos
"""    def post(self):
        value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5, 250),
            'magnitude': round(uniform(2.0, 5.5), 1),
            'latitude': uniform(-180, 180),
            'longitude': uniform(-90, 90),
            'verified': True,
            'sensorId': 2,
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 'AGREGADO SISMO  VERIFICA2', 201"""


# Recurso Usismo
class UnverifiedSeism(Resource):
    # Obtener recurso
    # @jwt_required
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return "ACCESS DENIED", 403

    # Eliminar recurso
    @jwt_required
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return "DELETE COMPLETE", 204
        else:
            return "ACCESS DENIED", 403

    # Modificar recurso
    @jwt_required
    def put(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            for key, value in request.get_json().items():
                setattr(seism, key, value)
            db.session.add(seism)
            db.session.commit()
            return seism.to_json(), 201
        else:
            return "ACCESS DENIED", 403


# Recurso UsismoS
class UnverifiedSeisms(Resource):
    # Obtener recurso
    # @jwt_required
    def get(self):
        page = 1
        per_page = 10
        max_per_page = 50
        raise_error = True

        # FILTROS
        filters = request.get_json().items()
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)

        for key, value in filters:
            if key == 'sensorId':
                seisms = seisms.join(SeismModel.sensor).filter(SensorModel.id == value)
            if key == "from_date":
                value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
                seisms = seisms.filter(SeismModel.datetime >= value)

            if key == "to_date":
                value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
                seisms = seisms.filter(SeismModel.datetime <= value)

        # ORDENAMIENTO
            if key == "sort_by":
                if value == "sensor.name.desc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())
                if value == "sensor.name.asc":
                    seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())

                if value == "datetime.desc":
                    seisms = seisms.order_by(SeismModel.datetime.desc())
                if value == "datetime.asc":
                    seisms = seisms.order_by(SeismModel.datetime.asc())

                if value == "magnitude.desc":
                    seisms = seisms.order_by(SeismModel.magnitude.desc())
                if value == "magnitude.asc":
                    seisms = seisms.order_by(SeismModel.magnitude.asc())
        # PAGINACION

            if key == "page":
                page = int(value)
            if key == "per_page":
                per_page = int(value)

        seisms = seisms.paginate(page, per_page, True, max_per_page)
        return jsonify({'Unverified-Seisms': [seism.to_json() for seism in seisms.items],
                        'total': seisms.total,
                        'pages': seisms.pages,
                        'page': page,
                        'per_page': per_page
                        })

    # Agrego POST para facilitar testeo
    @admin_required
    def post(self):
        sensors = db.session.query(SensorModel).all()
        sensorsId = []
        for sensor in sensors:
            sensorsId.append(sensor.id)

        value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5, 250),
            'magnitude': round(uniform(2.0, 5.5), 1),
            'latitude': uniform(-180, 180),
            'longitude': uniform(-90, 90),
            'verified': False,
            'sensorId': sensorsId[randint(0, len(sensorsId) - 1)]
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 201
