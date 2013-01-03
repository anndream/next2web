#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 17/10/2012

@author: INFRA-PC1
'''
from handlers.document import Document
from gluon.tools import Service
from helpers import message
from core import Core
from gluon.http import HTTP
service = Service()

def index():
    doc = Document('create')
    return doc.render('document/index')

def command():
    doc = Document()
    if not request.args or len(request.args)<=2:
        message('Value Error', 'Command requires an function name')
    fn = request.args[2]
    if not hasattr(doc, fn):
        message('Document Command Error', 'Unable to find a command with name %s'%fn)
    return getattr(doc, fn)(request.args[3:])

@request.restful()
def api():
    response.view = 'generic.' + request.extension
    db = Core().db()
    def GET(*args, **kwargs):
        patterns = [
            '/document[document]',
            '/document/{document.id}',
            '/document/{document.id}/:field',
            '/document/fields[documentfield]/doc-parent/{documentfield.doc_parent}/doc-parent-id/{documentfield.doc_parent_id}',
            '/field[documentfield]',
            '/field/{documentfield.id}',
            '/field/{documentfield.id}/:field'
            '/field/doc-parent/{documentfield.doc_parent}/doc-parent-id/{documentfield.doc_parent_id}'
        ]
        parse = db.parse_as_rest(patterns, args, kwargs)
        if parse.status == 200:
            return dict(content=parse.response)
        else:
            raise HTTP(parse.status, parse.error)
        
    def POST(doc_name, **vars):
        return db[doc_name].validate_and_insert(**vars)
    
    def PUT(doc_name, record_id, **vars):
        return db(db[doc_name]._id==record_id).update(**vars)
    
    def DELETE(doc_name, record_id):
        return db(db[doc_name]._id==record_id).delete()
    
    return {'GET': GET, 'POST': POST, 'PUT': PUT, 'DELETE': DELETE}

@service.json
def data():
    doc = Document()
    
    getattr(doc, doc.request.args.pop(0).split('.')[0])()
    return doc.render('generic.json')

def call():
    session.forget()
    return service()