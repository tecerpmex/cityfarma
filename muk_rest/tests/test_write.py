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

class WriteTestCase(RestfulCase):
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_write(self):
        client = self.authenticate()
        ids = json.dumps([2])
        values = json.dumps({'name': 'Restful Partner'})
        response = client.put(self.write_url, data={'model': 'res.partner', 'ids': ids, 'values': values})
        tester = self.env['res.partner'].browse([2]).name
        self.assertTrue(response)
        self.assertEquals('Restful Partner', tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_write_multi(self):
        client = self.authenticate()
        ids = json.dumps([1, 2])
        values = json.dumps({'name': 'Restful Partner'})
        response = client.put(self.write_url, data={'model': 'res.partner', 'ids': ids, 'values': values})
        tester = self.env['res.partner'].browse([1, 2]).mapped('name')
        self.assertTrue(response)
        self.assertTrue(len(tester) == 2)
        self.assertTrue('Restful Partner' in tester)
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_write_many2many(self):
        client = self.authenticate()
        ids = json.dumps([2])
        values = json.dumps({'name': 'Restful Partner', 'category_id': [[0, 0, {'name': 'Restful Category'}]]})
        response = client.put(self.write_url, data={'model': 'res.partner', 'ids': ids, 'values': values})
        tester = self.env['res.partner'].browse([2]).category_id.name
        self.assertTrue(response)
        self.assertEquals('Restful Category', tester)
    
    