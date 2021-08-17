# -*- coding: utf-8 -*-

from odoo import api, models


class IrConfigParameter(models.Model):

    _inherit = "ir.config_parameter"

    @api.model
    def set_params(self, params):
        for key, value in params.items():
            self.set_param(key, value)
