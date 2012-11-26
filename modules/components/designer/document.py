#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 09/11/2012

@author: INFRA-PC1
'''

from core import DocumentData, register_adapter
from helpers.storage import storage

class Document(DocumentData):
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.childs = storage.cookie(prefix=self.META.doc_name)
        
                
register_adapter('document', Document)
        