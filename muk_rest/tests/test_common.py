# -*- coding: utf-8 -*-
import os
import json
import urllib
import shutil
import logging
import requests
import unittest
import tempfile

import requests

from odoo import _, SUPERUSER_ID
from odoo.tests import common

from odoo.addons.muk_utils.tools.json import RecordEncoder
from odoo.addons.muk_rest.tests.common import active_authentication, RestfulCase

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

class CommonTestCase(RestfulCase):
    
    def test_version(self):
        self.assertTrue(self.url_open(self.version_url))
        
    def test_database(self):
        self.assertTrue(self.url_open(self.database_url))
    
    def test_csrf_token(self):
        self.assertTrue(self.url_open(self.csrf_token_url))
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_user(self):
        client = self.authenticate()
        response = client.get(self.user_url)
        self.assertTrue(response)
        self.assertTrue(response.json().get('uid'))
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_userinfo(self):
        client = self.authenticate()
        response = client.get(self.userinfo_url)
        self.assertTrue(response)
        self.assertTrue(response.json().get('name'))
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_session(self):
        client = self.authenticate()
        response = client.get(self.session_url)
        self.assertTrue(response)
        self.assertTrue(response.json().get('login'))
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_call_kwargs(self):
        client = self.authenticate()
        fields_list = ['name']
        tester = self.json_prepare(self.env['res.partner'].default_get(fields_list), RecordEncoder)
        kwargs = json.dumps({'fields_list': fields_list})
        response = client.post(self.call_url, data={'model': 'res.partner', 'method': 'default_get', 'kwargs': kwargs})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_call_args(self):
        client = self.authenticate()
        fields_list = ['name']
        tester = self.json_prepare(self.env['res.partner'].default_get(fields_list), RecordEncoder)
        args = json.dumps([fields_list])
        response = client.post(self.call_url, data={'model': 'res.partner', 'method': 'default_get', 'args': args})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_call_ids(self):
        client = self.authenticate()
        ids = [1]
        tester = self.json_prepare(self.env['res.partner'].browse(ids).copy().name_get(), RecordEncoder)
        response = client.post(self.call_url, data={'model': 'res.partner', 'method': 'copy', 'ids': json.dumps(ids)})
        self.assertTrue(response)
        self.assertEquals(response.json()[0][1], tester[0][1])
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_xmlid(self):
        client = self.authenticate()
        tester = self.env.ref('base.group_user')
        response = client.get(self.xmlid_url, data={'xmlid': 'base.group_user'})
        self.assertTrue(response)
        self.assertTrue(response.json().get('model'))
        self.assertEquals(response.json().get('id'), tester.id)

    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_binary(self):
        client = self.authenticate()
        response = client.get(self.binary_url, data={'id': 1})
        self.assertTrue(response)
        self.assertTrue(response.json().get('content'))
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_binary_file(self):
        client = self.authenticate()
        response = client.get(self.binary_url, data={'id': 1, 'file_response': True})
        self.assertTrue(response)
        self.assertTrue(response.content)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_upload_file(self):
        client = self.authenticate()
        tmp_dir = tempfile.mkdtemp()
        filename = os.path.join(tmp_dir, "test.txt")
        try:
            with open(filename, "w") as file:
                file.write("Lorem ipsum!")
            with open(filename, "rb") as file:   
                files_01 = {'ufile': file}
                files_02 = {'ufile': file}
                data_01 = {'model': 'res.partner', 'id': 1}
                data_02 = {'model': 'ir.attachment', 'id': 1, 'field': 'datas'}
                response_01 = client.post(self.upload_url, files=files_01, data=data_01)
                response_02 = client.post(self.upload_url, files=files_02, data=data_02)
                self.assertTrue(response_01)
                self.assertTrue(response_02)
        finally:
            shutil.rmtree(tmp_dir)
            
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_upload_files(self):
        client = self.authenticate()
        tmp_dir = tempfile.mkdtemp()
        filename = os.path.join(tmp_dir, "test.txt")
        try:
            with open(filename, "w") as file:
                file.write("Lorem ipsum!")
            with open(filename, "rb") as file:  
                files = [('ufile', file), ('ufile', file)]
                data = {'model': 'res.partner', 'id': 1}
                response = client.post(self.upload_url, files=files, data=data)
                self.assertTrue(response)
        finally:
            shutil.rmtree(tmp_dir)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_reports(self):
        client = self.authenticate()
        response = client.get(self.reports_url)
        self.assertTrue(response)
        self.assertTrue(response.json())
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_report_single(self):
        client = self.authenticate()
        response = client.get(self.report_url, data={'report': 'base.report_irmodulereference', 'ids': json.dumps([1])})
        self.assertTrue(response)
        self.assertTrue(response.json().get('content'))
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_report_multiple(self):
        client = self.authenticate()
        response = client.get(self.report_url, data={'report': 'base.report_irmodulereference', 'ids': json.dumps([1, 2])})
        self.assertTrue(response)
        self.assertTrue(response.json().get('content'))
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_report_file(self):
        client = self.authenticate()
        data = {'report': 'base.report_irmodulereference', 'ids': json.dumps([1]), 'file_response': True}
        response = client.get(self.report_url, data=data)
        self.assertTrue(response)
        self.assertTrue(response.content)
