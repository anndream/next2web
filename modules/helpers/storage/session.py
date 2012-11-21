#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 21/11/2012

@author: INFRA-PC1
'''

from helpers.storage.base import BaseStorage
from gluon import current

class SessionStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        super(SessionStorage, self).__init__(*args, **kwargs)
        if self.prefix not in self.request.session:
            self.init_data()
            
    def reset(self):
        current.session.modified = False
        self.init_data()
            
    def _get_data(self):
        current.session.modified = True
        return current.session[self.prefix]
    
    def _set_data(self, data):
        current.session[self.prefix] = data
        current.session.modified = True
    
    data = property(_get_data, _set_data)
        