#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 17/12/2012

@author: INFRA-PC1
'''

from base import BaseManager
from gluon import current
from gluon.http import HTTP
from gluon.compileapp import LOAD
from helpers import message
from core import Core
from helpers.storage.session import SessionStorage
from helpers.document import types

T = current.T

class QueryManager(BaseManager):
    AGGREGATORS = (('and', T('And')), ('or', T('Or')))
    def __init__(self, document, document_id):
        self.db = Core().db()
        self.document = self.db.get_document(document, document_id)
        self.__storage = SessionStorage()
        self.key = self.__class__.__name__
        
        BaseManager.__init__(self.db, self.document, self.__storage, self.key)
        
    def callback(self):
        
    def list_fields(self):
        return [{'name': f.df_name, 'label':f.df_title, 'operators': types[f.df_type].operators } for f in self.document.META.DOC_FIELDS]
                
    def query_builder(self):
        from pickle import loads