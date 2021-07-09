# -*- coding: utf-8 -*-

import base64
import urllib

from werkzeug.datastructures import CombinedMultiDict


def decode_http_basic_authentication_value(value):
    try:
        username, password = base64.b64decode(value).decode().split(":", 1)
        return urllib.parse.unquote(username), urllib.parse.unquote(password)
    except:
        return None, None


def decode_http_basic_authentication(encoded_header):
    header_values = encoded_header.strip().split(" ")
    if len(header_values) == 1:
        return decode_http_basic_authentication_value(header_values[0])
    if len(header_values) == 2 and header_values[0].strip().lower() == "basic":
        return decode_http_basic_authentication_value(header_values[1])
    return None, None


def request_params(httprequest):
    return CombinedMultiDict([httprequest.args, httprequest.form, httprequest.files])
