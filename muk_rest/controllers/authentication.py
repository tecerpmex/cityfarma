# -*- coding: utf-8 -*-

import re
import json
import urllib
import logging

from werkzeug import exceptions, utils

from odoo import _, http
from odoo.http import request, Response
from odoo.exceptions import AccessDenied
from odoo.tools import misc, config

from odoo.addons.muk_rest import validators, tools

_logger = logging.getLogger(__name__)
_csrf = config.get('rest_csrf', False)

class AuthenticationController(http.Controller):
    
    def __init__(self):
        super(AuthenticationController, self).__init__()
        self.oauth1 = validators.oauth1_provider
        self.oauth2 = validators.oauth2_provider

    #----------------------------------------------------------
    # OAuth Authorize
    #----------------------------------------------------------

    def client_information(self, client, values={}):
        values.update({
            'name': client.homepage,
            'company': client.company,
            'homepage': client.homepage,
            'logo_url': client.logo_url,
            'privacy_policy': client.privacy_policy,
            'service_terms': client.service_terms,
            'description': client.description,
        })
        return values
    
    def oauth1_information(self, token, realms=[], values={}):
        model = request.env['muk_rest.request_token'].sudo()
        domain = [('resource_owner_key', '=', token)]
        request_token = model.search(domain, limit=1)
        if token and request_token.exists():
            values = self.client_information(request_token.oauth, values)
            values.update({
                'oauth_token': request_token.resource_owner_key,
                'callback': request_token.callback,
                'realms': realms or [],
            })
            return values
        else:
            raise exceptions.BadRequest
        
    def oauth2_information(self, client_id, redirect_uri, response_type, state=None, scopes=[], values={}):
        model = request.env['muk_rest.oauth2'].sudo()
        domain = [('client_id', '=', client_id)]
        oauth = model.search(domain, limit=1)
        if client_id and redirect_uri and response_type and oauth.exists():
            values = self.client_information(oauth, values)
            values.update({
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'response_type': response_type,
                'state': state,
                'scopes': scopes or []
            })
            return values
        else:
            raise exceptions.BadRequest
        
    #----------------------------------------------------------
    # OAuth 1.0
    #----------------------------------------------------------

    @http.route('/api/authentication/oauth1/initiate', auth="none", type='http', methods=['POST'], csrf=_csrf)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.common.ensure_import()
    def oauth1_initiate(self, **kw):
        headers, body, status = self.oauth1.create_request_token_response(
            uri=request.httprequest.url,
            http_method=request.httprequest.method,
            body=request.httprequest.form,
            headers=request.httprequest.headers)
        return Response(response=body, headers=headers, status=status) 
    
    @http.route('/api/authentication/oauth1/authorize', auth="none", type='http', methods=['GET', 'POST'], csrf=_csrf)
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.common.ensure_import()
    def oauth1_authorize(self, **kw):
        try:
            if request.httprequest.method.upper() == 'GET':
                realms, credentials = self.oauth1.get_realms_and_credentials(
                    uri=request.httprequest.url,
                    http_method=request.httprequest.method,
                    body=request.httprequest.form,
                    headers=request.httprequest.headers)
                resource_owner_key = credentials.get('resource_owner_key', False)
                values = self.oauth1_information(resource_owner_key, realms)
                return request.render('muk_rest.authorize_oauth1', values)
            elif request.httprequest.method.upper() == 'POST':
                login = request.params.get('login', None)
                password = request.params.get('password', None)
                token = request.params.get('oauth_token')
                realms = request.httprequest.form.getlist('realms')
                try:
                    uid = request.session.authenticate(request.env.cr.dbname, login, password)
                    headers, body, status = self.oauth1.create_authorization_response(
                        uri=request.httprequest.url,
                        http_method=request.httprequest.method,
                        body=request.httprequest.form,
                        headers=request.httprequest.headers,
                        realms=realms or [],
                        credentials={'user': uid})
                    if status == 200:
                        verifier = str(urllib.parse.parse_qs(body)['oauth_verifier'][0])
                        content = json.dumps({'oauth_token': token, 'oauth_verifier': verifier}, sort_keys=True, indent=4)
                        return Response(content, content_type='application/json;charset=utf-8', status=200) 
                    else:
                        return Response(body, status=status, headers=headers)
                except AccessDenied:
                    values = self.oauth1_information(token, realms)
                    values.update({'error': _("Invalid login or password!")})
                    return request.render('muk_rest.authorize_oauth1', values)
        except exceptions.HTTPException as exc:
            _logger.exception("OAUth authorize failed!")
            return utils.redirect('/api/authentication/error', 302, exc)
        except:
            _logger.exception("OAUth authorize")    
            return utils.redirect('/api/authentication/error', 302)

    
    @http.route('/api/authentication/oauth1/token', auth="none", type='http', methods=['POST'], csrf=_csrf)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.common.ensure_import()
    def oauth1_token(self, **kw):
        headers, body, status = self.oauth1.create_access_token_response(
            uri=request.httprequest.url,
            http_method=request.httprequest.method,
            body=request.httprequest.form,
            headers=request.httprequest.headers)
        return Response(response=body, headers=headers, status=status) 
    
    #----------------------------------------------------------
    # OAuth 2.0
    #----------------------------------------------------------

    @http.route('/api/authentication/oauth2/authorize', auth="none", type='http', methods=['GET', 'POST'], csrf=_csrf)
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.common.ensure_import()
    def oauth2_authorize(self, **kw):
        try:
            if request.httprequest.method.upper() == 'GET':
                scopes, credentials = self.oauth2.validate_authorization_request(
                    uri=request.httprequest.url,
                    http_method=request.httprequest.method,
                    body=request.httprequest.form,
                    headers=request.httprequest.headers)
                client_id = credentials.get('client_id', False)
                redirect_uri = credentials.get('redirect_uri', False)
                response_type = credentials.get('response_type', False)
                state = credentials.get('state', False)
                values = self.oauth2_information(client_id, redirect_uri, response_type, state, scopes)
                return request.render('muk_rest.authorize_oauth2', values)
            elif request.httprequest.method.upper() == 'POST':
                login = request.params.get('login', None)
                password = request.params.get('password', None)
                client_id = request.params.get('client_id')
                redirect_uri = request.params.get('redirect_uri')
                response_type = request.params.get('response_type')
                state = request.params.get('state')
                scopes = request.httprequest.form.getlist('scopes')
                try:
                    uid = request.session.authenticate(request.env.cr.dbname, login, password)
                    headers, body, status = self.oauth2.create_authorization_response(
                        uri=request.httprequest.url,
                        http_method=request.httprequest.method,
                        body=request.httprequest.form,
                        headers=request.httprequest.headers,
                        scopes=scopes or ['all'],
                        credentials={'user': uid})
                    return Response(body, status=status, headers=headers)
                except AccessDenied:
                    values = self.oauth2_information(client_id, redirect_uri, response_type, state, scopes)
                    values.update({'error': _("Invalid login or password!")})
                    return request.render('muk_rest.authorize_oauth2', values)
        except exceptions.HTTPException as exc:
            _logger.exception("OAUth authorize")   
            return utils.redirect('/api/authentication/error', 302, exc)
        except:       
            _logger.exception("OAUth authorize")   
            return utils.redirect('/api/authentication/error', 302)
    
    @http.route('/api/authentication/oauth2/token', auth="none", type='http', methods=['POST'], csrf=False)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.common.ensure_import()
    def oauth2_token(self, **kw):
        headers, body, status = self.oauth2.create_token_response(
            uri=request.httprequest.url,
            http_method=request.httprequest.method,
            body=request.httprequest.form,
            headers=request.httprequest.headers)
        return Response(response=body, headers=headers, status=status) 
    
    @http.route('/api/authentication/oauth2/revoke', auth="none", type='http', methods=['POST'], csrf=_csrf)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.common.ensure_import()
    def oauth2_revoke(self, **kw):
        headers, body, status = self.oauth2.create_revocation_response(
            uri=request.httprequest.url,
            http_method=request.httprequest.method,
            body=request.httprequest.form,
            headers=request.httprequest.headers)
        request.session.logout()
        return Response(response=body, headers=headers, status=status) 
        
    @http.route('/api/authentication/error', auth="none", type='http', methods=['GET'])
    def oauth_error(self, **kw):
        return request.render('muk_rest.authorize_error')