#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Tag
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

# Import settings from .env file. Must define FLASK_CONFIG
if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Tag=Tag)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.option('-n',
                '--number-fakes',
                default=10,
                type=int,
                help='Number of each model type to create',
                dest='number_fakes')
def add_fake_data(number_fakes):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=number_fakes)
    Tag.generate_fake(count=number_fakes)


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()

    admin_email = 'alexharelick@gmail.com'
    if User.query.filter_by(email=admin_email).first() is None:
        User.create_confirmed_admin('Alex',
                                    'Harelick',
                                    admin_email,
                                    'password')


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production."""
    Role.insert_roles()

if __name__ == '__main__':
    manager.run()
