#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 10/12/2012

@author: INFRA-PC1
'''

from handlers.base import Base
from core import Core 

class Designer(Core):
    def start(self): 
        self.core = Core()
        self.db = self.core.db()
        self.auth = self.core.auth
        