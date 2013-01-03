#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 03/01/2013

@author: INFRA-PC1
'''

from gluon import current, validators
from gluon.html import *
from core import Core
from helpers.document import types

T = current.T

class VirtualWidget(object):
    _class = 'virtual-generic-widget'
    def __init__(self, df, widget, value, **attributes):
        
        self.db = df.PARENT._db
        self.docfield = df
        self.other = widget
        self.value = self.filter_in(value)
        self.attributes = attributes
        
    def widget(self, value, **attrs):
        raise NotImplementedError
    
    def validate(self, value):
        return True
    
    def filter_in(self, value):
        self.value = value
    
    def filter_out(self):
        return self.value
    
class Query(object):
    _class = 'query-widget'
    
    AGREGATORS = (('and', T('and')),
                  ('or', T('or')))
    
    def __init__(self, docfield, target, target_label, **attributes):
        self.db = docfield.PARENT._db
        self.doc_field = docfield
        
        self.document = self.db.get_document(self.doc_field.property('type', 'document'))
        
        self.attributes = attributes
        self.target = target
        self.target_label = target_label
    
    def widget(self):
        self.attributes['_data-query_options'] = self._build_options()
        self.attributes['_data-query_template_condition'] = self._build_condition_row_template()
        self.attributes['_data-query_template_result'] = self._build_results_row_template()
        self.attributes['_data-query_dialog_template'] = self._build_dialog_template()
        self.attributes['_data-result_target'] = self.target
        self.attributes['_data-result-target_label'] = self.label
        
        data = {'_data-target':self.doc_field.df_name}
        
        btn = A(I(_class='icon-search'), _class='btn btn-mini document-search', _title=T('Search'), _id='search', **data),
        
        return btn
        
    def _build_options(self):
        from pickle import dumps
        self.docfields = self.document.META.DOCFIELDS
        options = []
        for docfield in self.docfields:
            _type = docfield.df_type
            if _type in types and types[_type].has_key('operators') and len(types[_type].operators)>0:
                option = {docfield.df_name: docfield.df_label}
                operations = []
                for operation in types[_type].operators:
                    operator = {operation[0]: operation[1]}
                    operations.append(operator)
                option['operations'] = operations
                options.append(options)
        return dumps(options)
    
    def _build_condition_row_template(self):
        aggregator = SELECT(*[OPTION(o[1], _value=o[1]) for o in self.AGREGATORS], _name='aggregator', _class='query-expr-aggregator')
        docfield = SELECT(_name='doc_field', _class='query-expr-doc_field')
        condition = SELECT(_name='condition', _class='query-expr-condition')
        value = INPUT(_name='value', _class='query-expr-value')
        
        btn_add_expr = A(I(_class='icon-plus'), _class='btn btn-mini query-expr-add', _id='add_expre_{}', *{'_data-row': 'expression_{}'})
        btn_rem_expr = A(I(_class='icon-remove'), _class='btn btn-mini query-expre-rem', _id='rem_expre_{}', *{'_data-row': 'expression_{}'})
        
        container = DIV(
            aggregator,
            docfield,
            condition,
            value,
            btn_add_expr,
            btn_rem_expr,
            _id='%s_expression_{}'%self.docfield.df_name,
            _class='query-expression'
        )
        return container.xml()
        
    def _build_dialog_template(self):
        dialog = DIV(
            DIV(
                BUTTON(XML('&times;'), _type='button', _class='close', **{'_data-dismiss': 'modal', '_aria-hidden': 'true'}),
                H3(str(T('Select')) + ' ' + (self.document.df_title or '')),
                _class='modal-header'
            ),
            DIV(
                DIV('query-conditions'),
                DIV('query-results'),
                _class = 'modal-body'
            ),
            _id='%s_query_modal'%self.doc_field.df_name,
            _class="query-modal"
        )
        
    def _build_results_row_template(self):
        
        class DT(LI):
            tag = 'dt'
    
        class DD(LI):
            tag = 'dd'
        helpstring = self.docfield.property('type', 'help_string')
        row = TAG[''](
            DT('{.%s}'%self.docfield.property('type', 'label')), 
            DD(('{.%s}'%helpstring) if helpstring else ''),
            _class='query-result-{}'
        )
        
        return row.xml()
        