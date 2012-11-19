#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 17/10/2012

@author: INFRA-PC1
'''
from handlers.document import Document
from gluon.tools import Service

service = Service()

def index():
    doc = Document('add')
    return doc.render('document/index')

@service.json
def data():
    doc = Document()
    
    getattr(doc, doc.request.args.pop(0).split('.')[0])()
    return doc.render('generic.json')

def call():
    session.forget()
    return service()