#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 21/11/2012

@author: INFRA-PC1
'''

from gluon.storage import Storage
from base import BaseStorage
from cookie import CookieStorage
from session import SessionStorage

storage = Storage({'session': SessionStorage, 'cookie': CookieStorage})