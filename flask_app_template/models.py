# -*- coding: utf-8 -*-

from flask import current_app, make_response, jsonify, abort, session
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ForeignKeyConstraint, DateTime
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from datetime import datetime

from flask_app_template.common.sql import *


db = SQLAlchemy(query_class=BaseQuery)


class ExtendModel(object):

    # Serialize SQLAlchemy query results to JSON
    def _asdict(self):
        result = defaultdict(dict)
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)

        return result

    def add(self):
        db.session.add(self)

        return self.save()

    def update(self, exclude=['id', 'created_at', 'updated_at'], **kwargs):
        for k in kwargs:
            if k not in exclude and hasattr(self, k) is True:
                setattr(self, k, kwargs[k])

        return self.save()

    def delete(self):
        db.session.delete(self)

        return self.save()

    def save(self):
        try:
            return db.session.commit()
        except Exception as error:
            current_app.logger.error(str(error))
            db.session.rollback()
            abort(400, str(error.message))

    def __repr__(self):
        return '<%s (%s)>' % (self.__class__.__name__, dict(self._asdict()))


class ExampleModel(db.Model, ExtendModel):
    __tablename__ = 'example'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    name = Column(String, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
