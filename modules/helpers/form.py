#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 28/12/2012

@author: INFRA-PC1
'''

from gluon import current
from gluon.html import *
from core import Core
from helpers.widgets import widgets

__all__ = ['DocForm', 'DocSet', 'DocList', 'DocTree']

def pretty_help(string):
    if len(string or '') <= 30:
        return SPAN(string or '', _class='help-block') 
    else:
        return SPAN(
            A(
              I(_class='icon-exclamation-sign'),
              **{
                 '_data-animation': 'true',
                 '_data-placement': 'top',
                 '_data-trigger': 'hover',
                 '_data-content': string or ''
                }
            ),
            _class='help-block'
        )

class DocForm(FORM):
    T = current.T
    request = current.request
    response = current.response
    session = current.session
    def __init__(self, 
                 document,
                 **kwargs):
        self.document = document
        self.db = Core().db()
        
        FORM.__init__(self, *[], **kwargs)
        
        elements = self.formstyle_document()
        
        self.components = [elements]
        
    def _formstyle_document_section_break(self, widget, i):
        _type = self.document.META.DOC_FIELDS[i].df_type
        while i < len(self.document.META.DOC_FIELDS) and _type != 'sectionbreak':
            doc_field = self.document.META.DOC_FIELDS[i] 
            df_name = doc_field.df_name
            subwidget = widgets[_type].widget(self.document.META.DOC_FIELDS[i], 
                                              self.document[df_name] if hasattr(self.document, df_name) else '' , 
                                              row=self.document)
            if doc_field.property('policy', 'visible') == 'NEVER':
                i += 1
                continue    
            elif _type == 'columnbreak':
                subwidget, i = self._formstyle_document_column_break(subwidget, i+1)
            widget.components.append(subwidget)
            if (i+1) >= len(self.document.META.DOC_FIELDS) or self.document.META.DOC_FIELDS[i+1].df_type == 'sectionbreak': 
                break
            else:
                i += 1
                _type = self.document.META.DOC_FIELDS[i].df_type
        return widget, i
    
    def _formstyle_document_column_break(self, widget, i):
        _type = _type = self.document.META.DOC_FIELDS[i].df_type
        while i < len(self.document.META.DOC_FIELDS) and _type not in ('sectionbreak', 'columnbreak'):
            doc_field = self.document.META.DOC_FIELDS[i] 
            df_name = doc_field.df_name
            subwidget = widgets[_type].widget(self.document.META.DOC_FIELDS[i], 
                                              self.document[df_name] if hasattr(self.document, df_name) else '', 
                                              row=self.document)
            widget.components.append(subwidget)
            if doc_field.property('policy', 'visible') == 'NEVER':
                i += 1
                continue
            elif (i+1) >= len(self.document.META.DOC_FIELDS) or self.document.META.DOC_FIELDS[i+1].df_type in ('sectionbreak', 'columnbreak') : 
                break
            else:
                i += 1
                _type = self.document.META.DOC_FIELDS[i].df_type
        return widget, i
        
    def formstyle_document(self):
        i = 0
        element = TAG['']()
        
        while i < len(self.document.META.DOC_FIELDS):
            doc_field = self.document.META.DOC_FIELDS[i] 
            _type = doc_field.df_type
            df_name = doc_field.df_name
            wgt = widgets[_type].widget(self.document.META.DOC_FIELDS[i], 
                                        self.document[df_name] if hasattr(self.document, df_name) else '', 
                                        row=self.document )
            if doc_field.property('policy', 'visible') == 'NEVER':
                i += 1
                continue
            elif _type == 'sectionbreak':
                subwgt, i = self._formstyle_document_section_break(wgt, i+1)
                i += 1
                element.components.append(subwgt)
                continue
            elif _type == 'columnbrek':
                subwgt, i = self._formstyle_document_column_break(wgt, i+1)
                i += 1
                element.components.append(subwgt)
                continue
            else:
                element.components.append(wgt)  
            i += 1
        
        return element
    
class DocSet(FORM):
    
    T = current.T
    request = current.request
    response = current.response
    session = current.session
    
    TOTAL_DOCUMENT_COUNT = 'TOTAL_DOCUMENTS'
    INITIAL_DOCUMENT_COUNT = 'INITIAL_DOCUMENTS'
    TEMPLATE = 'TEMPLATE'
    DELETION_FIELD_NAME = 'DELETE'
    
    def __init__(self, document, docset, extra=4, *args, **kwargs):
        
        if not 'hidden' in kwargs:
            kwargs['hidden'] = self._get_hidden_fields()
            
        FORM.__init__(self, *args, **kwargs)
        
        self.document = document
        self.docset = docset
        self.db = Core().db()
        
        self.extra = extra
        
        self._template_fields = filter(lambda df: df.type not in ('sectionbreak', 'columnbreak') or \
                                       df.property('visibility', 'is_writable')!='NEVER', self.document.META.DOCFIELDS)
        
        self._cols = self.document.property('type', 'listable_columns') or \
            [df.df_name for df in filter(lambda x: x.property('policy','is_readable')=='ALWAYS', self.DOCUMENT.META.DOCFIELDS)]
        self._cols = [filter(lambda x: x.df_name == column, self.document.META.DOC_FIELDS)[0] for column in self._cols]
        self._head = TR([TH()]+[TH(df.df_title, **{'_data-metatype': df.df_type}) for df in self._cols])
        
        components = [self._head, self._construct_documents()]
        for i in xrange(self.extra):
            components.append(self._get_empty_document((self.get_total_document_count()-self.extra)+i))
        self.components = [components]
        
    def _get_hidden_fields(self):
        from gluon.dal import Field
        hidden = [
            Field(self.TOTAL_DOCUMENT_COUNT, 'integer', default=self.get_total_document_count(), required=True),
            Field(self.INITIAL_DOCUMENT_COUNT, 'integer', default=self.get_initial_document_count(), required=True),
            Field(self.TEMPLATE, 'text', required=True, default=self._template_document())
        ]
        return hidden
    
    def __iter__(self):
        return iter(self.documents)
    
    def __getitem__(self, index):
        return self.documents[index]
    
    def __len__(self):
        return len(self.documents)
    
    def __nonzero__(self):
        return True
    
    def _template_document(self):
        template = TR(*[TD(widgets[df.df_type].widget(df, 
                            '' , 
                            row=self.document)) for df in self._template_fields])
        for element in template.elements('_name*=[_]'):
            element['_name']+='_{id}'
        return template.xml()
    
    def get_total_document_count(self):
        return int(self.vars[self.TOTAL_DOCUMENT_COUNT] or 0) + self.extra
    
    def get_initial_document_count(self):
        return self.vars[self.INITIAL_DOCUMENT_COUNT] or len(self.docset)
    
    def _construct_documents(self):
        self.forms = []
        for i in xrange(self.get_total_document_count()):
            self.forms.append(self._contruct_form(i))
            
    def _construct_document(self, i, **kwargs):
        from gluon.dal import Field
        document = TR(*[TD(widgets[df.df_type].widget(df, 
                            self.docset[i][df.df_name] if hasattr(self.docset[i], df.df_name) else '' , 
                            row=self.document)) for df in self._template_fields] + \
                      [TD(Field(self.DELETION_FIELD_NAME + '_%d'%i, 'boolean', default=False))])
        for element in document.elements('_name*=[_]'):
            element['_name']+='_%d'%i
            
        return document
    
    def _get_empty_document(self, i, **kwargs):
        emptydoc = self.db.get_document(self.document.doc_name)
        document = TR(*[TD(widgets[df.df_type].widget(df, 
                            emptydoc[df.df_name] if hasattr(emptydoc, df.df_name) else '' , 
                            row=self.document)) for df in self._template_fields])
        for element in document.elements('_name*=[_]'):
            element['_name']+='_%d'%i
        return document
    
    def process(self, **kwargs):
        for i in xrange(self.get_total_document_count()):
            self.process_one(i, **kwargs)
    
    def process_one(self, index, **kwargs):
        pass
    
class DocTable(TABLE):
    
    T = current.T
    request = current.request
    response = current.response
    session = current.session
    
    def __init__(self, document, docset, *args, **kwargs):
        TABLE.__init__(self, *args, **kwargs)
        
        self.document = document
        self.docset = docset
        
        self.attributes['_class'] = 'table Documents'
        
        self._cols = self.document.property('type', 'listable_columns') or \
            [df.df_name for df in filter(lambda x: x.property('policy','is_readable')=='ALWAYS', self.DOCUMENT.META.DOCFIELDS)]
        self._cols = [filter(lambda x: x.df_name == column, self.document.META.DOC_FIELDS)[0] for column in self._cols]
        self._head = TR([TH()]+[TH(df.df_title, **{'_data-metatype': df.df_type}) for df in self._cols])
        self._cells = [TR(TD('%06d'%doc.id), *[TD(doc[df.df_name] for df in self._cols)]) for doc in self.docset]
        
        self.components = [self._head, self._cells]
        
class DT(UL):
    tag = 'dt'

class DL(LI):
    tag = 'dl'
    
class DD(LI):
    tag = 'dd'
        
class DocList(DT):
    
    T = current.T
    request = current.request
    response = current.response
    session = current.session
    
    def __init__(self, document, docset, *args, **kwargs):
        DT.__init__(self, *args, **kwargs)
        
        self.document = document
        self.docset = docset
        
        self.attributes['_class'] = 'list Documents'
        
        elements = []
        for row in self.docset:
            elements.append(DL('06d'%row.id))
            elements.append(DD(row))
            
        self.elements = [elements]
        
class DocTree(OL):
    def __init__(self, document, docset, *args, **kwargs):
        OL.__init__(self, *args, **kwargs)
        
        self.document = document
        self.docset = docset
        
    @classmethod    
    def build_levels(cls, docset):
        pass