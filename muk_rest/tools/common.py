# -*- coding: utf-8 -*-

import ast
import json
import importlib
import logging
import functools
import traceback

from werkzeug.exceptions import HTTPException

from odoo import _, http, api, SUPERUSER_ID
from odoo.tools import ustr, mail, config
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError

from odoo.addons.muk_rest import exceptions, tools
from odoo.addons.muk_utils.tools.json import RecordEncoder

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# Functions
#----------------------------------------------------------

def parse_value(value):
    try:
        return json.loads(value)
    except json.decoder.JSONDecodeError:
        return ast.literal_eval(value)

#----------------------------------------------------------
# Decorators
#----------------------------------------------------------

def parse_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            if isinstance(response, HTTPException):
                error = {'code': response.code, 'description': response.description}
                content = json.dumps(error, sort_keys=True, indent=4, cls=RecordEncoder)
                return http.Response(content, content_type='application/json;charset=utf-8', status=error.get('code', 500))
            return response
        except Exception as exc:
            _logger.exception("Restful API Error")
            modul = type(exc).__module__
            name = type(exc).__name__
            error = {
                "name": "%s.%s" % (modul, name) if modul else name,
                "message": ustr(exc),
                "arguments": exc.args,
                "exception_type": "error",
            }
            if config.get('rest_debug'):
                error["debug"] = traceback.format_exc()
            if isinstance(exc, HTTPException):
                error.update({'code': exc.code, 'description': exc.description})
            else:
                error.update({'code': 500, 'description': "Restful API Error"})
            if isinstance(exc, UserError):
                error["exception_type"] = "user_error"
            elif isinstance(exc, AccessError):
                error["exception_type"] = "access_error"
            elif isinstance(exc, MissingError):
                error["exception_type"] = "missing_error"
            elif isinstance(exc, ValidationError):
                error["exception_type"] = "validation_error"
            elif isinstance(exc, exceptions.common.NoDatabaseFound):
                error["exception_type"] = "database_error"
            elif isinstance(exc, exceptions.common.ModuleNotInstalled):
                error["exception_type"] = "module_error"
            elif isinstance(exc, exceptions.common.LibraryNotInstalled):
                error["exception_type"] = "library_error"
            content = json.dumps(error, indent=4, cls=RecordEncoder)
            return http.Response(content, content_type='application/json;charset=utf-8', status=error.get('code', 500))
    return wrapper

def ensure_database(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        params = http.request.params
        session = http.request.session
        database = params.get('db') and params.get('db').strip()
        if database and database not in http.db_filter([database]):
            database = None
        if not database and session.db and http.db_filter([session.db]):
            database = session.db
        if not database:
            database = http.db_monodb(http.request.httprequest)
        if not database:
            return exceptions.common.NoDatabaseFound()
        if database != session.db:
            session.logout()
        session.db = database
        return func(*args, **kwargs)
    return wrapper

def ensure_module(module='muk_rest', error=_("The Restful API is not supported by this database.")):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            states = ['installed', 'to install', 'to upgrade']
            env = api.Environment(http.request.cr, SUPERUSER_ID, {})
            record = env['ir.module.module'].search([('name', '=', module)], limit=1)
            if not record.exists() and record.state in states:
                return exceptions.common.ModuleNotInstalled(error)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def ensure_import(library='oauthlib', error=_("Authentication via OAuth is not supported!")):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                module = importlib.import_module(library)
            except ImportError:
                return exceptions.common.LibraryNotInstalled(error)
            return func(*args, **kwargs)
        return wrapper
    return decorator
