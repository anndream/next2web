#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 09/11/2012

@author: INFRA-PC1
'''

class Document(object):
    def __init__(self, document, doc_fields=[]):
        self.document = document
        self.doc_fields = doc_fields
        
    def pretty_field_names(self):
        restricted = ['doc_name', 'doc_parent', 'idx', 'created_by', 'created_on', 'modified_by', 'modified_on']
        for df in self.doc_fields:
            if df.doc_parent:
                if not df.df_name:
                    df.df_name = df.df_label.strip().lower().replace(' ', '_').replace('-', '_')
    
    def set_version(self):
        self.document.property('info', 'version', self.document.property('info', 'version')+1)
        
    def validate_doc_fields(self):
        import re
        fieldnames = {}
        illegal = re.compile("(?Lsu)([\w]+)?([\W]+)([\w]+)?")
        for df in self.doc_fields:
            if not df.property('security', 'level'):
                df.property('security', 'level', 0)