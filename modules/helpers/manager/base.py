#-*- coding: utf-8 -*-

from helpers import process_form
from gluon.html import URL
from gluon.storage import Storage

class BaseManager(object):
    components = []
    url_binds = Storage()
    def __init__(self, parent, db, document, storager, part_name=None):
        self.parent = parent
        self.db = db
        self.document = document
        self._part_name = part_name
        self._storager = storager

    def callback(self):            
        raise NotImplementedError
    
    @property
    def current_url(self):
        return URL(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars=self.request.vars)
    
    @property
    def url(self):
        raise NotImplementedError
    
    @property
    def form(self):
        raise NotImplementedError
    
    def store(self):
        raise NotImplementedError
        
    def save(self):
        data = process_form(self.form.vars)
        self._storager.set_data(self._part_name, data[0])
        self._storager.set_files(self._part_name, data[1])
    
    @property
    def data(self):
        self._storager.get_data(self._part_name)

    @property
    def files(self):
        self._storager.get_files(self._part_name)
        
    def validate_and_save(self):
        if self.form.validate():
            self.save()