# -*- coding: utf-8 -*-

import logging

from odoo import _, models, api, fields

_logger = logging.getLogger(__name__)

class Access(models.Model):
    
    _name = 'muk_rest.access'
    _description = "Access Control"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    active = fields.Boolean(
        string="Active",
        default=True)
    
    model = fields.Many2one(
        comodel_name='ir.model',
        string="Model", 
        index=True, 
        required=True, 
        ondelete='cascade',
        domain=[('transient', '=', False)])
    
    perm_read = fields.Boolean(
        string='Read Access',
        default=True)
    
    perm_write = fields.Boolean(
        string='Write Access',
        default=True)
    
    perm_create = fields.Boolean(
        string='Create Access',
        default=True)
    
    perm_unlink = fields.Boolean(
        string='Delete Access',
        default=True)
    
    oauth = fields.Many2one(
        comodel_name='muk_rest.oauth',
        string="OAuth Configuration",
        required=True, 
        ondelete='cascade')
    