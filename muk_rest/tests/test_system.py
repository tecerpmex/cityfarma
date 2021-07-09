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
from odoo.addons.muk_rest.tests.common import RestfulCase
from odoo.addons.muk_rest.tests.common import MASTER_PASSWORD, LOGIN, PASSWORD, DISABLE_DATABASE_TESTS

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

class SystemTestCase(RestfulCase):
    
    def test_languages(self):
        response = self.url_open(self.url_prepare('/api/languages'))
        self.assertTrue(response)
        
    def test_countries(self):
        response = self.url_open(self.url_prepare('/api/countries'))
        self.assertTrue(response)
    
    def test_modules(self):
        response = self.url_open(self.url_prepare('/api/modules'))
        self.assertTrue(response)
        
    @unittest.skipIf(DISABLE_DATABASE_TESTS, "Skipped to avoid side effects on the server.")
    def test_change_password(self):
        response = self.url_open(self.url_prepare('/api/change_master_password'), 
            data={'password_old': MASTER_PASSWORD, 'password_new': "new_pw"})
        self.assertTrue(response)
        response = requests.post(self.url_prepare('/api/change_master_password'),
            data = {'password_old': "new_pw", 'password_new': MASTER_PASSWORD})
        self.assertTrue(response)