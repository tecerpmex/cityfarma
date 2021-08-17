# -*- coding: utf-8 -*-

import logging

from odoo import _, models, api, fields, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class AuthorizationCode(models.Model):
    
    _name = 'muk_rest.authorization_code'
    _description = "OAuth2 Authorization Code"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    code = fields.Char(
        string="Code",
        required=True,
        readonly=True)
    
    state = fields.Char(
        string="State",
        readonly=True)

    callback = fields.Char(
        string="Callback",
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
    
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    def _read_from_database(self, field_names, inherited_field_names=[]):
        super(AuthorizationCode, self)._read_from_database(field_names, inherited_field_names)
        protected_fields = ['code', 'state']
        if self.env.uid != SUPERUSER_ID and set(protected_fields).intersection(field_names):
            for record in self:
                for field in protected_fields:
                    try:
                        record._cache[field]
                        record._cache[field] = '****************'
                    except:
                        pass
