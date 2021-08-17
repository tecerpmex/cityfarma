# -*- coding: utf-8 -*-

import re
import ast
import json
import urllib
import logging

from werkzeug import exceptions

from odoo import _, http, release
from odoo.http import request, Response
from odoo.tools import misc, config

from odoo.addons.muk_rest import validators, tools
from odoo.addons.muk_rest.tools.common import parse_value
from odoo.addons.muk_utils.tools.json import ResponseEncoder, RecordEncoder

_logger = logging.getLogger(__name__)
_csrf = config.get('rest_csrf', False)

class ModelController(http.Controller):

    #----------------------------------------------------------
    # Inspection
    #----------------------------------------------------------
    
    @http.route([
        '/api/field_names',
        '/api/field_names/<string:model>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def field_names(self, model, **kw):
        result = request.env[model].fields_get_keys()
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/fields',
        '/api/fields/<string:model>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def fields(self, model, fields=None, attributes=None, **kw):
        fields = fields and parse_value(fields) or None
        attributes = attributes and parse_value(attributes) or None
        result = request.env[model].fields_get(allfields=fields, attributes=attributes)
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/metadata',
        '/api/metadata/<string:model>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def metadata(self, model, ids, context=None, **kw):
        ctx = request.session.context.copy()
        ctx.update(context and parse_value(context) or {})
        ids = ids and parse_value(ids) or []
        records = request.env[model].with_context(ctx).browse(ids)
        result = records.get_metadata()
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    #----------------------------------------------------------
    # Search / Read
    #----------------------------------------------------------
    
    @http.route([
        '/api/search',
        '/api/search/<string:model>',
        '/api/search/<string:model>/<string:order>',
        '/api/search/<string:model>/<int:limit>/<string:order>',
        '/api/search/<string:model>/<int:limit>/<int:offset>/<string:order>'
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def search(self, model, domain=None, context=None, count=False, limit=80, offset=0, order=None, **kw):
        ctx = request.session.context.copy()
        ctx.update({'prefetch_fields': False})
        ctx.update(context and parse_value(context) or {})
        domain = domain and parse_value(domain) or []
        count = count and misc.str2bool(count) or None
        limit = limit and int(limit) or None
        offset = offset and int(offset) or None
        model = request.env[model].with_context(ctx)
        result = model.search(domain, offset=offset, limit=limit, order=order, count=count)
        if not count:
            result = result.ids
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/name',
        '/api/name/<string:model>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def name(self, model, ids, context=None, **kw):
        ctx = request.session.context.copy()
        ctx.update(context and parse_value(context) or {})
        ids = ids and parse_value(ids) or []
        records = request.env[model].with_context(ctx).browse(ids)
        result = records.name_get()
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/read',
        '/api/read/<string:model>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def read(self, model, ids, fields=None, context=None, **kw):
        ctx = request.session.context.copy()
        ctx.update(context and parse_value(context) or {})
        ids = ids and parse_value(ids) or []
        fields = fields and parse_value(fields) or None
        records = request.env[model].with_context(ctx).browse(ids)
        result = records.read(fields=fields)
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)

    @http.route([
        '/api/search_read',
        '/api/search_read/<string:model>',
        '/api/search_read/<string:model>/<string:order>',
        '/api/search_read/<string:model>/<int:limit>/<string:order>',
        '/api/search_read/<string:model>/<int:limit>/<int:offset>/<string:order>'
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def search_read(self, model, domain=None, fields=None, context=None, limit=80, offset=0, order=None, **kw):
        ctx = request.session.context.copy()
        ctx.update(context and parse_value(context) or {})
        domain = domain and parse_value(domain) or []
        fields = fields and parse_value(fields) or None
        limit = limit and int(limit) or None
        offset = offset and int(offset) or None
        model = request.env[model].with_context(ctx)
        result = model.search_read(domain, fields=fields, offset=offset, limit=limit, order=order)
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/read_group',
        '/api/read_group/<string:model>',
        '/api/read_group/<string:model>/<string:orderby>',
        '/api/read_group/<string:model>/<int:limit>/<string:orderby>',
        '/api/read_group/<string:model>/<int:limit>/<int:offset>/<string:orderby>'
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def read_group(self, model, domain, fields, groupby, context=None, offset=0, limit=None, orderby=False, lazy=True, **kw):
        ctx = request.session.context.copy()
        ctx.update(context and parse_value(context) or {})
        domain = domain and parse_value(domain) or []
        fields = fields and parse_value(fields) or []
        groupby = groupby and parse_value(groupby) or []
        limit = limit and int(limit) or None
        offset = offset and int(offset) or None
        lazy = misc.str2bool(lazy)
        model = request.env[model].with_context(ctx)
        result = model.read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    #----------------------------------------------------------
    # Create / Update / Delete
    #----------------------------------------------------------
    
    @http.route([
        '/api/create',
        '/api/create/<string:model>',
    ], auth="none", type='http', methods=['POST'], csrf=_csrf)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected(operations=['create'])
    def create(self, model, values=None, context=None, **kw):
        ctx = request.session.context.copy()
        ctx.update(context and parse_value(context) or {})
        values = values and parse_value(values) or {}
        model = request.env[model].with_context(ctx)
        result = model.create(values).ids
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/write',
        '/api/write/<string:model>',
    ], auth="none", type='http', methods=['PUT'], csrf=_csrf)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected(operations=['write'])
    def write(self, model, ids=None, values=None, context=None, **kw):
        ctx = request.session.context.copy()
        ctx.update(context and parse_value(context) or {})
        ids = ids and parse_value(ids) or []
        values = values and parse_value(values) or {}
        records = request.env[model].with_context(ctx).browse(ids)
        result = records.write(values)
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/unlink',
        '/api/unlink/<string:model>',
    ], auth="none", type='http', methods=['DELETE'], csrf=_csrf)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected(operations=['unlink'])
    def unlink(self, model, ids=None, context=None, **kw):
        ctx = request.session.context.copy()
        ctx.update(context and parse_value(context) or {})
        ids = ids and parse_value(ids) or []
        records = request.env[model].with_context(ctx).browse(ids)
        result = records.unlink()
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)