#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Jack Bai'

from functools import wraps
from flask import g
from .errors import forbidden


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kw):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kw)
        return decorated_function
    return decorator
