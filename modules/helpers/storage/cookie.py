#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 21/11/2012

@author: INFRA-PC1
'''

from helpers import get_key
from helpers.storage.base import BaseStorage

from gluon.contrib import simplejson as json
from gluon.utils import simple_hash

class CookieManipulated(Exception):
    pass

class CookieStorage(BaseStorage):
    encoder = json.JSONEncoder(separators=(',', ':'))
    
    def __init__(self, *args, **kwargs):
        super(CookieStorage, self).__init__(*args, **kwargs)
        self.data = self.load_data()
        if self.data is None:
            self.init_data()
            
    def unsign_cookie_data(self, data):
        if data is None:
            return None
        
        bits = data.split('$', 1)
        if len(bits) == 2:
            if bits[0] == self.get_cookie_hash(bits[1]):
                return bits[1]
            
        raise CookieManipulated('Storage cookie manipulated')
    
    def load_data(self):
        data = self.request.cookies[self.prefix]
        cookie_data = self.unsign_cookie_data(data)
        if cookie_data is None:
            return None
        return json.loads(cookie_data, cls=json.JSONDecoder)
        
    def update_response(self, response):
        if self.data:
            response.cookies[self.prefix] = self.create_cookie_data(self.data)
        else:
            del response.cookies[self.prefix]
        return response
    
    def create_cookie_data(self, data):
        encoded_data = self.encoder.encode(self.data)
        cookie_data = '%s$%s' % (self.get_cookie_hash(encoded_data), encoded_data)
        return cookie_data
    
    def get_cookie_hash(self, data):
        return simple_hash('%s$%s'%(get_key(), data))