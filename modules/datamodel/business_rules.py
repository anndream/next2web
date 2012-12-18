#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 12/12/2012

@author: INFRA-PC1
'''

from gluon.dal import Field
from basemodel import BaseModel
from gluon.validators import *
from gluon.html import XML
from gluon import current

class Rule(BaseModel):
    