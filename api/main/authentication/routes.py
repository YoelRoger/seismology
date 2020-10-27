from main.models import UserModel
from main import db
from main.models import SensorModel
from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token
from main.mail_methods.methods import sendMail
from main.authentication.decorators import admin_required

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
def login():
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get('email')).first_or_404()
    correct_password = user.validate_pass(request.get_json().get('password'))

    if correct_password:
        access_token = create_access_token(identity=user)
        data = '{"id":"'+str(user.id)+'", "email":"'+str(user.email)+'", "access_token":"'+access_token+'"}'
        return data, 200
    else:
        return 'WRONG CREDENTIALS', 401


@auth.route('/register', methods=['POST'])
def register():
    user = UserModel.from_json(request.get_json())
    exists = db.session.query(UserModel).filter(UserModel.id == user.id).scalar() is not None
    if exists:
        return 'EMAIL DUPLICATED', 409
    else:
        try:
            db.session.add(user)
            sent = sendMail(user.email, "Register", 'mail/register', user=user)
            if sent:
                db.session.commit()
            else:
                db.session.rollback()
                return str(sent), 502
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return user.to_json(), 201


@auth.route('/checksensors', methods=['GET'])
@admin_required
def checkStatus():
    sensors = db.session.query(SensorModel).filter(SensorModel.active == True).filter(SensorModel.status == False).all()
    if sensors:
        admins = db.session.query(UserModel).filter(UserModel.admin == True).all()
        if admins:
            adminList = [admin.email for admin in admins]
            sendMail(adminList, "DEACTIVATED SENSORS", "mail/sensor", sensorList=sensors)
        return jsonify({'sensors': [sensor.to_json() for sensor in sensors]})
    else:
        return "NO DEACTIVATED SENSOR FOUND", 200
