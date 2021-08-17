# -*- coding: utf-8 -*-

import os
import json
import urllib
import logging
import requests
import unittest

import requests

from odoo import _, SUPERUSER_ID
from odoo.tests import common

from odoo.addons.muk_rest import validators, tools
from odoo.addons.muk_rest.tests.common import active_authentication, RestfulCase

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

class CreateTestCase(RestfulCase):
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_create(self):
        client = self.authenticate()
        values = json.dumps({'name': 'Restful Partner'})
        response = client.post(self.create_url, data={'model': 'res.partner', 'values': values})
        tester = self.env['res.partner'].browse(response.json()).name
        self.assertTrue(response)
        self.assertEquals('Restful Partner', tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_create_multi(self):
        client = self.authenticate()
        values = json.dumps([{'name': 'Restful Partner'}, {'name': 'Restful Partner'}, {'name': 'Restful Partner'}])
        response = client.post(self.create_url, data={'model': 'res.partner', 'values': values})
        tester = self.env['res.partner'].browse(response.json()).mapped('name')
        self.assertTrue(response)
        self.assertTrue(len(tester) == 3)
        self.assertTrue('Restful Partner' in tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_create_many2many(self):
        client = self.authenticate()
        values = json.dumps({'name': 'Restful Partner', 'category_id': [[0, 0, {'name': 'Restful Category'}]]})
        response = client.post(self.create_url, data={'model': 'res.partner', 'values': values})
        tester = self.env['res.partner'].browse(response.json()).category_id.name
        self.assertTrue(response)
        self.assertEquals('Restful Category', tester)