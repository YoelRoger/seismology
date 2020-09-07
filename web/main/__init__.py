import os
from flask import Flask
from dotenv import load_dotenv
from flask_breadcrumbs import Breadcrumbs
from .routes.main import main
from .routes.unverified_seism import unverified_seism


def create_app():
    app = Flask(__name__)
    Breadcrumbs(app=app)
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')

    app.register_blueprint(main)
    app.register_blueprint(unverified_seism)
    return app
