from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from .extensions import db
import logging

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
sentry = Sentry(app)
logger = logging.getLogger(__name__)


def run():
    try:
        app.run('0.0.0.0', 4000, debug=True)

    except Exception as exec:
        logger.error(exec.message)
