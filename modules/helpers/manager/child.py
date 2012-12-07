#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 27/11/2012

@author: INFRA-PC1
'''

from base import BaseManager
from gluon import current
from gluon.http import HTTP
from gluon.compileapp import LOAD
from helpers import message

class ChildManager(BaseManager):
    def __init__(self, db, document, doc_parent, storager, part_name=None ):
        BaseManager.__init__(self, db, document, storager, part_name)
        
        self.doc_parent = doc_parent
                
        self.child_name = self.document.META.doc_name
        self.T = current.T
        self.request = current.request
        self.response = current.response
        
        if not self._part_name:
            self._part_name = self.__class__.__name__
        
        self._id = '%s_%s_%s'%(self._part_name, self.child_name, self.doc_parent.META.doc_name)
        self._name = '%s_for_%s_on_%s'%(self._part_name, self.child_name, self.doc_parent.META.doc_name)
        
        self.base_url_child = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_child_form_%s'%self.child_name: self.doc_parent.META.doc_name, '__action': 'table'})
        self.base_url_child_add = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_child_form_%s'%self.child_name: self.doc_parent.META.doc_name, '__action': 'add'})
        self.base_url_child_edit = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_child_form_%s'%self.child_name: self.doc_parent.META.doc_name, '__action': 'edit'})
        self.base_url_child_remove = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_child_form_%s'%self.child_name: self.doc_parent.META.doc_name, '__action': 'remove'})
        self.base_url_child_childs = dict(r=self.request, c=self.request.cotnroller, f=self.request.function, args=self.request.args, vars={'__document_child_form_%s'%self.child_name: self.doc_parent.META.doc_name, '__action': 'childs'})
        
        self.callback()
        
    @property
    def component(self):
        base = self.base_url_child.copy()
        base['ajax'] = True
        base['ajax_trap'] = True
        return  LOAD(**base)
    
    def callback(self):
        if '__document_child_form_%s'%self.child_name in self.request.vars and self.request.vars['__document_child_form_%s'%self.child_name] == self.doc_parent.META.doc_name:
            if '__action' in self.request.vars and self.request.vars['__action'] == 'table':
                raise HTTP(200, self.build_table().xml())
            if '__action' in self.request.vars and self.request.vars['__action'] == 'add':
                raise HTTP(200, self.form)
            if '__action' in self.request.vars and self.request.vars['__action'] == 'edit':
                self.document = self.get_child(self.request.vars['__saved'], self.request.vars['__idx'])
                raise HTTP(200, self.form)
            if '__action' in self.request.vars and self.request.vars['__action'] == 'childs':
                #TODO: Future
                raise self.build_components()
            raise HTTP(200, self.build_modal())
    
    def count_childs(self, child_name=None, doc_parent=None, doc_parent_id = None):
        return self.db((self.db[child_name or self.child_name].document==self.document.META.id)&
                       (self.db[child_name or self.child_name].doc_parent==(doc_parent or self.doc_parent.META.id))&
                       (self.db[child_name or self.child_name].doc_parent_id==(doc_parent_id or self.doc_parent.id))).count()
    
    def has_sub_childs(self, child_name=None, doc_parent = None, doc_parent_id = None):
        return self.db((self.db[child_name or self.child_name].document==self.document.META.id)&
                       (self.db[child_name or self.child_name].doc_parent==(doc_parent or self.doc_parent.META.id))&
                       (self.db[child_name or self.child_name].doc_parent_id==(doc_parent_id or self.doc_parent.id))).count()>0
    
    def list_sub_childs(self, child_name = None, doc_parent = None, doc_parent_id = None):
        return self.db((self.db[child_name or self.child_name].document==self.document.META.id)&
                       (self.db[child_name or self.child_name].doc_parent==(doc_parent or self.doc_parent.META.id))&
                       (self.db[child_name or self.child_name].doc_parent_id==(doc_parent_id or self.doc_parent.id))).select(self.db[child_name or self.child_name].ALL)
    
    def list_childs(self):
        childs = []
        childs.extend(self.list_childs_in_session())
        childs.extend(self.list_childs_in_db())
        return childs
    
    def list_childs_in_session(self):
        return self.data
        
    def list_childs_in_db(self):
        childs = self.db((self.db[self.child_name].document==self.document.META.id)&
                         (self.db[self.child_name].doc_parent==self.doc_parent.META.id)&
                         (self.db[self.child_name].doc_parent_id==self.doc_parent.id)).select(self.db[self.child_name].ALL)
        
        map(lambda x: x.__setitem__('__saved', (True, x.id)), childs)
        
        return childs
    
    def get_child(self, saved, idx):
        from helpers import safe_bool
        
        if safe_bool(saved):
            return self.get_child_in_db(idx)
        else:
            return self.get_child_in_session(idx)
    
    def get_child_in_db(self, child_id):
        child_row = self.db.get_document(self.child_name, child_id)
        if child_row:
            return child_row
        message(self.T('Children Lookup Error'), self.T('Unable to locate document children for this document'), True)
        return False
        
    def remove_child(self, child_id):
        child_row = self.get_child(child_id)
        if child_row:
            return child_row
    
    def validate_child(self, **kwargs):
        return self.db[self.child_name]._validate(**kwargs)
    
    def add_child(self, **kwargs):
        if not kwargs.has_key('document'):
            kwargs['document'] = self.document.META.id
        if not kwargs.has_key('doc_parent'):
            kwargs['doc_parent'] = self.parent.META.id
        if not kwargs.has_key('data_id'):
            kwargs['doc_parent_id'] = self.parent.id
        errors = self.validate_child(**kwargs)
        if not errors:
            child_id = self.db[self.child_name].insert(**kwargs)
            return child_id
        else:
            message(self.T('Validation Error'), ['<b>%s:</b> %s'%(self.document.META.get_df_name(df), error) for df, error in errors.values()], as_table=True)
            
    def update_child(self, child_id, **kwargs):
        child_row = self.get_child(child_id)
        if child_row:
            errors = self.validate_child(**kwargs)
            if not errors:
                return self.document.update_document(**kwargs)
            else:
                message('Validation Error', ['<b>%s:</b> %s'%(self.document.META.get_df_name(df), error) for df, error in errors.values()], as_table=True)
    
    @property
    def form(self):
        raise NotImplementedError
    
    def _session_reindex(self):
        for i, row in enumerate(self.data):
            row['__saved'] = (False, i)
    
    def validate_and_save(self):
        def processor(_vars):
            row = self.db[self.child_name]._filter_fields(**self.request.vars)
            row['__saved'] = (False, len(self.data))
            self.data.insert(0, row)
            self._session_reindex() 
    
        if self.form.accepts(self.request.vars, formname=self._name):
            self.save_data(processor)
        else:
            message(self.T('Validation Error'), ['<b>%s:</b> %s'%(self.document.META.get_df_name(df), error) for df, error in self.form.errors.values()], as_table=True)
            
    def script(self):
        raise NotImplementedError
    
    def build_components(self):
        raise NotImplementedError
    
    def build_modal(self):
        raise NotImplementedError
    
    def build_table(self):
        raise NotImplementedError
    
    @property
    def cwidget(self):
        raise NotImplementedError
    
    def store(self):
        for row in self.data:
            self.add_child(**row)