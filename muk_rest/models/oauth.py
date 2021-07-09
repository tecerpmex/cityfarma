# -*- coding: utf-8 -*-
import logging
import datetime
import textwrap

from odoo import _, models, api, fields

_logger = logging.getLogger(__name__)

class OAuth(models.Model):
    
    _name = 'muk_rest.oauth'
    _description = "OAuth Configuration"
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    name = fields.Char(
        string="Name",
        required=True)
    
    active = fields.Boolean(
        string="Active",
        default=True)
    
    color = fields.Integer(
        string="Color")
    
    company = fields.Char(
        string="Company")
    
    homepage = fields.Char(
        string="Homepage URL")
    
    logo_url = fields.Char(
        string="Product logo URL")
    
    privacy_policy = fields.Char(
        string="Privacy policy URL")
    
    service_terms = fields.Char(
        string="Terms of service URL")
    
    description = fields.Text(
        string="Description")
    
    security = fields.Selection(
        selection=[
            ('basic', "Basic Access Control"),
            ('advanced', "Advanced Access Control")],
        string="Security",
        required=True,
        default='basic',
        help=textwrap.dedent("""\
            Defines the security settings to be used by the Restful API
            - Basic uses the user's security clearance to check requests from the API.
            - Advanced uses other rules in addition to the user security clearance, to further restrict the access.
            """))
    
    callbacks = fields.One2many(
        comodel_name='muk_rest.callback',
        inverse_name='oauth', 
        string="Callback URLs")
    
    rules = fields.One2many(
        comodel_name='muk_rest.access',
        inverse_name='oauth', 
        string="Access Rules")
    
    sessions = fields.Integer(
        compute='_compute_sessions',
        string="Sessions")
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    def action_settings(self):
        oauth_configuration_id = next(iter(self.ids or []), None)
        oauth1 = self.env['muk_rest.oauth1'].sudo().search([('oauth', '=', oauth_configuration_id)], limit=1)
        oauth2 = self.env['muk_rest.oauth2'].sudo().search([('oauth', '=', oauth_configuration_id)], limit=1)
        action = {
            'name': _("Settings"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
        }
        if oauth1.exists():
            action.update({
                'res_model': 'muk_rest.oauth1',
                'res_id': oauth1.id
            })
        elif oauth2.exists():
            action.update({
                'res_model': 'muk_rest.oauth2',
                'res_id': oauth2.id
            })
        return action
    
    def action_sessions(self):
        oauth_configuration_id = next(iter(self.ids or []), None)
        oauth1 = self.env['muk_rest.oauth1'].sudo().search([('oauth', '=', oauth_configuration_id)], limit=1)
        oauth2 = self.env['muk_rest.oauth2'].sudo().search([('oauth', '=', oauth_configuration_id)], limit=1)
        action = {
            'name': _("Sessions"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'tree'), (False, 'form')],
            'target': 'current',
        }
        if oauth1.exists():
            action.update({
                'res_model': 'muk_rest.access_token',
                'domain': [('oauth', '=', oauth1.id)],
            })
        elif oauth2.exists():
            action.update({
                'res_model': 'muk_rest.bearer_token',
                'domain': [('oauth', '=', oauth2.id)],
                'context': {'search_default_active': 1},
            })
        return action
    
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    def _compute_sessions(self):
        for record in self:
            domain_oauth1 = [('oauth.oauth', '=', record.id)]
            domain_oauth2 = [
                '&', ('oauth.oauth', '=', record.id), 
                '|', ('expires_in', '=', False), ('expires_in', '>', datetime.datetime.utcnow())]
            count_oauth1 = self.env['muk_rest.access_token'].sudo().search(domain_oauth1, count=True)
            count_oauth2 = self.env['muk_rest.bearer_token'].sudo().search(domain_oauth2, count=True)
            record.sessions = count_oauth1 + count_oauth2
