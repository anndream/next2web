#-*- coding: utf-8 -*-

from gluon.dal import Field
from gluon.sqlhtml import SQLFORM
from gluon.storage import Storage
from gluon.contrib.simplejson import loads, dumps

from helpers.document import types, vtypes, policy



class Manager(object):
    _form = None
    _data = None
    def __init__(self):
        pass
    
    def form(self, **defaults):
        self._form = SQLFORM.factory(self.fields, table_name='docfield_meta')
        if defaults:
            for (k,v) in defaults.items():
                if not self.form.vars[k]:
                    self.form.vars[k]=v
                    
        return self._form
    
    def isValid(self):
        if not self._form: return False
        return self._form.process(dbio=False).accepted
    
    def errors(self):
        if self._form:
            return self._form.errors
    
    def data(self):
        return self._data
    
    def process(self, data):
        if not self._form: self.form()
        self._form.vars.update(data)
        self._form.vars.process(dbio=False)
        self._data = self._form.vars 
        
    def dump(self):
        data = self._data
        if self.options:
            data['options'] = self.options
        return {'name': self.name, 'data': data}

class PolicyManager(Manager):
    def __init__(self, data):
        self.data = data
        self.fields = []
        
        for field in policy:
            self.fields.append(Field(field, 'boolean', default=field in self.data, label = policy[field]))
            
    
class TypeManager(Manager):
    types = types
    types.update(vtypes)
    
    def __init__(self, name, data={}):
        assert name in self.types, 'Cold not find type %s in common types'%`name`
            
        self.name = name
        self._data = data if data else {}
        self.options = types[name]
        self.fields = []
        
        data = self.options['options']
        if not isinstance(data, (Storage, list)):
            return 
        
        if not isinstance(data, list): data = [data]
        for field in data:
            self.fields.append(field)

    def has_options(self):
        return self.options.has_key('options')

    def has_option(self, option):
        return option in self._data
    
    def get_options(self):
        return self._data
    
    def get_option(self, option, default=None):
        if self.has_option(option) or default!=None:
            return self._data.get(option, default)
        else:
            raise KeyError, 'Could not find option'
        
    def default(self):
        data = {}
        if self.options['options']:
            for field in self.options['options']:
                data[field.name] = field.default
        return data
    
    def __repr__(self):
        return '<TypeMananer: %s>'%`self.name`

    
class ValidatorManager(Manager):
    _errors = {}
    validator = None
    _data = {}
    def __init__(self, name, data={}):
        import inspect
        
        self.name = name
        self._data = data
        self.validator = __import__('gluon.validators', globals(), locals(), [self.name], -1)
        
        self.fields = []
        
        _data = inspect.getargspec(self.validator.__init__)
        
        for field in data.args[1:]:
            self.fields.append(Field(**field))
        
    def get(self):
        if self.isvalid() and self.validator:
            self.validator(**self._data)
        
    def isValid(self):
        if not Manager.validate(self) or not self._form: return False
        try:
            self.validator(**self._form.vars)
        except TypeError, e:
            self._errors['__meta__'] = e.message
    
    def errors(self):
        self._errors.update(Manager.errors(self) or {})
        return self._errors
    
    def __repr__(self):
        return '<ValidatorManager: %s>'%`self.name`

class ValidatorList(object):
    objects = []
    def __init__(self, data): 
        if data: 
            self.load(data)
    
    def load(self, text):
        data = loads(text)
        for validator in data:
            for (k,v) in validator:
                self.objects.append(ValidatorManager(k,v))
    
    def data(self):
        return map(lambda x: x.data(), self.objects)
    
    def dump(self):
        return dumps(map(lambda x: x.dump(), self.objects))
    
    def isValid(self):
        return all(map(lambda x: x.isValid(), self.objects))
    
    def errors(self):
        return map(lambda x: x.errors(), filter(lambda x: not x.isValid(), self.objects))
    
    def add(self, obj):
        self.objects.append(obj)
        return self
    
    def index(self, idx):
        if not str(idx).isdigits():
            return [obj.name for obj in self.objects].index(idx)
        elif self.objects.__getitem__(idx, None):
            return idx
        else:
            return None
            
    def update(self, idx, other):
        assert isinstance(other, ValidatorManager), 'Cold not update using object %s'%`type(other)`
        self.objects[self.index(idx)] = other
    
    def remove(self, idx):
        assert len(self.objects)< int(idx), 'Cold not find object in %s index position'%`idx`
        return self.objects.pop(int(idx))
    
    def from_dict(self, other):
        for (k,v) in other.items():
            self.add(ValidatorManager(k, v))
    
    def to_dict(self):
        retval = {}
        for obj in self.objects:
            retval[obj.name] = obj.data
            
    def get(self, idx):
        idx = self.index(idx) or idx
        if str(idx).isdigit() and len(self.objects) < int(idx):
            return self.objects[int(idx)]
    
    def validators(self):
        validators = []
        for validator in self.objects:
            validators.append(validator.get())
        return validators
            
    def __len__(self):
        return len(self.objects)
    
    def __iter__(self):
        return iter(self.objects)
    
class DocFieldList(Manager):
        pass