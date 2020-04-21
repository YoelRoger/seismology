from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel
from random import uniform, randint  # importado para metodo POST
import time  # importado para metodo POST


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
        filters = request.get_json().items()
        # FILTROS AGREGADOS
        verified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)
        for key, value in filters:
            if key is "id_num":
                verified_seisms = verified_seisms.filter(SeismModel.id_num == value)
            if key is "datetime":
                verified_seisms = verified_seisms.filter(SeismModel.datetime == value)
            if key is "magnitude":
                verified_seisms = verified_seisms.filter(SeismModel.magnitude == value)
            if key is "sensorId":
                verified_seisms = verified_seisms.filter(SeismModel.sensor_id == value)
            verified_seisms.all()
            # seism -> verified_seism logica metal
        return jsonify({'verified_seisms': [verified_seism.to_json() for verified_seism in verified_seisms]})

    # Agrego POST para facilitar el testeo y creacion de sismos

    def post(self):
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
        return seism.to_json(), 'AGREGADO SISMO  VERIFICA2', 201


# Recurso Usismo
class UnverifiedSeism(Resource):
    # Obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return "ACCESS DENIED", 403

    # Eliminar recurso
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return "DELETE COMPLETE", 204
        else:
            return "ACCESS DENIED", 403

    # Modificar recurso
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
    def get(self):
        filters = request.get_json().items()
        # FILTROS AGREGADOS
        unverified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)
        for key, value in filters:
            if key is "id_num":
                unverified_seisms = unverified_seisms.filter(SeismModel.id_num == value)
            if key is "datetime":
                unverified_seisms = unverified_seisms.filter(SeismModel.datetime == value)
            if key is "magnitude":
                unverified_seisms = unverified_seisms.filter(SeismModel.magnitude == value)
            if key is "sensorId":
                unverified_seisms = unverified_seisms.filter(SeismModel.sensor_id == value)
            unverified_seisms.all()
        return jsonify({'unverified_seisms': [unverified_seism.to_json() for unverified_seism in unverified_seisms]})

    # Agrego POST para facilitar testeo
    def post(self):

        value_sensor = {
            'datetime': time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()),
            'depth': randint(5, 250),
            'magnitude': round(uniform(2.0, 5.5), 1),
            'latitude': uniform(-180, 180),
            'longitude': uniform(-90, 90),
            'verified': False,
            'sensorId': 2,
        }
        seism = SeismModel.from_json(value_sensor)
        db.session.add(seism)
        db.session.commit()
        return seism.to_json(), 'AGREGADO SISMO SIN VERIFICAR', 201
