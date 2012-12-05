#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 14/11/2012

@author: INFRA-PC1
'''

from gluon.storage import Storage

class PropertyManager(object):
    _data = []
    _defaults = []
    def __init__(self, df, data):
        self._data = data or []
        self._defaults = (df.df_default if hasattr(df, 'df_default') else (df.doc_default if hasattr(df, 'doc_default') else [] )) or []
        
        self._build_data()
        self._build_default()
        self.df = df
        
        df.properties = self.properties
        df.property = self.property
        df.update_property = self.property_updater
    
    def property_getter(self):
        return self._data
    
    def property_updater(self, group, name, data):
        if hasattr(self.df, 'update_record'):
            self.property(group, name, data)
            self.df.update_record(**{('df_meta' if hasattr(self.df, 'df_meta') else 'doc_meta') : self._data})
    
    def _build_data(self):
        self.data = Storage()
        for prop in self._data:
            if not self.data[prop['group']]:
                self.data[prop['group']] = Storage() 
            self.data[prop['group']][prop['property']] = prop['value']
    
    def _build_default(self):
        self.default = Storage()
        for prop in self._defaults:
            if not self.default[prop['group']]:
                self.default[prop['group']] = Storage() 
                self.default[prop['group']][prop['property']] = prop.get('default', None)
                        
    def _merge(self, lft, rgt):
        new_props = Storage()
        for prop in lft.keys():
            if not rgt.has_key(prop):
                if not isinstance(lft[prop], Storage):
                    new_props[prop if prop != 'default' else 'value'] = lft[prop]
                else:
                    new_props[prop] = self._merge(lft[prop], Storage())
            elif not isinstance(rgt[prop], Storage):
                new_props[prop] = rgt[prop]
            else:
                new_props[prop] = self._merge(rgt[prop])
        return new_props
    
    def properties(self, group, default={}):
        return self._merge(self.data.get(group, Storage()), self.default.get(group, Storage())) or Storage()
        
    def property(self, group, name, value=None):
        prop_group = self.properties(group)
        prop = prop_group.get(name, value)
        if prop and value:
            row = filter(lambda row: row['group']==group and row['property']==name, self._data)
            prop_group[name] = value
            if row:
                row[0]['value'] = value
            else:
                self._data.append({'group': group, 'property': name, 'value': value or prop})
        elif value:
            return value
        return prop
        