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
from odoo.addons.muk_utils.tools.security import generate_token

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

try:
    import oauthlib
    import requests_oauthlib
except ImportError:
    _logger.warning("The Python library requests_oauthlib is not installed, OAuth tests wont work.")
    requests_oauthlib = None

class SettingsTestCase(RestfulCase):
    
    def setUp(self):
        super(SettingsTestCase, self).setUp()
        self.oauth_settings_client_key = generate_token()
        self.oauth_settings_client_secret = generate_token()
        self.oatuh_settings_client = self.env['muk_rest.oauth2'].create({
            'name': "Settings Test",
            'client_id': self.oauth_settings_client_key,
            'client_secret': self.oauth_settings_client_secret,
            'state': 'password',
            'security': 'advanced',
            'rules': [(0, 0, {'model': self.ref('base.model_res_partner')})]})
        
    @unittest.skipIf(not requests_oauthlib, "Skipped because Requests-OAuthlib is not installed!")
    def test_oauth_valid(self):
        client = oauthlib.oauth2.LegacyApplicationClient(client_id=self.oauth_settings_client_key)
        oauth = requests_oauthlib.OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.oauth2_access_token_url,
            client_id=self.oauth_settings_client_key, 
            client_secret=self.oauth_settings_client_secret,
            username=self.login, password=self.password)
        response = oauth.get(self.search_url, data={'model': 'res.partner'})
        self.assertTrue(response)
        
    @unittest.skipIf(not requests_oauthlib, "Skipped because Requests-OAuthlib is not installed!")
    def test_oauth_invalid(self):
        client = oauthlib.oauth2.LegacyApplicationClient(client_id=self.oauth_settings_client_key)
        oauth = requests_oauthlib.OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.oauth2_access_token_url,
            client_id=self.oauth_settings_client_key, 
            client_secret=self.oauth_settings_client_secret,
            username=self.login, password=self.password)
        response = oauth.get(self.search_url, data={'model': 'res.users'})
        self.assertFalse(response)
        
    @unittest.skipIf(not requests_oauthlib, "Skipped because Requests-OAuthlib is not installed!")
    def test_oauth_operation(self):
        self.oatuh_settings_client.rules.write({'perm_read': False})
        client = oauthlib.oauth2.LegacyApplicationClient(client_id=self.oauth_settings_client_key)
        oauth = requests_oauthlib.OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.oauth2_access_token_url,
            client_id=self.oauth_settings_client_key, 
            client_secret=self.oauth_settings_client_secret,
            username=self.login, password=self.password)
        response = oauth.get(self.search_url, data={'model': 'res.partner'})
        self.assertFalse(response)
        