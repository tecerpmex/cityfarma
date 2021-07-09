# -*- coding: utf-8 -*-

import logging

from odoo import models, api, fields

_logger = logging.getLogger(__name__)

class Request(models.Model):
    
    _name = 'muk_rest.request'
    _description = "Request"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    client_key = fields.Char(
        string="Client Key")
    
    timestamp = fields.Char(
        string="Timestamp")
    
    nonce = fields.Char(
        string="Nonce")
    
    token = fields.Char(
        string="Token")
   