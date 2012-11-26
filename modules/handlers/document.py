#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 02/10/2012

@author: INFRA-PC1
'''
import os

from handlers.base import Base
from gluon.storage import Storage
from helpers.widgets import Document as FORM

from core import Core

class Document(Base):
    def start(self):
        self.core = Core()
        self.db = self.core.db()
        self.auth = self.context.auth = self.core.auth
        self.session = self.core.session
        self.db._check_update('document', 'designer')
        
    def get(self):
        self.context.document = self.db.get_document(*self.request.args[:2])
        if len(self.request.args)>1 and not self.session.document[self.request.args[1]]:
            self.session.document[self.request.args[1]] = Storage()
             
    def add(self):
        self.get()
        self.context.form = FORM(self.context.document)
        
    def edit(self):
        self.get()
        self.context.form = FORM(self.context.document)

    def delete(self):
        self.db.send_to_trash(self.request.args[0], self.request.args[1])
        
    def show(self):
        self.get()
        self.context.form = FORM(self.context.document, readonly=True)
