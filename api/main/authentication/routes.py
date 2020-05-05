from main.models import UserModel
from main import db

from flask import request, Blueprint
from flask_jwt_extended import create_access_token
from .decorators import admin_required
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
def login():
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get('email')).first_or_404()
    correct_password = user.validate_pass(request.get_json().get('password'))

    if correct_password:
        access_token = create_access_token(identity=user)
        data = {"id": user.id,
                "email": user.email,
                "access_token": access_token}
        return data, 200
    else:
        return 'WRONG CREDENTIALS',


"""
@auth.route('/register', methods=['POST'])
def register():
    user = UserModel.from_json(request.get_json())
    exists = db.session.query(UserModel).filter(UserModel.id == user.id).scalar() is not None
    if exists:
        return 'EMAIL DUPLICATED', 409
    else:
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201"""
