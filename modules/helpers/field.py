#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 14/11/2012

@author: INFRA-PC1
'''

from gluon import dal
from gluon import validators
from helpers.document import types
from gluon.storage import Storage

class MetaField(object):
    _type = "generic-field"
    _keys = {
        'df_name': 'name',
        'df_type': 'type',
        'df_label': 'label',
        'df_description': 'comments',
    }
    
    @classmethod
    def has_options(cls):
        return types[cls._type].has_key("options") if isinstance(cls._type, dict) else False
    
    @classmethod
    def _attributes(cls, **attrs):
        new_attrs = {}
        for key in cls._keys.keys():
            if key in attrs:
                new_attrs[cls._keys[key]] = attrs[key]
        return new_attrs
    
    @classmethod
    def _properties(cls, properties):
        new_options = {}
        if cls.has_options():
            for option in types[cls._type]:
                if option.name in properties:
                    new_options[option.name] = properties[option.name]
        return new_options
    
    @classmethod
    def requires(cls, df):
        req = []
        if df.property('policy', 'is_required') == 'ALWAYS':
            req.append(validators.IS_NOT_EMPTY())
        return req
    
    @classmethod
    def build_type(cls, df):
        return cls._type.native
    
    @classmethod
    def field(cls, df):
        from properties import PropertyManager
        
        PropertyManager(df, df.df_meta)
        
        attrs = {}
        attrs['requires'] = cls.requires(df)
        
        field =  dal.Field(df.df_name, cls.build_type(df), **attrs)
        
        return field
    
class String(MetaField):
    _type = types.string
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        props = df.properties('type')
        if props.has_key('maxsize') and props.has_key('minsize'):
            req.append(validators.IS_LENGTH(maxsize=props['maxsize'], minsize=props['minsize']))
        elif props.has_key('maxsize'):
            req.append(validators.IS_LENGTH(maxsize=props['maxsize']))
        elif props.has_key('minsize'):
            req.append(validators.IS_LENGTH(minsize=props['minsize']))
        return req
    
class Email(MetaField):
    _type = types.email
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        if df.property('type', 'validate'):
            req.append(validators.IS_EMAIL())
        return req

class Url(MetaField):
    _type = types.url
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        if df.property('type', 'validate'):
            req.append(validators.IS_URL())
        return req
    
class Phone(MetaField):
    _type = types.phone
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        if df.property('type', 'validate'):
            pass
            # TODO: Implementar um validator para campos mascarádos, baseado nas opções do iMask
        return req
    
class Integer(MetaField):
    _type = types.integer
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        props = df.properties('type')
        if props.has_key('minimun') and props.has_key('maximun'):
            req.append(validators.IS_INT_IN_RANGE(minimun=props['minimun'], maximun=props['maximun']))
        elif props.has_key('minimun'):
            req.append(validators.IS_INT_IN_RANGE(minimun=props['minimun']))
        elif props.has_key('maximun'):
            req.append(validators.IS_INT_IN_RANGE(maximun=props['maximun']))
    
class Double(MetaField):
    _type = types.double
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        props = df.properties('type')
        if props.has_key('minimun') and props.has_key('maximun'):
            req.append(validators.IS_FLOAT_IN_RANGE(minimun=props['minimun'], maximun=props['maximun'], dot=props['dot']))
        elif props.has_key('minimun'):
            req.append(validators.IS_FLOAT_IN_RANGE(minimun=props['minimun'], dot=props['dot']))
        elif props.has_key['maximun']:
            req.append(validators.IS_FLOAT_IN_RANGE(maximun=props['maximun'], dot=props['dot']))
    
class Decimal(Double):
    _type = types.decimal
    
    @classmethod
    def build_type(cls, df):
        props = df.properties('type')
        if props['n'] and props['m']:
            return cls._type + '(%s, %s)'%(props['n'], props['m'])
        return cls._type
    
class Date(MetaField):
    _type = types.date
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        props = df.properties('type')
        if props['minimun'] and props['maximun']:
            req.append(validators.IS_DATETIME_IN_RANGE(minimun=props['minimun'], maximun=props['maximun'], format=props['format']))
        elif props['maximun']:
            req.append(validators.IS_DATETIME_IN_RANGE(maximun=props['maximun'], format=props['format']))
        elif props['minimun']:
            req.append(validators.IS_DATETIME_IN_RANGE(minimun=props['minimun'], format=props['format']))
        elif props['format']:
            req.append(validators.IS_DATETIME(format=props['format']))
            
class Time(Date):
    _type = types.time
    
class Datetime(Date):
    _type = types.datetime
    
class Currency(MetaField):
    _type = types.currency
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        props = df.properties('type')
        if props.has_key('minimun') and props.has_key('maximun'):
            req.append(validators.IS_FLOAT_IN_RANGE(minimun=props['minimun'], maximun=props['maximun'], dot=props['decimalSeparator']))
        elif props.has_key('minimun'):
            req.append(validators.IS_FLOAT_IN_RANGE(minimun=props['minimun'], dot=props['decimalSeparator']))
        elif props.has_key['maximun']:
            req.append(validators.IS_FLOAT_IN_RANGE(maximun=props['maximun'], dot=props['decimalSeparator']))
    
class Text(MetaField):
    _type = types.text

class SmallText(MetaField):
    _type = types.smalltext
    
class Texteditor(MetaField):
    _type = types.texteditor
    
class Rule(MetaField):
    _type = types.rule
    
class Select(MetaField):
    _type = types.select
    
    @classmethod
    def build_type(cls, df):
        return df.property("type", "datatype")
    
class MultipleSelect(MetaField):
    _type = types.multipleselect
    
class List(MetaField):
    _type = types.list
    
class Password(MetaField):
    _type = types.password
    
    @classmethod
    def requires(cls, df):
        req = MetaField.requires(df)
        req.append(validators.CRYPT())
        if df.properties('type', 'enforce_safety'):
            req.append = validators.IS_STRONG()
        return req
    
class FileLink(MetaField):
    _type = types.filelink
    
class Link(MetaField):
    _type = types.link
    
    @classmethod
    def build_type(cls, df):
        return cls._type.native + ' %s' %df.property('type', 'document')
    
    
fields = Storage(
    string = String,
    email = Email,
    url = Url,
    phone = Phone,
    integer = Integer,
    double = Double,
    decimal = Decimal,
    date = Date,
    time = Time,
    datetime = Datetime,
    currency = Currency,
    text = Text,
    smalltext = SmallText,
    texteditor = Texteditor,
    rule = Rule,
    select = Select,
    multipleselect = MultipleSelect,
    list = List,
    password = Password,
    filelink = FileLink,
    link = Link
)