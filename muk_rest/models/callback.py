# -*- coding: utf-8 -*-

import logging

from odoo import _, models, api, fields

_logger = logging.getLogger(__name__)

class Callback(models.Model):
    
    _name = 'muk_rest.callback'
    _description = "Callback"
    
    _rec_name = 'url'
    _order = 'sequence'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    url = fields.Char(
        string="Callback URL",
        required=True)
    
    sequence = fields.Integer(
        string='Sequence',
        required=True,
        default=5)
    
    oauth = fields.Many2one(
        comodel_name='muk_rest.oauth',
        string="OAuth Configuration",
        ondelete='cascade',
        required=True)