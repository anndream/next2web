#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 21/11/2012

@author: INFRA-PC1
'''

from gluon.storage import Storage
from helpers.storage.base import BaseStorage
from helpers.storage.cookie import CookieStorage
from helpers.storage.session import SessionStorage

storage = Storage({'session': StorageSession, 'cookie': StorageCookie})