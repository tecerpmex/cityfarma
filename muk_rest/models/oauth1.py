# -*- coding: utf-8 -*-

import logging

from odoo import _, models, api, fields
from odoo.exceptions import ValidationError

from odoo.addons.muk_utils.tools import security

_logger = logging.getLogger(__name__)

class OAuth1(models.Model):
    
    _name = 'muk_rest.oauth1'
    _description = "OAuth1 Configuration"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    oauth = fields.Many2one(
        comodel_name='muk_rest.oauth',
        string='OAuth',
        delegate=True,  
        required=True,
        ondelete='cascade')

    consumer_key = fields.Char(
        string="Consumer Key",
        required=True,
        default=lambda x: security.generate_token())
    
    consumer_secret = fields.Char(
        string="Consumer Secret",
        required=True,
        default=lambda x: security.generate_token())

    #----------------------------------------------------------
    # Constraints
    #----------------------------------------------------------
    
    _sql_constraints = [
        ('consumer_key_unique', 'UNIQUE (consumer_key)', 'Consumer Key must be unique.'),
        ('consumer_secret_unique', 'UNIQUE (consumer_secret)', 'Consumer Secret must be unique.'),
    ]
    
    @api.constrains('consumer_key')
    def check_consumer_key(self):
        for record in self:
            if not (20 < len(record.consumer_key) < 50):
                raise ValidationError(_("The consumer key must be between 20 and 50 characters long."))
            
    @api.constrains('consumer_secret')
    def check_consumer_secret(self):
        for record in self:
            if not (20 < len(record.consumer_secret) < 50):
                raise ValidationError(_("The consumer secret must be between 20 and 50 characters long."))
            
    #----------------------------------------------------------
    # Create / Update / Delete
    #----------------------------------------------------------

    def unlink(self):
        self.mapped('oauth').unlink()
        return super(OAuth1, self).unlink()