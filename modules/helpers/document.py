#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 17/10/2012

@author: INFRA-PC1
'''

from gluon.dal import Field
from gluon.storage import Storage
from gluon import current, validators
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
        'label': T('Data'),
        'options': [
            Field('minsize', 'integer', notnull=True, default=None, label=T('Min Size')),
            Field('maxsize', 'integer', notnull=True, default=None, label=T('Max Size'))
        ]
    }),
    'email': Storage({
        'native': 'string',
        '_class': 'email',
        'label': T('Email'),
        'options': [
            Field('validate', 'boolean', default=True, label=T('Validate?'))
        ]
    }),
    'url': Storage({
        'native': 'string',
        '_class': 'url',
        'label': T('Url'),
        'options': [
            Field('validate', 'boolean', default=True, label=T('Validate?'))
        ]
    }),
    'phone': Storage({
        'native': 'string',
        '_class': 'phone',
        'label': T('Phone'),
        'options': [
            Field('mask', 'boolean', default=True, label=T('Mask')),
        ]
    }),
    'text': Storage({
        'native': 'text',
        '_class': 'text',
        'label':  T('Text'),
        'options': [
            Field('minsize', 'integer', notnull=True, default=None, label=T('Min Size')),
            Field('maxsize', 'integer', notnull=True, default=None, label=T('Max Size'))
        ]
    }),
    'smalltext': Storage({
        'native': 'string',
        '_class': 'smalltext',
        'label': T('Small Text'),
        'options': [
            Field('minsize', 'integer', notnull=True, default=None, label=T('Min Size')),
            Field('maxsize', 'integer', notnull=True, default=None, label=T('Max Size'))
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
    'property': Storage({
        'native': 'text',
        '_class': 'property',
        'label': T('Property')
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
        'options': [
            Field('minimun', 'integer', default=None, label=T('Minimun')),
            Field('maximun', 'integer', default=None, label=T('Maximun'))
        ]
    }),
    'double': Storage({
        'native': 'double',
        '_class': 'double',
        'label': T('Double Number'),
        'options': [
            Field('minimun', 'integer', default=None, label=T('Minimun')),
            Field('maximun', 'integer', default=None, label=T('Maximun')),
            Field('dot', 'string', default='.', label=T('Dot'))
        ]
    }),
    'decimal': Storage({
        'native': 'decimal',
        '_class': 'decimal',
        'label': T('Decimal'),
        'options': [
            Field('n', 'integer', default=None, label=T('Digits')),
            Field('m', 'integer', default=None, label=T('Decimal Places')),
            Field('minimun', 'integer', default=None, label=T('Minimun')),
            Field('maximun', 'integer', default=None, label=T('Maximun')),
            Field('dot', 'string', default='.', label=T('Dot'))
        ],
    }),
    'currency': Storage({
        'native': 'double',
        '_class': 'currency',
        'label': T('Money'),
        'options': [
            Field('symbol', 'string', default='$', label=T('Symbol')),
            Field('international', 'string', default='USD', label=T('International')),
            Field('decimalDigits', 'integer', default=2, label=T('Decimal Digits')),
            Field('decimalSeparator', 'string', default='.', label=T('Decimal Separator')),
            Field('thousandDigits', 'integer', default=3, label=T('Thousand Digits')),
            Field('thousandSeparator', 'string', default=',', label=T('Thousand Separator')),
            Field('minimun', 'integer', default=None, label=T('Minimun')),
            Field('maximun', 'integer', default=None, label=T('Maximun')),
        ],
    }),
    'date': Storage({
        'native': 'date',
        '_class': 'date',
        'label': T('Date'),
        'options': [
            Field('format', 'string', default='%Y-%m-%d', requires=validators.IS_NOT_EMPTY(), label=T('Format')),
            Field('minimun', 'string', default='1900-01-01', label=T('Minimun')),
            Field('maximun', 'string', default=None, label=T('Maximun'))
        ],
    }),
    'time': Storage({
        'native': 'time',
        '_class': 'time',
        'label': T('Time'),
        'options': [
            Field('format', 'string', default='%H-%M-%S', requires=validators.IS_NOT_EMPTY(), label='Format'),
            Field('minimun', 'string', default='1900-01-01', label=T('Minimun')),
            Field('maximun', 'string', default=None, label=T('Maximun'))
        ],
    }),
    'datetime': Storage({
        'native': 'datetime',
        '_class': 'datetime',
        'label': T('Date/Time'),
        'options': [
            Field('format', 'string', default='%Y-%m-%d %H-%M-%S', requires=validators.IS_NOT_EMPTY(), label='Format'),
            Field('minimun', 'string', default='1900-01-01', label=T('Minimun')),
            Field('maximun', 'string', default=None, label=T('Maximun'))
        ],
    }),
    'password': Storage({
        'native': 'password',
        '_class': 'password',
        'label': T('Password'),
        'options': [
            Field('enforce_safety', 'boolean', default=False, label=T("Enforce Safety"))
        ]
    }),
    'filelink': Storage({
        'native': 'upload',
        '_class': 'filelink',
        'label': T('Upload'),
        'options': [
            Field('multiple', 'boolean', default=False, label=T('Allow Multiple Files?'))
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

#TODO 1: Implementar uma rotina de atualização para cada registro.

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
