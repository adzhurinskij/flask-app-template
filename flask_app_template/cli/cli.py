# -*- coding: utf-8 -*-

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from flask_app_template.app import create_app
from flask_app_template.models import db


@MigrateCommand.command
def create():
    """Creates database tables from sqlalchemy models."""
    if prompt_bool("Create all tables?"):
        db.create_all()


@MigrateCommand.command
def drop():
    """Drops database tables."""
    if prompt_bool("Drop all tables?"):
        db.drop_all()


@MigrateCommand.command
def recreate():
    """Recreates database tables (same as issuing 'drop' and then 'create')."""
    drop()
    create()


def main():
    manager = Manager(create_app)

    manager.add_option('-c', '--config', dest='config', required=True)

    manager.add_command('db', MigrateCommand)

    manager.run()


if __name__ == '__main__':
    main()
