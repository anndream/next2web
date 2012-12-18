#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 17/10/2012

@author: INFRA-PC1
'''

import os

from gluon.dal import Field
from gluon.storage import Storage
from gluon import current, validators
from gluon.contrib.simplejson import loads
import re

from datetime import date, datetime
from time import time, strptime

T = current.T

yes_no = {
    False : T('No'),
    True : T('True')
}

status_draft = 'd'
status_sended = 's'
status_cancelled = 'c'
status_in_trash = 't'

status = Storage({
    status_draft: T('Draft'),
    status_sended: T('Sended'),
    status_cancelled: T('Cancelled'),
    status_in_trash: T('In Trash')
})

EQ_OPERATOR = ('eq', T('Equals to'), lambda lft, rgt: lft == rgt)
GT_OPERATOR = ('gt', T('Greather than'), lambda lft, rgt: lft > rgt) 
LT_OPERATOR = ('lt', T('Less than'), lambda lft, rgt: lft < rgt)
NE_OPERATOR = ('ne', T('Not equals to'), lambda lft, rgt: lft != rgt)
GE_OPERATOR = ('ge', T('Greather or equals to'), lambda lft, rgt: lft >= rgt)
LE_OPERATOR = ('le', T('Less or equals to'), lambda lft, rgt: lft <= rgt)

COMMON_OP = [
    EQ_OPERATOR,
    GT_OPERATOR,
    LT_OPERATOR,
    NE_OPERATOR,
    GE_OPERATOR,
    LE_OPERATOR
]

STR_OP = [
    ('contains', T('Contains'), lambda lft, rgt: rgt in lft),
    ('notcontains', T('Not contains'), lambda lft, rgt: not rgt in lft ),
    ('startswith', T('Starts with'), lambda lft, rgt: str(lft).startswith(str(rgt))),
    ('endswith', T('Ends with'), lambda lft, rgt: str(lft).endswith(str(rgt)))
]

BOOL_OP = [
    ('is_true', T('Is True'), lambda lft: lft == True),
    ('is_false', T('Is False'), lambda lft: lft == False)
]

REGEX_OP = [('match', T('Match'), lambda lft, rgt: not re.match(rgt, lft) is None )]

DATE_OP = (
    ('eq', T('Equals to'), lambda lft, rgt, strftime="%Y-%m-%d": lft == date(*strptime(rgt, strftime)[:3])),
    ('gt', T('Greather than'), lambda lft, rgt, strftime="%Y-%m-%d": lft > date(*strptime(rgt, strftime)[:3])),
    ('lt', T('Less than'), lambda lft, rgt, strftime="%Y-%m-%d": lft < date(*strptime(rgt, strftime)[:3])),
    ('ne', T('Not equals to'), lambda lft, rgt, strftime="%Y-%m-%d": lft != date(*strptime(rgt, strftime)[:3])),
    ('ge', T('Greather or equals to'), lambda lft, rgt, strftime="%Y-%m-%d": lft >= date(*strptime(rgt, strftime)[:3])),
    ('le', T('Less or equals to'), lambda lft, rgt, strftime="%Y-%m-%d": lft <= date(*strptime(rgt, strftime)[:3]))
)

TIME_OP = (
    ('eq', T('Equals to'), lambda lft, rgt, strftime="%H:%M:%s": lft == time(*strptime(rgt, strptime)[-4: -1])),
    ('gt', T('Greather than'), lambda lft, rgt, strftime="%H:%M:%s": lft > time(*strptime(rgt, strptime)[-4: -1])),
    ('lt', T('Greather than'), lambda lft, rgt, strftime="%H:%M:%s": lft < time(*strptime(rgt, strptime)[-4: -1])),
    ('ne', T('Not equals to'), lambda lft, rgt, strftime="%H:%M:%s": lft != time(*strptime(rgt, strptime)[-4: -1])),
    ('ge', T('Greather or equals to'), lambda lft, rgt, strftime="%H:%M:%s": lft >= time(*strptime(rgt, strptime)[-4: -1])),
    ('le', T('Less or equals to'), lambda lft, rgt, strftime="%H:%M:%s": lft <= time(*strptime(rgt, strptime)[-4: -1]))
)

DATETIME_OP = (
    ('eq', T('Equals to'), lambda lft, rgt, strftime="%Y-%m-%d %H:%M:%s": lft == datetime(*strptime(rgt, strftime))),
    ('gt', T('Greather than'), lambda lft, rgt, strftime="%Y-%m-%d %H:%M:%s": lft > datetime(*strptime(rgt, strftime))),
    ('lt', T('Less than'), lambda lft, rgt, strftime="%Y-%m-%d %H:%M:%s": lft < datetime(*strptime(rgt, strftime))),
    ('ne', T('Not equals to'), lambda lft, rgt, strftime="%Y-%m-%d %H:%M:%s": lft != datetime(*strptime(rgt, strftime))),
    ('ge', T('Greather or equals to'), lambda lft, rgt, strftime="%Y-%m-%d %H:%M:%s": lft >= datetime(*strptime(rgt, strftime))),
    ('le', T('Less or equals to'), lambda lft, rgt, strftime="%Y-%m-%d %H:%M:%s": lft <= datetime(*strptime(rgt, strftime)))
)


types = Storage({
    'string': Storage({
        'native': 'string',
        '_class': 'string',
        'label': T('Data'),
        'options': [
            Field('minsize', 'integer', notnull=True, default=None, label=T('Min Size')),
            Field('maxsize', 'integer', notnull=True, default=None, label=T('Max Size'))
        ],
        'operators': COMMON_OP + STR_OP
    }),
    'email': Storage({
        'native': 'string',
        '_class': 'email',
        'label': T('Email'),
        'options': [
            Field('validate', 'boolean', default=True, label=T('Validate?'))
        ],
        'operators': STR_OP
    }),
    'url': Storage({
        'native': 'string',
        '_class': 'url',
        'label': T('Url'),
        'options': [
            Field('validate', 'boolean', default=True, label=T('Validate?'))
        ],
        'operators': STR_OP
    }),
    'phone': Storage({
        'native': 'string',
        '_class': 'phone',
        'label': T('Phone'),
        'options': [
            Field('mask', 'boolean', default=True, label=T('Mask')),
        ],
        'operators': STR_OP
    }),
    'text': Storage({
        'native': 'text',
        '_class': 'text',
        'label':  T('Text'),
        'options': [
            Field('minsize', 'integer', notnull=True, default=None, label=T('Min Size')),
            Field('maxsize', 'integer', notnull=True, default=None, label=T('Max Size'))
        ],
        'operators': STR_OP[:2]
    }),
    'smalltext': Storage({
        'native': 'string',
        '_class': 'smalltext',
        'label': T('Small Text'),
        'options': [
            Field('minsize', 'integer', notnull=True, default=None, label=T('Min Size')),
            Field('maxsize', 'integer', notnull=True, default=None, label=T('Max Size'))
        ],
        'operators': STR_OP[:2]
    }),
    'texteditor': Storage({
        'native': 'text',
        '_class': 'texteditor',
        'label': T('Text Editor'),
        'operators': STR_OP[:2]
    }),
    'rule': Storage({
        'native': 'text',
        '_class': 'rule',
        'label': T('Rule'),
        'operators': STR_OP[:2]
    }),
    'property': Storage({
        'native': 'text',
        '_class': 'property',
        'label': T('Property'),
    }),
    'boolean': Storage({
        'native': 'boolean',
        '_class': 'boolean',
        'label': T('Yes/No'),
        'operators': BOOL_OP
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
        ],
        'operators': COMMON_OP
    }),
    'double': Storage({
        'native': 'double',
        '_class': 'double',
        'label': T('Double Number'),
        'options': [
            Field('minimun', 'integer', default=None, label=T('Minimun')),
            Field('maximun', 'integer', default=None, label=T('Maximun')),
            Field('dot', 'string', default='.', label=T('Dot'))
        ],
        'operators': COMMON_OP
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
        'operators': COMMON_OP
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
        'operators': COMMON_OP
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
        'operators': DATE_OP,
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
        'operators': TIME_OP,
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
        'operators': DATETIME_OP
    }),
    'password': Storage({
        'native': 'password',
        '_class': 'password',
        'label': T('Password'),
        'options': [
            Field('enforce_safety', 'boolean', default=False, label=T("Enforce Safety"))
        ],
        'operators': []
    }),
    'filelink': Storage({
        'native': 'upload',
        '_class': 'filelink',
        'label': T('Upload'),
        'options': [
            Field('multiple', 'boolean', default=False, label=T('Allow Multiple Files?'))
        ],
        'operators': []
    }),
    'link': Storage({
        'native': 'reference',
        '_class': 'link',
        'label': T('Link'),
        'options': [ 
            Field('document', 'reference tabDocuments', default=None, label=T('Document'), required=True),
            Field('label', 'reference tabDocumentFields', default=None, required=True, notnull=True),
            Field('help_string', 'string', default=None, label=T('Label Field')),
            Field('search_in_childs', 'boolean', default=False, label=T('Allo'))
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
    'childsingle': Storage({
        'native': 'virtual',
        '_class': 'child-single',
        'label': 'Single Child',
    }),
    'childtable': Storage({
        'native': 'virtual',
        '_class': 'child-many',
        'label': 'Many Childs',
        'option': [
            Field('document', 'reference tabDocuments', ),
            Field('columns', 'list:string', label=T('Columns')),
            #Field('with_sub_childs', 'boolean', default=False, label=T('With sub-childs?'), requires=validators.IS_IN_SET(yes_no, zero=None)),
            #Field('allow_links', 'boolean', default=False, label=T('Allow links'), requires=validators.IS_IN_SET(yes_no, zero=None)),
            #Field('allow_file_links', 'boolean', default=False, label=T('Allow file-links'), requires=validators.IS_IN_SET(yes_no, zero=None))
        ]
    }),
    'button': Storage({
       'native': 'virtual',
       '_class': 'button',
       'label': T('Button'),
    }),
})

DOC_FIELD_META_DEFAULTS = [
    {"default": "ALWAYS", "type": "string", "property": "is_writable", "group": "policy", "options": ["ON_CREATE", "ON_UPDATE", "ALWAYS", "NEVER"]}, 
    {"default": "ALWAYS", "type": "string", "property": "is_readable", "group": "policy", "options": ["ON_CREATE", "ON_UPDATE", "ALWAYS", "NEVER"]}, 
    {"default": "NEVER", "type": "atring", "property": "is_required", "group": "policy", "options": ["ON_CREATE", "ON_UPDATE", "ALWAYS", "NEVER"]}, 
    {"type": "string", "property": "represent", "group": "visibility"}, 
    {"default": False, "type": "boolean", "property": "hide_in_filter", "group": "visibility"}, 
    {"default": False, "type": "boolean", "property": "hide_in_report", "group": "visibility"}, 
    {"default": False, "type": "boolean", "property": "hide_in_filter", "group": "visilibity"}
]

DOCUMENT_META_DEFAULTS = [
    {"default": True, "type": "boolean", "property": "allow_create", "group": "policy"}, 
    {"default": True, "type": "boolean", "property": "allow_list", "group": "policy"}, 
    {"default": True, "type": "boolean", "property": "allow_print", "group": "policy"}, 
    {"default": True, "type": "boolean", "property": "allow_send", "group": "policy"}, 
    {"default": True, "type": "boolean", "property": "allow_trash", "group": "policy"}, 
    {"default": True, "type": "boolean", "property": "allow_assignment", "group": "functionality"}, 
    {"default": True, "type": "boolean", "property": "allow_tagging", "group": "functionality"}, 
    {"default": True, "type": "boolean", "property": "allow_attachments", "group": "functionality"}, 
    {"default": True, "type": "boolean", "property": "allow_comments", "group": "functionality"}, 
    {"type": "list:string", "property": "search_fields", "group": "functionality"}, 
    {"default": 0, "type": "integer", "property": "level", "group": "security"}, 
    {"default": 0, "type": "integer", "property": "version", "group": "info"}, 
    {"type": "readonly", "property": "data_hash", "group": "info"}, 
    {"type": "readonly", "property": "definition_hash", "group": "info"}
]

#TODO 1: Implementar uma rotina de atualização para cada registro.

def definition_lookup(definition, name='definition', sep='.', ext='.json'):
    base = os.path.join(current.request.folder, 'modules', 'components')
    paths = definition.split('.')
    if not isinstance(paths, list):
        paths = [paths]
    paths += [name+ext]
    path = os.path.join(base, *paths) 
    if os.path.exists(path):
        return path

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
