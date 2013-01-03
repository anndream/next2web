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
from helpers.document import types
from gluon.contrib.simplejson import loads

T = current.T

class QueryManager(BaseManager):
    AGGREGATORS = (('and', T('And')), ('or', T('Or')))
    def __init__(self, db, document, storager, part_name=None):
        if not part_name:
            part_name = self.__class__.__name__
        BaseManager.__init__(self.db, self.document, storager, part_name)
        
        self.T = current.T
        self.db = db
        self.document = document
        self.storager = self.storager
        self.request = current.request
        self.response = current.response
        
        self._id = '%s_%s' %(self.document.META.doc_name, self._part_name)
        self._name = '%s_for_%s_'%(self._part_name, self._id)
        
        self.base_url_fields = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_query_fields': self.document.doc_name, '__action': 'fields'})
        
    def callback(self):
        if '__document_query_fields' in self.request.var and self.request.vars['__document_query_fields'] == self.document.doc_name:
            if '__action' in self.request.vars and self.request.vars['__action'] == 'fields':
                raise HTTP(200, self.list_fields())
        
    def list_fields(self):
        return [{'name': f.df_name, 'label':f.df_title, 'operators': types[f.df_type].operators } for f in self.document.META.DOC_FIELDS]
                
    def query_builder(self):
        query = None;
        conditions = loads(self.request.vars.query)
        
        