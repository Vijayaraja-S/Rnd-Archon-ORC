import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask

from .config import Config
from .controllers.document_controller import document_bp
from .controllers.document_type_controller import document_type_bp
from .extensions import db
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)
    configure_logging(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()


def register_blueprints(app):
    app.register_blueprint(document_bp, url_prefix='/document_bp')
    app.register_blueprint(document_type_bp, url_prefix='/document_type_bp')


def configure_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('App startup')
