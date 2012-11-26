#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 17/10/2012

@author: INFRA-PC1
'''

#-*- coding: utf-8 -*-
#!/usr/bin/env python

from gluon.dal import Field
from basemodel import BaseModel
from gluon import current
from gluon.storage import Storage

T = current

class WorkflowRoles(BaseModel):
    tablename='tabWorkflowRoles'
    def set_properties(self):
        self.fields = [
            Field('name', 'string', length=64),
            Field('description', 'text')
        ]
        
class Workflow(BaseModel):
    tablename='tabWorkflow'
    DRAFTED, CREATED, REMOVED = range(3)
    STATUS_CHOICE_LIST = ((DRAFTED, T('Drafted')),
                          (CREATED, T('Created')),
                          (REMOVED, T('Removed')))
    
    errors = Storage(workflow=[], states=Storage(), trasitions=Storage())
    
    def set_properties(self):
        from gluon.validators import IS_IN_SET
        self.fields = [
            Field('name', 'status', length=128),
            Field('description', 'text'),
            Field('status', 'integer', required=IS_IN_SET(self.STATUS_CHOICE_LIST))
            
        ]
        
class State(BaseModel):
    tablename = 'tabWorkflowState'
    SECOND = 1
    MINUTE = SECOND * 60
    HOUR = MINUTE * 60
    DAY =  HOUR * 24
    WEEK = DAY * 7
    MONTH = DAY * 30
    
    DURATIONS = ((SECOND, T('Second(s)')),
                 (MINUTE, T('Minute(s)')),
                 (HOUR, T('Hour(s)')),
                 (DAY, T('Day(s)')),
                 (WEEK, T('Week(s)')),
                 (MONTH, T('Month(s)'))
                )
    START, END = range(2)
    TYPE_CHOICES_LIST = ((START, T('Start')),
                          (END, T('End')))
    
    def set_properties(self):
        self.fields = [
            Field('workflow', 'reference tabWorkflow', required=True),
            Field('name', 'string', length=256),
            Field('description', 'text'),
            Field('type', 'integer'),
            Field('roles', 'list:reference tabWorkflowRole'),
            Field('estimation_value', 'integer', default=0),
            Field('estimation_unit', 'integer', default=self.DAY)
        ]
    
    def set_validations(self):
        from gluon.validators import IS_EMPTY_OR, IS_IN_SET
        self.entity.type.requires = IS_EMPTY_OR(IS_IN_SET(self.TYPE_CHOICES_LIST))
        self.entity.estimation_unit.requires = IS_IN_SET(self.DURATIONS)
        
    def set_labels(self):
        self.entity.name.label = T('State Name'),
        self.entity.description.label = T('Description'),
        self.entity.type.label = T('State Type'),
        self.entity.estimation_unit.label = T('Estimation Unit')
        
    def set_comments(self):
        from gluon.html import XML
        self.entity.type.comments = XML('<span class="help-block">%s <small class="warning">%s</small></span>'%(T('Select "start" if this is the initial state'), 
                                                                              T('There can only be only an initial state for each workflow')))
        self.entity.estimation_value.comments = XML('<span class="help-block">%s</span>'%(T('Use whole numbers')))
        self.entity.estimation_unit.comments = XML('<span class="help-block">%s</span>'%(T('Estimation Unit of Time')))
        
class Transition(BaseModel):
    tablename = 'tabWorkflowTransition'
    def set_properties(self):
        self.fields = [
            Field('workflow', 'reference tabWorkflow'),
            Field('name', 'string', length=128),
            Field('from_state', 'string')
        ]