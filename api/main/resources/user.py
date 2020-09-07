from flask_restful import Resource
from flask import request, jsonify

from .. import db
from main.models import UserModel
from main.authentication import admin_required


class User(Resource):

    # Obtener recurso
    # @admin_required
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    # Modificar recurso
    # @admin_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    # Eliminar recurso
    # @admin_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return 'CANT DELETE USR WITH ASSIGNMENT', 409
        return "DELETE COMPLETE", 204


class Users(Resource):
    # Obtener recurso
    @admin_required
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify({'Users': [user.to_json() for user in users]})

    # Insertar recurso

    # @admin_required
    def post(self):
        user = UserModel.from_json(request.get_json())
        email_exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
        if email_exists:
            return 'THE EMAIL IS ALREADY IN USE', 409
        else:
            db.session.add(user)
            db.session.commit()
            return user.to_json(), 201
