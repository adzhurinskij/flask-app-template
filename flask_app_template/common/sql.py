# -*- coding: utf-8 -*-

from flask import abort, request
from flask_sqlalchemy import BaseQuery, Pagination


class CustomBaseQuery(BaseQuery):

    def get_or_400(self, ident, msg=None):
        """Like :meth:`get` but aborts with 400 if not found instead of returning ``None``."""

        if ident is None:
            abort(400, msg)

        rv = self.get(ident)
        if rv is None:
            abort(400, msg)
        return rv

    def get_or_404(self, ident, msg=None):
        """Like :meth:`get` but aborts with 404 if not found instead of returning ``None``."""

        if ident is None:
            abort(404, msg)

        rv = self.get(ident)
        if rv is None:
            abort(404, msg)
        return rv

    def first_or_404(self, msg=None):
        """Like :meth:`first` but aborts with 404 if not found instead of returning ``None``."""

        rv = self.first()
        if rv is None:
            abort(404, msg)
        return rv

    def first_or_400(self, msg=None):
        """Like :meth:`first` but aborts with 400 if not found instead of returning ``None``."""

        rv = self.first()
        if rv is None:
            abort(400, msg)
        return rv

    def paginate(self, page=None, per_page=None, error_out=True, max_per_page=None):
        """Returns ``per_page`` items from page ``page``.
        If ``page`` or ``per_page`` are ``None``, they will be retrieved from
        the request query. If ``max_per_page`` is specified, ``per_page`` will
        be limited to that value. If there is no request or they aren't in the
        query, they default to 1 and 20 respectively.
        When ``error_out`` is ``True`` (default), the following rules will
        cause a 404 response:
        * No items are found and ``page`` is not 1.
        * ``page`` is less than 1, or ``per_page`` is negative.
        * ``page`` or ``per_page`` are not ints.
        When ``error_out`` is ``False``, ``page`` and ``per_page`` default to
        1 and 20 respectively.
        Returns a :class:`Pagination` object.
        """

        if request:
            if page is None:
                try:
                    page = int(request.args.get('page', 1))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)

                    page = 1

            if per_page is None:
                try:
                    per_page = int(request.args.get('per_page', 20))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)

                    per_page = 20
        else:
            if page is None:
                page = 1

            if per_page is None:
                per_page = 20

        if max_per_page is not None:
            per_page = min(per_page, max_per_page)

        if page < 1:
            if error_out:
                abort(404)
            else:
                page = 1

        if per_page < 0:
            if error_out:
                abort(404)
            else:
                per_page = 20
        elif per_page == 0 and max_per_page is not None:
            per_page = max_per_page

        # unlimit
        if per_page == 0:
            items = self.all()
        else:
            items = self.limit(per_page).offset((page - 1) * per_page).all()

        if (not items or per_page == 0) and page != 1 and error_out:
            abort(404)

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, per_page, total, items)
