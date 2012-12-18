#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 12/12/2012

@author: INFRA-PC1
'''

from helpers.storage.base import BaseStorage
from gluon import current
from gluon.html import URL

class URLDispatch(object):
    storage = BaseStorage(prefix='url_dispach')
    current_url = URL(r=current.request, c=current.controller, f=current.function, args=current.args, vars=current.vars)
    
    