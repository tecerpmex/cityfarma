# -*- coding: utf-8 -*-

import re
import ast
import json
import urllib
import logging

from werkzeug import exceptions

from odoo import _, http, release
from odoo.http import request, Response
from odoo.exceptions import AccessError, UserError

from odoo.addons.muk_rest import validators, tools
from odoo.addons.muk_rest.tools.common import parse_value
from odoo.addons.muk_utils.tools.json import ResponseEncoder, RecordEncoder

_logger = logging.getLogger(__name__)

class SecurityController(http.Controller):

    #----------------------------------------------------------
    # Access
    #----------------------------------------------------------
    
    @http.route([
        '/api/access/rights',
        '/api/access/rights/<string:model>',
        '/api/access/rights/<string:model>/<string:operation>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def access_rights(self, model, operation='read', **kw):
        try:
            result = request.env[model].check_access_rights(operation)
        except (AccessError, UserError):
            result = False
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/access/rules',
        '/api/access/rules/<string:model>',
        '/api/access/rules/<string:model>/<string:operation>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def access_rules(self, model, ids, operation='read', **kw):
        ids = ids and parse_value(ids) or []
        try:
            result = request.env[model].browse(ids).check_access_rule(operation) is None
        except (AccessError, UserError):
            result = False
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/access/fields',
        '/api/access/fields/<string:model>',
        '/api/access/fields/<string:model>/<string:operation>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def access_fields(self, model, operation='read', fields=None, **kw):
        fields = fields and parse_value(fields) or None
        try:
            result = request.env[model].check_field_access_rights(operation, fields=fields)
        except (AccessError, UserError):
            result = False
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route([
        '/api/access',
        '/api/access/<string:model>',
        '/api/access/<string:model>/<string:operation>',
    ], auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def access(self, model, ids, operation='read', fields=None, **kw):
        ids = ids and parse_value(ids) or []
        fields = fields and parse_value(fields) or None
        try:
            rights = request.env[model].check_access_rights(operation)
            rules = request.env[model].browse(ids).check_access_rule(operation) is None
            fields = request.env[model].check_field_access_rights(operation, fields=fields)
            result = rights and rules and bool(fields)
        except (AccessError, UserError):
            raise
            result = False
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)