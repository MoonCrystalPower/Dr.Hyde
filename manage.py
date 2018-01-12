from hyde.app import app, db
import unittest

from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)


@manager.command
def test():
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('./tests')
    test_runner.run(test_suite)


@manager.command
def run_server():
    hyde.app.run()


if __name__ == '__main__':
    manager.run()
