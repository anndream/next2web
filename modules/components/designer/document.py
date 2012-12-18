#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 09/11/2012

@author: INFRA-PC1
'''

import string

from handlers.document import Document
from helpers import message
from gluon import current

T = current.T

class Document(Document):
    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        
    def autoname(self):
        alphabet = string.lowercase
        
        
    def _validate_doc_name(self, case='Title Case'):
        db = self.META._db
        if db.has_document(self.doc_name):
            message('Document already exists', 'The Document %s already exists in database'%self.doc_name)
        
        if case == 'Title Case': self.doc_name = self.doc_name.title()
        if case == 'UPPER CASE': self.doc_name = self.doc_name.upper()
        
        self.doc_name = self.doc_name.strip()
        
        errors = []
        forbidden = ['%', '"', "'", "#", "*","?", "`", "&", "-", ":"]
        for f in forbidden:
            if f in self.name:
                errors.append((True, str(T("%s not allowed in Document Name"))%f))
                errors = True
        return errors or (None, '')
    
    def _validate_doc_tablename(self):
        db = self.META._db
        errors = False
        if db(db.Document.doc_tablename==self.doc_tablename).count()>0:
            errors.append((True, str(T('Table name %s already exists'))%self.doc_tablename))
        return errors or (None, '')
    
    def clear_table(self, childname):
        pass
        