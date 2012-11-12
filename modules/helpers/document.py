#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 17/10/2012

@author: INFRA-PC1
'''

from gluon.dal import Field
from gluon.storage import Storage
from gluon import current
from gluon.contrib.simplejson import loads

T = current.T

policy_readable = 'r'
policy_writable = 'w'
policy_unique = 'u'
policy_unique_in_parent = 'p'
policy_required = 'n'

policy = Storage({
    policy_readable: T('Readable'),
    policy_writable: T('Writable'),
    policy_unique: T('Unique'),
    policy_unique_in_parent: T('Unique in parent'),
    policy_required: T('Required')
})

status_draft = 'd'
status_sended = 's'
status_cancelled = 'c'
status_for_exclusion = 'e'

status = Storage({
    status_draft: T('Draft'),
    status_sended: T('Sended'),
    status_cancelled: T('Cancelled'),
    status_for_exclusion: T('To Exclude')
})

types = Storage({
    'string': Storage({
        'native': 'string',
        '_class': 'string',
        'ui_type': 'text',
        'label': T('Data'),
    }),
    'text': Storage({
        'native': 'text',
        '_class': 'text',
        'label':  T('Text'),
    }),
    'smalltext': Storage({
        'native': 'string',
        '_class': 'smalltext',
        'label': T('Small Text'),
        'options': [
            Field('lenght', 'integer', notnull=True, default=100, label=T('Lenght'))
        ],
    }),
    'texteditor': Storage({
        'native': 'text',
        '_class': 'texteditor',
        'label': T('Text Editor'),
    }),
    'rule': Storage({
        'native': 'text',
        '_class': 'rule',
        'label': T('Rule'),
    }),
    'boolean': Storage({
        'native': 'boolean',
        '_class': 'boolean',
        'label': T('Yes/No'),
    }),
    'blob': Storage({
        'native': 'blob',
        '_class': 'generic-widget',
        'label': T('Binary Data'),
    }),
    'integer': Storage({
        'native': 'integer',
        '_class': 'integer',
        'label': T('Number'),
    }),
    'double': Storage({
        'native': 'double',
        '_class': 'double',
        'label': T('Double Number'),
    }),
    'decimal': Storage({
        'native': 'decimal',
        '_class': 'decimal',
        'label': T('Decimal'),
        'options': [
            Field('n', 'integer', default=None, label='Digits'),
            Field('m', 'integer', default=None, label='Decimal Places')
        ],
    }),
    'currency': Storage({
        'native': 'double',
        '_class': 'currency',
        'label': T('Money'),
        'options': [
            Field('symbol', 'string', default='$', label='Symbol'),
            Field('international', 'string', default='USD', label='International'),
            Field('decimal_digits', 'integer', default=2, label='Decimal Digits'),
            Field('decimal_separator', 'string', default='.', label='Decimal Separator'),
            Field('thousand_digits', 'integer', default=3, label='Thousand Digits'),
            Field('thousand_separator', 'string', default=',', label='Thousand Separator'),
        ],
    }),
    'date': Storage({
        'native': 'date',
        '_class': 'date',
        'label': T('Date'),
        'options': [
            Field('strftime', 'string', default='%Y-%m-%d', label='Format'),
        ],
    }),
    'time': Storage({
        'native': 'time',
        '_class': 'time',
        'label': T('Time'),
        'options': [
            Field('strftime', 'string', default='%H-%M-%S', label='Format'),
        ],
    }),
    'datetime': Storage({
        'native': 'datetime',
        '_class': 'datetime',
        'label': T('Date/Time'),
        'options': [
            Field('strftime', 'string', default='%Y-%m-%d %H-%M-%S', label='Format'),
        ],
    }),
    'password': Storage({
        'native': 'password',
        '_class': 'password',
        'label': T('Password'),
    }),
    'filelink': Storage({
        'native': 'upload',
        '_class': 'filelink',
        'label': T('Upload'),
        'options': [
            Field('uploadfield', 'string', default=None, label='Field'),
            Field('uploadfolder', 'upload', default=None, label='Folder'),
            Field('uploadseparated', 'boolean', default=None, label='Separated?'),
            Field('uploadfs', 'string', default=None, label='Diferenced File System?'),
        ],
    }),
    'link': Storage({
        'native': 'reference',
        '_class': 'link',
        'label': T('Link'),
        'options': [ 
            Field('document', 'reference tabDocuments', default=None, label=T('Document'), required=True),
            Field('label', 'reference tabDocumentFields', default=None, required=True, notnull=True),
            Field('help_string', 'string', default=None, label=T('Label Field')),
        ],
    }),
    'select': Storage({
        'native': 'string',
        'class': 'select',
        'label': T('Single Choice'),
        'options': [
            Field('choices', 'text', notnull=True, required=True, label=T('Choices')),
        ],
    }),
    'multipleselect': Storage({
        'native': 'list:string',
        'class': 'multiple',
        'label': T('Multiple Choices'),
        'options': [
            Field('choices', 'text', notnull=True, required=True, label=T('Choices')),
        ],
    }),
    'list': Storage({
        'native': 'list:integer',
        'class': 'list',
        'label': T('List'),
        'options': [
            Field('choices', 'text', notnull=True, required=True, label=T('Choices')),
        ],
    }),
})

vtypes = Storage({
    'suggest': Storage({
        'native': 'virtual',
        '_class': 'suggest',
        'label': T('Suggest'),
    }),
    'table': Storage({
        'native': 'virtual',
        '_class': 'table',
        'label': T('Table'),
        'options': [
            Field('child', 'string', notnull=True, required=True, label=T('Child'))
        ],
    }),
    'sectionbreak': Storage({
        'native': 'virtual',
        '_class': 'sectionbreak',
        'label': T('Section Break'),
    }),
    'columnbreak': Storage({
        'native': 'virtual',
        '_class': 'columnbreak',
        'label': T('Column Break'),
    }),
    'button': Storage({
       'native': 'virtual',
       '_class': 'button',
       'label': T('Button'),   
    }),
})

def _loader(db, table, data, document=None):
    if isinstance(data, list):
        for row in data:
            _loader(db, table, row, document)
    elif isinstance(data, dict):
        if document:
            data['document'] = document
        return  db[table].insert(**db[table]._filter_fields(data))
    
def _solve_definition(db, table, data, document=None):
    if not isinstance(data, list): data = [data]
    for definition in data:
        parent = _loader(db, table, definition, document)
        if definition.has_key('doc_fields'):
            _loader(db, 'tabDocumentField', definition['doc_fields'], parent)

def load_definition(db, filename):
    data = loads(open(filename).read())
    _solve_definition(db, 'tabDocument', data)
    db.commit();
   
def load_data(db, filename):
    pass
        