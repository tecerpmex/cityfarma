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

class SearchTestCase(RestfulCase):
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_search(self):
        client = self.authenticate()
        tester = self.json_prepare(self.env['res.partner'].search([]).ids)
        response = client.get(self.search_url, data={'model': 'res.partner'})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_search_count(self):
        client = self.authenticate()
        tester = self.json_prepare(self.env['res.partner'].search([], count=True))
        response = client.get(self.search_url, data={'model': 'res.partner', 'count': True})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_search_domain_simple(self):
        client = self.authenticate()
        domain = [['id', '=', 1]]
        tester = self.json_prepare(self.env['res.partner'].search(domain, count=True))
        domain = json.dumps(domain)
        response = client.get(self.search_url, data={'model': 'res.partner', 'domain': domain, 'count': True})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_search_domain_complex(self):
        client = self.authenticate()
        domain = ['&', ['id', '=', 1], '|', ['category_id', 'child_of', [1]], ['category_id.name', 'ilike', "%"]]
        tester = self.json_prepare(self.env['res.partner'].search(domain, count=True))
        domain = json.dumps(domain)
        response = client.get(self.search_url, data={'model': 'res.partner', 'domain': domain, 'count': True})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_search_domain_context(self):
        client = self.authenticate()
        tester = self.json_prepare(self.env['res.partner'].with_context(bin_size=True).search([], count=True))
        context = json.dumps({'bin_size': True})
        response = client.get(self.search_url, data={'model': 'res.partner', 'context': context, 'count': True})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_search_limit(self):
        client = self.authenticate()
        tester = self.json_prepare(self.env['res.partner'].search([], count=True, limit=1))
        response = client.get(self.search_url, data={'model': 'res.partner', 'count': True, 'limit': 1})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_search_offset(self):
        client = self.authenticate()
        tester = self.json_prepare(self.env['res.partner'].search([], count=True, offset=1))
        response = client.get(self.search_url, data={'model': 'res.partner', 'count': True, 'offset': 1})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_search_order(self):
        client = self.authenticate()
        tester = self.json_prepare(self.env['res.partner'].search([], count=True, order='name desc'))
        response = client.get(self.search_url, data={'model': 'res.partner', 'count': True, 'oder': 'name desc'})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)