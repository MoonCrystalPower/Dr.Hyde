from flask.ext.testing import TestCase
from hyde.extensions import db
from hyde.app import app


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
