# -*- coding: utf-8 -*-

from flask.json import JSONEncoder
from datetime import date, datetime
from gevent.wsgi import WSGIHandler

import uuid


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, uuid.UUID):
            return str(obj)

        return JSONEncoder.default(self, obj)


class CustomWSGIHandler(WSGIHandler):

    def format_request(self):
        now = datetime.now().replace(microsecond=0)

        length = self.response_length or '-'

        if self.time_finish:
            delta = '%.6f' % (self.time_finish - self.time_start)
        else:
            delta = '-'

        client_address = self.client_address[0] if isinstance(self.client_address, tuple) else self.client_address

        if 'HTTP_X_REAL_IP' in self.environ:
            client_address = self.environ['HTTP_X_REAL_IP']

        if 'HTTP_X_FORWARDED_FOR' in self.environ:
            client_address = self.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]

        return '%s - - [%s] "%s" %s %s %s' % (
            client_address or '-',
            now,
            self.requestline or '',
            # Use the native string version of the status, saved so we don't have to
            # decode. But fallback to the encoded 'status' in case of subclasses
            # (Is that really necessary? At least there's no overhead.)
            (self._orig_status or self.status or '000').split()[0],
            length,
            delta)
