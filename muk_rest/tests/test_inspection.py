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

class CommonTestCase(RestfulCase):
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_field_names(self):
        client = self.authenticate()
        tester = self.json_prepare(self.env['res.partner'].fields_get_keys())
        response = client.get(self.field_names_url, data={'model': 'res.partner'})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_fields(self):
        client = self.authenticate()
        tester = self.json_prepare(self.env['res.partner'].fields_get())
        response = client.get(self.fields_url, data={'model': 'res.partner'})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_fields_attributes(self):
        client = self.authenticate()
        fields = ['name']
        attributes = ['string', 'help', 'type']
        tester = self.json_prepare(self.env['res.partner'].fields_get(allfields=fields, attributes=attributes))
        fields = json.dumps(fields)
        attributes = json.dumps(attributes)
        response = client.get(self.fields_url, data={'model': 'res.partner', 'fields': fields, 'attributes': attributes})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_metadata(self):
        client = self.authenticate()
        ids = [1, 2]
        tester = self.json_prepare(self.env['res.partner'].browse(ids).get_metadata())
        ids = json.dumps(ids)
        response = client.get(self.metadata_url, data={'model': 'res.partner', 'ids': ids})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)