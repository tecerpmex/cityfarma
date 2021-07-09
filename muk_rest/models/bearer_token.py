# -*- coding: utf-8 -*-

import logging

from odoo import _, models, api, fields, SUPERUSER_ID

_logger = logging.getLogger(__name__)
    
class BearerToken(models.Model):
    
    _name = 'muk_rest.bearer_token'
    _description = "OAuth2 Bearer Token"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    access_token = fields.Char(
        string="Token",
        required=True,
        readonly=True)
    
    refresh_token = fields.Char(
        string="Refresh",
        readonly=True)
    
    expires_in = fields.Datetime(
        string="Expires_in",
        required=True,
        readonly=True)
    
    user = fields.Many2one(
        comodel_name='res.users',
        string="User",
        readonly=True,
        ondelete='cascade')
    
    oauth = fields.Many2one(
        comodel_name='muk_rest.oauth2',
        string="Configuration",
        required=True, 
        readonly=True,
        ondelete='cascade')
    
    meta_oauth = fields.Many2one(
        related='oauth.oauth',
        comodel_name='muk_rest.oauth',
        string="Base Configuration",
        invisible=True)
    
        
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    def _read_from_database(self, field_names, inherited_field_names=[]):
        super(BearerToken, self)._read_from_database(field_names, inherited_field_names)
        protected_fields = ['access_token', 'refresh_token']
        if self.env.uid != SUPERUSER_ID and set(protected_fields).intersection(field_names):
            for record in self:
                for field in protected_fields:
                    try:
                        record._cache[field]
                        record._cache[field] = '****************'
                    except:
                        pass