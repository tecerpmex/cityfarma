# -*- coding: utf-8 -*-

import re
import ast
import json
import urllib
import logging

from werkzeug import exceptions
from collections import OrderedDict

from odoo import _, api, http, release, service, SUPERUSER_ID
from odoo.exceptions import AccessError, UserError
from odoo.http import request, Response
from odoo.tools import topological_sort

from odoo.addons.muk_rest import validators, tools
from odoo.addons.muk_utils.tools.json import ResponseEncoder, RecordEncoder

_logger = logging.getLogger(__name__)

class SystemController(http.Controller):

    #----------------------------------------------------------
    # System
    #----------------------------------------------------------

    @http.route('/api/modules', auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    @tools.common.ensure_database
    def modules(self):
        loadable = list(http.addons_manifest)
        env = api.Environment(http.request.cr, SUPERUSER_ID, {})
        records = env['ir.module.module'].search([('state','=','installed'), ('name','in', loadable)])
        result = OrderedDict((record.name, record.dependencies_id.mapped('name')) for record in records)
        content = json.dumps(topological_sort(result), sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route('/api/languages', auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    def languages(self):
        result = [(lang[0], lang[1].split("/")[0].strip()) for lang in service.db.exp_list_lang()]
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)
    
    @http.route('/api/countries', auth="none", type='http', methods=['GET'])
    @tools.common.parse_exception
    def countries(self):
        result = service.db.exp_list_countries()
        content = json.dumps(result, sort_keys=True, indent=4, cls=ResponseEncoder)
        return Response(content, content_type='application/json;charset=utf-8', status=200)