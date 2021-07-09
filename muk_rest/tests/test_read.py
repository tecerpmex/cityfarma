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

class ReadTestCase(RestfulCase):
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_name(self):
        client = self.authenticate()
        ids = [1, 2]
        tester = self.json_prepare(self.env['res.partner'].browse(ids).name_get())
        ids = json.dumps(ids)
        response = client.get(self.name_url, data={'model': 'res.partner', 'ids': ids})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_read(self):
        client = self.authenticate()
        ids = [1]
        tester = self.json_prepare(self.env['res.partner'].browse(ids).read(fields=None))
        ids = json.dumps(ids)
        response = client.get(self.read_url, data={'model': 'res.partner', 'ids': ids})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_read_single(self):
        client = self.authenticate()
        ids = [1]
        fields = ['name']
        tester = self.json_prepare(self.env['res.partner'].browse(ids).read(fields=fields))
        ids = json.dumps(ids)
        fields = json.dumps(fields)
        response = client.get(self.read_url, data={'model': 'res.partner', 'ids': ids, 'fields': fields})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_read_multiple(self):
        client = self.authenticate()
        ids = [1, 2, 3]
        fields = ['name']
        tester = self.json_prepare(self.env['res.partner'].browse(ids).read(fields=fields))
        ids = json.dumps(ids)
        fields = json.dumps(fields)
        response = client.get(self.read_url, data={'model': 'res.partner', 'ids': ids, 'fields': fields})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_read_context(self):
        client = self.authenticate()
        ids = [1, 2, 3]
        fields = ['name', 'image_1024']
        tester = self.json_prepare(self.env['res.partner'].with_context(bin_size=True).browse(ids).read(fields=fields))
        ids = json.dumps(ids)
        fields = json.dumps(fields)
        context = json.dumps({'bin_size': True})
        response = client.get(self.read_url, data={'model': 'res.partner', 'ids': ids, 'fields': fields, 'context': context})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
    