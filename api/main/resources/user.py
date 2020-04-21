from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel


class User(Resource):

    # Obtener recurso
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    # Modificar recurso
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    # Eliminar recurso
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return 'INTENTO ELIMINAR UN USR CON ASIGNACIONES', 409
        return "DELETE COMPLETE", 204


class Users(Resource):
    # Obtener recurso
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify({'Users': [user.to_json() for user in users]})

    # Insertar recurso
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
