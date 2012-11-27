#-*- coding: utf-8 -*-

from gluon.storage import Storage

class BaseManager(object):
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
    def form(self):
        raise NotImplementedError
    
    def store(self):
        raise NotImplementedError
        
    def save_data(self, processor=None):
        data = (processor(self.form.vars) if callable(processor) else (True, self.form.vars))
        if data[0]:
            self._storager.set_data(self._part_name, data[1])
    
    def save_files(self, processor=None):
        data = (processor(self.form.vars) if callable(processor) else (True, self.form.vars))
        self._storager.set_files(self._part_name, data)
    
    @property
    def data(self):
        return self._storager.get_data(self._part_name)

    @property
    def files(self):
        self._storager.get_files(self._part_name)
        
    def validate_and_save(self):
        if self.form.validate():
            self.save()