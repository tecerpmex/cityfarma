# -*- coding: utf-8 -*-

import logging
import datetime

from odoo import models, fields

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    
    _inherit = 'res.users'

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    oauth1_sessions = fields.Integer(
        compute='_compute_oauth1_sessions',
        string="OAuth1 Sessions")
    
    oauth2_sessions = fields.Integer(
        compute='_compute_oauth2_sessions',
        string="OAuth2 Sessions")
    
    #----------------------------------------------------------
    # Framework
    #----------------------------------------------------------
    
    # def __init__(self, pool, cr):
    #     init_result = super(ResUsers, self).__init__(pool, cr)
    #     oauth_fields = ['oauth1_sessions', 'oauth2_sessions']
    #     type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
    #     type(self).SELF_READABLE_FIELDS.extend(oauth_fields)
    #     return init_result

    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    def _compute_oauth1_sessions(self):
        for record in self:
            model = self.env['muk_rest.access_token']
            domain = [('user', '=', self.env.uid)]
            record.oauth1_sessions = model.search(domain, count=True)
            
    def _compute_oauth2_sessions(self):
        for record in self:
            model = self.env['muk_rest.bearer_token']
            domain = [
                '&', ('user', '=', self.env.uid),
                '|', ('expires_in', '=', False), ('expires_in', '>', datetime.datetime.utcnow())
            ]
            record.oauth2_sessions = model.search(domain, count=True)