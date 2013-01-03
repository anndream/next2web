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
from gluon.validators import *
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
    
    DURATIONS = (
        (SECOND, T('Second(s)')),
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
            Field('from_state', 'reference tabWorkflowState'),
            Field('to_state', 'reference tabWorkflowState'),
            Field('roles', 'list:reference tabWorkflowRoles')
        ]
        
class EventType(BaseModel):
    tablename = 'tabWorkflowEventType'
    def set_properties(self):
        self.fields = [
            Field('name', 'string', notnull=True, required=True),
            Field('description', 'text', lenght=255)
        ]
        
class Event(BaseModel):
    tablename = 'tabWorkflowEvent'
    def set_properties(self):
        self.fields = [
            Field('name', 'string', notnull=True, required=True),
            Field('description', 'text'),
            Field('workflow', 'reference tabWorkflow', required=True, notnull=True),
            Field('state', 'reference tabWorkflowState', required=True, notnull=True),
            Field('roles', 'list:reference tabWorkflowRole'),
            Field('event_types', 'list:reference tabWorkflowEventType'),
            Field('is_mandatory', 'boolean', default=False),
        ]

class DocumentWorkflowActivity(BaseModel):
    tablename = 'tabDocumentWorkflowActivity'
    def set_properties(self):
        self.fields = [
            Field('document', 'reference tabDocument'),
            Field('doc_parent', 'reference tabDocument'),
            Field('workflow', 'reference tabWorkflow'),
            Field('started_on', 'datetime'),
            Field('completed_on', 'datetime')
        ]
        
class Participant(BaseModel):
    tablename = 'tabWorkflowParticipant'
    def set_properties(self):
        self.fields = [
            Field('user', 'reference auth_user', notnull=True, required=True),
            Field('roles', 'list:reference tabWorkflowRole'),
            Field('disabled', 'boolean', default=False)
        ]

class WorkflowHistory(BaseModel):
    tablename = 'tabWorkflowHistory'
    TRANSITION = 1
    EVENT = 2
    ROLE = 3
    COMMENT = 4
    
    TYPE_ROLE_LIST = (
            (TRANSITION, T('Transition')),
            (EVENT, T('Event')),
            (ROLE, T('Role')),
            (COMMENT, T('Comment'))
            )
    
    def set_properties(self):
        self.fields = [
            Field('worflowactivity', 'reference tabWorkflowActivity'),
            Field('log_type', 'integer', notnull=True, required=True, requires=IS_IN_SET(self.TYPE_ROLE_LIST)),
            Field('state', 'reference tabWorkflowState', required=True, notnull=True),
            Field('transition', 'reference tabWorkflowTransition', required=True, notnull=True),
            Field('event', 'reference tabWorkflowTransition', required=True, notnull=True),
            Field('participant', 'reference tabWorkflowParticipant', required=True, notnull=True),
        ]
        
class Notification(BaseModel):
    tablename = 'tabWorkflowNotification'
    TRANSITION = 1
    EVENT = 2
    ROLE = 3
    COMMENT = 4
    
    TYPE_ROLE_LIST = (
        (TRANSITION, T('Transition')),
        (EVENT, T('Event')),
        (ROLE, T('Role')),
        (COMMENT, T('Comment'))
    )
    
    def set_properties(self):
        self.fields = [
            Field('workflowactivity', 'reference tabWorkflowActivity'),
            Field('log_type', 'integer', notnull=True, required=True, requires=IS_IN_SET(self.TYPE_ROLE_LIST)),
            Field('states', 'list:reference tabWorkflowState'),
            Field('transitions', 'list:reference tabWorkflowTransition'),
            Field('events', 'list:reference tabWorkflowTransition'),
            Field('roles', 'list:reference tabWorkflowRoles'),
            Field('participants', 'list:reference tabWorkflowParticipant'),
            Field('message', 'text')
        ]
    
    