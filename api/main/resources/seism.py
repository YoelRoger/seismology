from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel


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
        verified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == True).all()
        for key, value in filters:
            if key is "id_num":
                verified_seisms = verified_seisms.filter(SeismModel.id_num == value)
            elif key is "datetime":
                verified_seisms = verified_seisms.filter(SeismModel.datetime == value)
            elif key is "magnitude":
                verified_seisms = verified_seisms.filter(SeismModel.magnitude == value)
            elif key is "sensor_id":
                verified_seisms = verified_seisms.filter(SeismModel.sensor_id == value)
            verified_seisms.all()
            # seism -> verified_seism logica metal
        return jsonify({'verified_seisms': [verified_seism.to_json() for verified_seism in verified_seisms]})


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
        unverified_seisms = db.session.query(SeismModel).filter(SeismModel.verified == False).all()
        for key, value in filters:
            if key is "id_num":
                unverified_seisms = unverified_seisms.filter(SeismModel.id_num == value)
            elif key is "datetime":
                unverified_seisms = unverified_seisms.filter(SeismModel.datetime == value)
            elif key is "magnitude":
                unverified_seisms = unverified_seisms.filter(SeismModel.magnitude == value)
            elif key is "sensor_id":
                unverified_seisms = unverified_seisms.filter(SeismModel.sensor_id == value)
            unverified_seisms.all()
        return jsonify({'unverified_seisms': [unverified_seism.to_json() for unverified_seism in unverified_seisms]})

    # camb seism -> unverified_seism logica metal
