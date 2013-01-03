#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 09/11/2012

@author: INFRA-PC1
'''

import string

from handlers.document import Document
from helpers import message, command
from gluon import current
from helpers.document import types
from gluon.sqlhtml.SQLFORM import factory
from gluon.contrib.simplejson import dumps
from helpers.storage import SessionStorage

T = current.T

class Document(Document):
    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        self.storage = SessionStorage(prefix = "DocumentDesigner")

    @command
    def list_types(self):
        return dumps([{t: types[t].label} for t in types.keys()])

    @command
    def type_has_option(self, name):
        if not name in types:
            message('Value Error', 'Unknow type %s'%`name`)
        return dumps(types[name].has_key('options'))

    @command
    def make_options_form(self, df_name, typename):
        if not typename in types:
            message('Value Error', 'Unable to create a form for the type %s' % typename)
            return
        return factory(types[typename].options, name=df_name).process(self.request.post_vars)
    
    @command
    def is_form_options_valid(self, df_name, typename):
        form = self.make_options_form(df_name, typename)
        return dumps([False if form.errors else True, form.xml()])
    
    @command
    def save_form_options(self, df_name, typename):
        self.storage.set_data(df_name, self.make_field_properties(typename))
    
    def make_field_properties(self, typename):
        if not typename in types:
            message('Value Error', 'Unable to create properties for the type %s' % typename)
        props = []
        for f in types[typename].options or []:
            props.append({"group": "type", "property": f.name, "value": self.request.post_vars[f.name]})
        return props
    
    def autoname(self):
        alphabet = string.lowercase
        length = len(alphabet)
        result = self.document.last_name
        i = len(result)
        
        while (i >= 0):
            i -=1
            last = self.document.last_name[i]
            nxt, carry = "", False
        
            if str(last).isalpha():
                try:
                    index = alphabet.index(str(last))
                    nxt = alphabet[(index + 1) % length]
                    if (last == last.upper()):
                        nxt = nxt.upper()
                    carry = index + 1 >= length
                    if carry and i == 0:
                        added = 'A' if last == last.upper() else 'a'
                        result = added + nxt + result[1:]
                        break
                except ValueError:
                    nxt, carry = last, True
            else:
                nxt = int(last) + 1
                if nxt > 9:
                    nxt, carry = 0, True
                if carry and i == 0:
                    result = '1' + nxt + result[:1]
                    break;
            result = result[:i] + str(nxt) + result[i+1:]
            if not carry:
                break
        return result
        
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
        