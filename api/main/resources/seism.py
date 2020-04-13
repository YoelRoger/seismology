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
            return "ACCESS DENY", 403


# Recurso dato sismoS
class VerifiedSeisms(Resource):
    # Obtener recurso

    def get(self):
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True).all()
        return jsonify({'Verified-Seisms': [seism.to_json() for seism in seisms]})


# Recurso Usismo
class UnverifiedSeism(Resource):
    # Obtener recurso
    def get(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            return seism.to_json()
        else:
            return "ACCESS DENY", 403

    # Eliminar recurso
    def delete(self, id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return "DELETE COMPLETE", 204
        else:
            return "ACCESS DENY", 403

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
            return "ACCESS DENY", 403


# Recurso UsismoS
class UnverifiedSeisms(Resource):
    # Obtener recurso
    def get(self):
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False).all()
        return jsonify({'Unverified-Seisms': [seism.to_json() for seism in seisms]})
