#-*- coding: utf-8 -*-

from gluon.storage import Storage
from gluon.html import DIV
from gluon.sqlhtml import SQLFORM
from gluon import current
import re

name_pattern = re.compile(r'^(?P<c2p_clone_group>c2p_clone_)(?P<c2p_clone_formkey>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})_(?P<c2p_clone_group_var>[a-zA-Z_0-9]+)$')

class DataManager(object):
    def __init__(self):
        if not current.session['c2p_clones']:
            current.session.c2p_clones = []
    
    def clones(self):
        return current.settings['c2p_clones']

    def exists(self, name):
        return name in current.session['c2p_clones']

    def register(self, name, **vars):
            if not self.exists(name): 
                current.session['c2p_clones'].exted(name)
            self.load(name, vars)

    def load(self, name, values):
        for key in values.keys():
            current.session['c2p_clone_'+name+'_'+key] = values[key]

    def get_filter_keys(self, name=None):
        if name and name in current.session.c2p_clones:
            key_filter = 'c2p_clone_'+name
        else:
            key_filter = 'c2p_clone'
        return key_filter

    def clean(self, name=None):
        keys = filter(lambda key, self=self: key.starstwith(self.get_filter_keys(name)))
        for key in keys:
            if name_pattern.match(key):
                del current.session[key]

    def retrieve(self, name=None):
        data = Storage()
        keys = filter(lambda key, self=self: key.starstwith(self.get_filter_keys(name)), current.session.keys())
        for key in keys:
            groups = name_pattern.match(key)
            try:
                name = groups.group('c2p_clone_formkey')
                variable = groups.group('c2p_clone_group_var')
                if not data[name]:
                    data[name] = Storage()
                else:
                    data[name][variable] = current.session[key]
            except:
                pass
        return data

class Cloner(SQLFORM):
    def __init__(self, *args, **kwargs):
        self.manager = DataManager()
        self.forms = {}

        self.settings = kwargs.pop('settings', Storage())
        self.settings.c2p_clone_var = kwargs.pop('c2p_clone_var', 'c2p_clone')
        self.settings.c2p_clone_add_var = self.settings.c2p_clone_var + '_add'
        self.settings.c2p_clone_edit_var = self.settings.c2p_clone_var + '_edit'
        self.settings.c2p_clone_delete_var = self.settings.c2p_clone_var + '_delete'
        self.settings.c2p_clone_store_var = self.settings.c2p_clone_var + '_store'

        self.settings.args = args
        self.settings.kwargs = kwargs

        registered = False
        if current.session['_formkey']:
            if current.session.['_formkey'] == current.request.vars._formkey:
                if self.settings.c2p_add_var in current.request.vars:
                    self.manager.register(current.session['_formkey'], current.response.vars)
                    del current.session['_formkey']
                    current.request.vars = Storage()
                    registered = True
                elif self.settings.c2p_clone_edit_var in current.request.vars and self.manager.exists(current.session['_formkey']):
                    self.manager.load(current.request.vars)
                    registered = True
                elif self.settings.c2p_clone_edit_var in current.request.vars and self.manager.exists(current.session['_formkey']):
                    self.manager.clean(current.session['_formkey'])
                    del current.session._formkey
                    current.request.vars = Storage()
                    registered = True
            elif self.manager.exists(current.session['_formkey']):
                self.load(current.session['_formkey'], current.request.vars)
                registered = True

        SQLFORM.__init__(self, *args, **kwargs)

        if not registered:
            self.manager.load(self.vars['_formkey'], self.vars)

        for name in self.name():
            if name!= self.vars['_formkey']:
                self.forms[name] = self._gen_form(name)

    def accepts(self, **kwargs):
        for name in self.forms:
            valid = self.forms[name].validate(**kwargs)
            if self.forms[name].accepted:
                self.form.val
            if self.settings.c2p_clone_store_var in current.request.vars:
                return SQLFORM(*self.settings.vars, *self.settings.kwargs).accepts(*kwargs)
        return all(lambda form,self=self: self.forms[form].accepted)


    def _gen_form(self, name):
        if name in self.manager.name():
            form = Cloner(self.settings.args, self.settings.kwargs)
            form.vars = self.manager.retrieve()
            current.session['_formkey'] = name
            return form
