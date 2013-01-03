#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 03/01/2013

@author: INFRA-PC1
'''

class PermissionError(Exception):
    """ Raised on Workflow Permission Error """
    
class WorkflowError(Exception):
    """ Raised when have error during workflow operation """