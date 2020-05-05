import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

api = Api()
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    load_dotenv()
    if not os.path.exists(os.getenv('SQLALCHEMY_DATABASE_PATH')+os.getenv('SQLALCHEMY_DATABASE_NAME')):
        os.mknod(os.getenv('SQLALCHEMY_DATABASE_PATH') + os.getenv('SQLALCHEMY_DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('SQLALCHEMY_DATABASE_PATH')+os.getenv('SQLALCHEMY_DATABASE_NAME')
    db.init_app(app)

    app.config['JWT_SECRET_KEY'] = 'programacion12020'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

    jwt.init_app(app)

    # Verifica si la conexion es sqlite

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def activatePrimaryKeys(conection, conection_record):
            # Ejecuta el comando que activa claves foraneas en sqlite
            conection.execute('pragma foreign_keys=ON')

        with app.app_context():
            from sqlalchemy import event
            # Al conectar a la base de datos llamar a la función que activa la claves foraneas
            event.listen(db.engine, 'connect', activatePrimaryKeys)

    import main.resources as resources

    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.SensorResource, '/sensor/<id>')

    api.add_resource(resources.VerifiedseismsResource, '/verified-seisms')
    api.add_resource(resources.VerifiedseismResource, '/verified-seism/<id>')

    api.add_resource(resources.UnverifiedseismsResource, '/unverified-seisms')
    api.add_resource(resources.UnverifiedseismResource, '/unverified-seism/<id>')

    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.UsersResource, '/users')
    api.init_app(app)

    from main.authentication import authBlueprint

    app.register_blueprint(authBlueprint)

    return app
