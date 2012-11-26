#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 22/11/2012

@author: INFRA-PC1
'''

from core import Core
from helpers.widgets import widgets
from helpers.document import types
from gluon.html import *

class Editor(object):
        
    def __init__(self):
        self.core = Core()
        self.db = self.core.db()
        self.document = self.db.get_document('document')

    def options_composer(self, options):
        widgets = []
        for option in options:
            widgets.append(LABEL(option.label, _class='control-label', _for=option.name, requires=option.requires))
            widgets.append(INPUT(_type='text', _name=option.name, _class=option.type, _class='input-large'))
        return FORM(
            DIV(
                *widgets,
                _class='controls'
            ),
            _class='form'
        ).xml()
    
    def template_composer(self, widget):
        from gluon.dal import Row
    
    def widget_composer(self, widget):
        options = self.options_composer(types[widget].options)
        template = self.template_composer(widget)
        return DIV(
            template,
            _class='control-group component',
            _rel = 'popover',
            _title = types[widget].label,
            _trigger = 'manual',
            **{
               '_data-type': widget,
               '_data-content': options
               }
        )