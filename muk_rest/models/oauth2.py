# -*- coding: utf-8 -*-

import logging

from odoo import _, models, api, fields
from odoo.exceptions import ValidationError

from odoo.addons.muk_utils.tools import security

_logger = logging.getLogger(__name__)

class OAuth2(models.Model):
    
    _name = 'muk_rest.oauth2'
    _description = "OAuth2 Configuration"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    oauth = fields.Many2one(
        comodel_name='muk_rest.oauth',
        string='OAuth',
        delegate=True,  
        required=True,
        ondelete='cascade')
    
    state = fields.Selection(
        selection=[
            ('authorization_code', 'Authorization Code'),
            ('implicit', 'Implicit'),
            ('password', 'Password Credentials'),
            ('client_credentials', 'Client Credentials')],
        string="OAuth Type",
        required=True,
        default='authorization_code')
    
    client_id = fields.Char(
        string="Client Key",
        required=True,
        default=lambda x: security.generate_token())
    
    client_secret = fields.Char(
        string="Client Secret",
        states={
            'authorization_code': [('required', True)], 
            'client_credentials': [('required', True)]},
        default=lambda x: security.generate_token())
    
    default_callback = fields.Many2one(
        compute='_compute_default_callback',
        comodel_name='muk_rest.callback',
        string="Default Callback")
    
    user = fields.Many2one(
        comodel_name='res.users',
        string="User",
        states={
            'authorization_code': [('invisible', True)], 
            'implicit': [('invisible', True)], 
            'password': [('invisible', True)], 
            'client_credentials': [('required', True)]},
        ondelete='cascade')
    
    #----------------------------------------------------------
    # Constraints
    #----------------------------------------------------------
    
    _sql_constraints = [
        ('client_id_unique', 'UNIQUE (client_id)', 'Client ID must be unique.'),
        ('client_secret_unique', 'UNIQUE (client_secret)', 'Client Secret must be unique.'),
    ]
    
    @api.constrains('state', 'callbacks')
    def _check_default_callback(self):
        for record in self.filtered(lambda rec: rec.state == 'authorization_code'):
            if not record.default_callback:
                raise ValidationError(_("Authorization Code needs a default callback."))
    
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    @api.depends('callbacks')
    def _compute_default_callback(self):
        for record in self:
            if len(record.callbacks) >= 1:
                record.default_callback = record.callbacks[0]
            else:
                record.default_callback = False
        
        
    #----------------------------------------------------------
    # Create / Update / Delete
    #----------------------------------------------------------

    def unlink(self):
        self.mapped('oauth').unlink()
        return super(OAuth2, self).unlink()
        