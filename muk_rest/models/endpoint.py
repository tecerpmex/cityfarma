# -*- coding: utf-8 -*-

import json
import time
import base64
import logging
import datetime
import dateutil
import textwrap

from pytz import timezone

from odoo import _, models, api, fields
from odoo.http import request, Response
from odoo.exceptions import ValidationError, Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval, test_python_expr

from odoo.addons.muk_rest.tools.common import parse_value
from odoo.addons.muk_utils.tools.json import ResponseEncoder, RecordEncoder

_logger = logging.getLogger(__name__)

class Endpoint(models.Model):
    
    _name = 'muk_rest.endpoint'
    _description = "Custom Restful Endpoint"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    name = fields.Char(
        string="Name",
        required=True)
    
    active = fields.Boolean(
        string="Active",
        default=True, 
        help="When unchecked, the endpoint is hidden and will not be available through the API.")
    
    method = fields.Selection(
        selection=[
            ("GET", "GET"),
            ("POST", "POST"),
            ("PUT", "PUT"),
            ("DELETE", "DELETE")],
        string="HTTP Method",
        required=True,
        default='GET')
    
    endpoint = fields.Char(
        string="Custom Endpoint",
        required=True)
    
    route = fields.Char(
        compute='_compute_route',
        string="Restful Endpoint",
        readonly=True,
        store=True)
    
    model = fields.Many2one(
        comodel_name='ir.model', 
        string='Model', 
        required=True, 
        ondelete='cascade')
    
    model_name = fields.Char(
        related='model.model',
        string="Model Name",
        readonly=True,
        store=True)
    
    perm_read = fields.Boolean(
        string='Requires Read',
        default=True,
        help="If a client with advanced security is used, this setting can restrict access to the endpoint.")
    
    perm_write = fields.Boolean(
        string='Requires Write',
        default=True,
        help="If a client with advanced security is used, this setting can restrict access to the endpoint.")
    
    perm_create = fields.Boolean(
        string='Requires Create',
        default=True,
        help="If a client with advanced security is used, this setting can restrict access to the endpoint.")
    
    perm_unlink = fields.Boolean(
        string='Requires Delete',
        default=True,
        help="If a client with advanced security is used, this setting can restrict access to the endpoint.")
    
    state = fields.Selection(
        selection=[
            ('domain', 'Evaluate Domain'),
            ('action', 'Execute a Server Action'),
            ('code', 'Execute Python Code')],
        string='Type',
        required=True,
        default='domain', 
        help=textwrap.dedent("""\
            Type of the endpoint. The following values are available:
            - Evaluate Domain: A domain that is evaluated on the model.
            - Execute a Server Action: A server action that is run.
            - Execute Python Code: A block of Python code that will be executed.
            """))
    
    action = fields.Many2one(
        comodel_name='ir.actions.server', 
        string="Server Actions",
        domain="[('model_id', '=', model)]",
        ondelete='cascade',
        states={
            'domain': [('invisible', True)], 
            'action': [('required', True)], 
            'code': [('invisible', True)]},
        help="Action that is called by the endpoint.")
    
    domain = fields.Char(
        string='Domain',
        states={
            'domain': [('required', True)], 
            'action': [('invisible', True)], 
            'code': [('invisible', True)]},
        help="Domain that is called by the endpoint.")
    
    domain_fields = fields.Many2many(
        comodel_name='ir.model.fields',
        domain="[('model_id', '=', model)]", 
        string='Fields',
        states={
            'action': [('invisible', True)], 
            'code': [('invisible', True)]},
        help="Domain Field that will be automatically read after the search.")
    
    code = fields.Text(
        string='Code',
        states={
            'domain': [('invisible', True)], 
            'action': [('invisible', True)], 
            'code': [('required', True)]},
        help="Python code that is called by the endpoint.",
        default=textwrap.dedent("""\
            # Information about Python expression is available in the help tab of this document.
            # Enter Python code here...
            """))
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    @api.model
    def _get_eval_context(self, endpoint, params={}):
        active_id = params.get('id', None)
        active_ids = params.get('ids', [])
        if active_id and isinstance(active_id, (str, bytes, bytearray)):
            try:
                active_id = parse_value(active_id)
            except:
                try:
                    active_id = int(active_id)
                except:
                    active_id = None
        if active_ids and isinstance(active_ids, (str, bytes, bytearray)):
            try:
                active_ids = parse_value(active_ids)
            except:  
                active_ids = None
        active_id = active_id or self.env.context.get('active_id')
        active_ids = active_ids or self.env.context.get('active_ids')
        return {
            'active_id': active_id,
            'active_ids': active_ids
        }
    
    @api.model
    def _get_eval_computation_context(self, endpoint, params={}):
        context = self._get_eval_context(endpoint, params)
        context.update({
            'time': time,
            'datetime': datetime,
            'dateutil': dateutil,
            'timezone': timezone,
            'uid': self.env.uid,
            'user': self.env.user,
        })
        return context
    
    @api.model
    def _get_eval_action_context(self, endpoint, params={}):
        active_model = endpoint.model.sudo().model
        context = self._get_eval_context(endpoint, params)
        context.update({'active_model': active_model })
        return context

    @api.model
    def _get_eval_domain_context(self, endpoint, params={}):
        return self._get_eval_computation_context(endpoint, params)
    
    @api.model
    def _get_eval_code_context(self, endpoint, params={}):
        context = self._get_eval_computation_context(endpoint, params)
        model = self.env[endpoint.model.sudo().model]
        record = model.browse(context['active_id']) if context['active_id'] else None        
        records = model.browse(context['active_ids']) if context['active_ids'] else None
        context.update({
            'json': json,
            'env': self.env,
            'model': model,
            'params': params,
            'record': record,
            'records': records,
            'b64encode': base64.b64encode,
            'b64decode': base64.b64decode,
            'date_format': DEFAULT_SERVER_DATE_FORMAT,
            'datetime_format': DEFAULT_SERVER_DATETIME_FORMAT,'Warning': Warning,
            'logger': logging.getLogger("%s (%s)" % (__name__, endpoint.name)),
        })
        return context

    def evaluate(self, params):
        self.ensure_one()
        if self.state == 'domain':
            model = self.env[self.model.sudo().model]
            fields = self.domain_fields.mapped('name') or None
            domain = safe_eval(self.domain or "[]", self._get_eval_domain_context(self, params))
            result = {
                'endpoint': self.route,
                'model': model._name,
                'domain': domain,
                'fields': self.domain_fields.mapped('name'),
                'result': model.search_read(domain, fields=fields),
            }
            content = json.dumps(result, sort_keys=True, indent=4, cls=RecordEncoder)
            return Response(content, content_type='application/json;charset=utf-8', status=200)
        elif self.state == 'action':
            result = {
                'endpoint': self.route,
                'action': self.action.name,
                'result': self.action.with_context(**self._get_eval_action_context(self, params)).run(),
            }
            content = json.dumps(result, sort_keys=True, indent=4, cls=RecordEncoder)
            return Response(content, content_type='application/json;charset=utf-8', status=200)
        elif self.state == 'code':
            content = _("No result was found for this endpoint!")
            context = self._get_eval_code_context(self, params)
            safe_eval(self.code.strip(), context, mode="exec", nocopy=True)   
            if 'result' in context and context.get('result'):
                result = {'endpoint': self.route, 'result': context['result']}
                content = json.dumps(result, sort_keys=True, indent=4, cls=RecordEncoder)
            elif 'payload' in context and context.get('payload'):
                content = context['payload']
            if 'headers' in context and context.get('headers'):
                return Response(content, headers=context['headers'], status=200)
            return Response(content, content_type='application/json;charset=utf-8', status=200)
        return Response(_("Invalid endpoint!"), content_type='application/json;charset=utf-8', status=200)

    #----------------------------------------------------------
    # View
    #----------------------------------------------------------
    
    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'domain':
            self.method = 'GET'
        else:
            self.method = 'POST'
            self.domain = None

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Custom Endpoints'),
            'template': '/muk_rest/static/xls/muk_rest_endpoints.xls'
        }]
    
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    @api.depends('endpoint')
    def _compute_route(self):
        for record in self:
            record.route = "/api/custom/%s" % record.endpoint
            
    #----------------------------------------------------------
    # Create, Update, Delete
    #----------------------------------------------------------
    
    @api.constrains('code')
    def _check_code(self):
        for record in self.sudo().filtered('code'):
            message = test_python_expr(expr=record.code.strip(), mode="exec")
            if message:
                raise ValidationError(message)
    
    @api.constrains('state', 'action', 'code')
    def _validate(self):
        validators = {
            'domain': lambda rec: True,
            'action': lambda rec: rec.action,
            'code': lambda rec: rec.code,
        }
        for record in self:
            if not validators[record.state](record):
                raise ValidationError(_("Endpoint validation has failed!"))
    