#-*- coding: utf-8 -*-
#!/usr/bin/env python

from gluon.dal import Field
from basemodel import BaseModel
from gluon.validators import *
from gluon.html import XML
from gluon import current

T=current.T

from helpers.document import types

class Document(BaseModel):
    tablename = 'tabDocument'
    def set_properties(self):
        from gluon.contrib.simplejson import loads, dumps
        
        filter_in = lambda obj, dumps=dumps: dumps(obj) if obj else {}
        filter_out = lambda txt, loads=loads: loads(txt) if txt else ''
        
        self.fields = [
            Field('doc_name', unique=True, notnull=True),
            Field('doc_title', notnull=True),
            Field('doc_description', 'text'),
            Field('doc_parent', 'reference tabDocument'),
            Field('doc_parent_id', 'integer'),
            Field('doc_tablename', 'string', notnull=True),
            Field('doc_meta', 'text', filter_in = filter_in, filter_out = filter_out),
        ]
            
class DocumentField(BaseModel):
    tablename = 'tabDocumentField'
    def set_properties(self):
        from gluon.contrib.simplejson import loads, dumps
        
        filter_in = lambda obj, dumps=dumps: dumps(obj) if obj else {}
        filter_out = lambda txt, loads=loads: loads(txt) if txt else ''
        
        self.fields = [
            Field('document', 'reference tabDocument', notnull=True),
            Field('doc_parent', 'reference tabDocument'),
            Field('doc_parent_id', 'integer'),
            Field('idx', 'integer', notnull=True, default=1),
            Field('df_name', 'string', notnull=True),
            Field('df_type', 'string', notnull=True),
            Field('df_label', 'string', notnull=False),
            Field('df_description', 'text'),
            Field('df_default', 'text', filter_in = filter_in, filter_out = filter_out),
            Field('df_meta', 'text', filter_in = filter_in, filter_out = filter_out)
        ]
    def set_validators(self):
        self.validators = {
            'df_name': IS_NOT_EMPTY(),
            'df_type': IS_IN_SET(types.keys()),
        } 
    
    def _set_comments(self):
        
        self.entity.df_default.comment = XML(
            '<b>n</b>: An value<br/>'\
            '<b>eval:lambda n: int(n)</b>: An lambda or function to be evaluated on insert or update'
        )
                
        self.entity.df_width.comment = XML(
            '<b><i>n</i>px</b>: Absolute width of Widget in pixels <br/>'\
            '<b><i>n</i>%</b>: Relative width of Widget in percents <br/>'
        )
      
class Tags(BaseModel):
    tablename = 'tabTags'
    def set_properties(self):
        self.fields = [
            Field('tag_name', 'string', notnull=True, required=True)
        ]
        
class DocumentTag(BaseModel):
    tablename = 'tabDocumentTag'
    def set_properties(self):
        self.fields = [
            Field('document', 'reference tabTags', notnull=True, required=True),
            Field('data_id', 'integer', notnull=True, required=True),
            Field('tag', 'reference tabDocumentTags', notnull=True, required=True)
        ]
        
class DocumentComment(BaseModel):
    tablename = 'tabDocumentComment'
    def set_properties(self):
        self.fields = [
            Field('document', 'reference tabDocument', notnull=True, required=True),
            Field('data_id', 'integer', notnull=True, required=True),
            Field('comment', 'text', notnull=True, length = 255)
        ]
    
    
class File(BaseModel):
    tablename = 'tabFiles'
    def set_properties(self):
        self.fields = [
            Field('title', 'string', length=255, notnull=True),
            Field('filename', 'string', length=255, notnull=True),
            Field('path', 'upload', notnull=True),
            Field('contenttype', 'string', notnull=True)
        ]
        
class DocumentFile(BaseModel):
    tablename = 'tabDocumentFile'
    def set_properties(self):
        self.fields = [
            Field('document', 'reference tabDocument', notnull=True, required=True),
            Field('data_id', 'integer', notnull=True, required=True),
            Field('file', 'integer', notnull=True)
        ]