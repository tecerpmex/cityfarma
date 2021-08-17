# -*- coding: utf-8 -*-#

import logging

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotImplemented

from odoo import _

_logger = logging.getLogger(__name__)

class NoDatabaseFound(BadRequest):
    
    description = _("No database could be matched to the request.")
    
    
class ModuleNotInstalled(NotImplemented):
    
    description = _("The request is not supported by this database.")
    
    
class LibraryNotInstalled(NotImplemented):

    description = _("The request is not supported by this database.")