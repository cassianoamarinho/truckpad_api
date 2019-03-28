import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app_truckpad_api = Flask(__name__)

    config_env = os.environ.get('TRUCKPAD_ENV', '').title()
    app_truckpad_api.config.from_object('truckpad_api.config.{}Config'.format(config_env))

    db.init_app(app_truckpad_api)

    migrate_truckpad_api = Migrate(app_truckpad_api, db)

    from truckpad_api import models

    return app_truckpad_api


app = create_app()


def register_blueprints():
    from truckpad_api.health import health_bp
    from truckpad_api.drivers import drivers_bp

    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(drivers_bp, url_prefix='/api')


register_blueprints()
