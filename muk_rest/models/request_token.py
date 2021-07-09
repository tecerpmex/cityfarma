# -*- coding: utf-8 -*-

import logging

from odoo import _, models, api, fields, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class RequestToken(models.Model):
    
    _name = 'muk_rest.request_token'
    _description = "OAuth1 Request Token"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    resource_owner_key = fields.Char(
        string="Token",
        required=True,
        readonly=True)
    
    resource_owner_secret = fields.Char(
        string="Token Secret",
        required=True,
        readonly=True)
    
    callback = fields.Char(
        string="Callback",
        readonly=True)
    
    verifier = fields.Char(
        string="Verifier",
        readonly=True)
    
    user = fields.Many2one(
        comodel_name='res.users',
        string="User",
        readonly=True,
        ondelete='cascade')
    
    oauth = fields.Many2one(
        comodel_name='muk_rest.oauth1',
        string="Configuration",
        required=True,
        readonly=True,
        ondelete='cascade')
    
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    def _read_from_database(self, field_names, inherited_field_names=[]):
        super(RequestToken, self)._read_from_database(field_names, inherited_field_names)
        protected_fields = ['resource_owner_key', 'resource_owner_secret', 'verifier']
        if self.env.uid != SUPERUSER_ID and set(protected_fields).intersection(field_names):
            for record in self:
                for field in protected_fields:
                    try:
                        record._cache[field]
                        record._cache[field] = '****************'
                    except:
                        pass