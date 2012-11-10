#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 02/10/2012

@author: INFRA-PC1
'''

from handlers.base import Base
from gluon.sqlhtml import SQLFORM
from gluon.storage import Storage, StorageList
from Magika import MGK
import os

class DocumentNotLoaded(Exception):
    pass

class DocumentFieldNotLoaded(Exception):
    pass

class DocumentDataNotLoaded(Exception):
    pass

class UnableToLoadDocumentData(Exception):
    pass
    
class Document(Base):
    def start(self):
        from datamodel.document import Document as DocumentModel
        from datamodel.document import DocumentField as DocumentFieldModel
        from datamodel.document import Tags
        from datamodel.document import DocumentTag
        from datamodel.document import DocumentComment
        
        self.DEFINITION_FILE = os.path.join(os.path.dirname(self.__file__), 'definition.json')
        self.DATA_FILE = os.path.join(os.path.dirname(self.__file__), 'data.json')
        
        self.app = MGK()
        self._db = self.app.db([DocumentModel, DocumentFieldModel, Tags, DocumentTag, DocumentComment], framework=True)
        self.auth = self.context.auth = self.app.auth
        self.meta = None
        self._parent = None
        self._data = None
        self.fields = Storage()
        self.childs = Storage()
        self.roles = StorageList()
        self.perms = StorageList()
        
        self.deps = []
        
        self.__dependecies = None        
        self.load_document()

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, parent):
        assert isinstance(parent, Document), '`parent` requires a instance of Document'
        self._parent = parent
    
    @property
    def table(self):
        if not self.meta:
            raise DocumentNotLoaded
        return self.db[self.meta.doc_name]
    
    @table.setter
    def table(self, value):
        raise ValueError, 'Unable to redefine table'

    @property
    def vtable(self):
        return self.define_virtual_table()
    
    @vtable.setter
    def vtable(self, value):
        raise ValueError, 'Unable to redefine virtual table'
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        raise ValueError, 'Unable to redefine data'
    
    def list_documents(self):
        return self._db(self._db.Document.id>0).select()

    def _load_definition(self):
        from helpers.document import load_definition
        from helpers import md5sum
        
        load_definition(self._db, self.DEFINITION_FILE)
        return md5sum(self.DEFINITION_FILE)
         
    def _load_default_data(self):
        from helpers.document import load_data
        from helpers import md5sum
        
        load_data(self._db, self.DATA_FILE)
        return md5sum(self.DATA_FILE)

    def _check_updates(self):
        from helpers import md5sum
        
        row = self._db(self._db.Document.doc_name==getattr(self, 'doc_name', None)).select().first()
        
        if row:
            if os.path.exists(self.DEFINITION_FILE):
                md5 = md5sum(self.DEFINITION_FILE)
                if md5!=row.doc_definition_hash:
                    self._load_definition()
                    row.update_record(doc_definition_hash = md5)
            if os.path.exists(self.DATA_FILE):
                md5 = md5sum(self.DATA_FILE)
                if md5!=row.doc_data_hash:
                    self._load_default_data()
                    row.update_record(doc_data_hash=md5)

    def _list_implicit_dependecies(self):
        deps = []
        if not self.fields: return deps
        for field in self.fields:
            if self.fields[field].meta.df_type in ('link', ):
                self.deps.append(self.fields[field].get_field_option('document'))
        return deps

    def exists(self, doc_name):
        return self._db(self._db.Document.doc_name==doc_name).count()>0
        
    def load_document(self, doc_name=''):
        doc_name = doc_name or getattr(self, 'doc_name', None)
        if not self.exists(doc_name):
            def_md5 = self._load_definition()
            dat_md5 = self._load_default_data()
            self._db(self._db.Document.doc_name==doc_name).select().first().update_record(doc_definition_hash=def_md5, doc_data_hash=dat_md5)
        else:
            self._check_updates()
        if doc_name and self.exists(doc_name)>0:
            if not getattr(self, 'doc_name', None):
                self.doc_name = doc_name
            self.meta = self._db(self._db.Document.doc_name==doc_name).select().first()
            if self.has_fields():
                self.load_fields()
            if self.has_childs():
                self.load_childs()
            self.__dependencies = self._list_implicit_dependecies()
            for dep in self.__dependencies:
                self.load_child(dep, self.meta.id, True)
            if self.has_fields() and self.has_childs():
                self.define_tables()

    def load_fields(self, field_names = [], doc_name='', in_field_list=True):
        if not self.meta:
            if not self.field_names and doc_name:
                raise DocumentNotLoaded
        fields = []
        
        if not field_names: 
            for field in self.list_fields():
                fields.append(self.load_field(field.df_name, doc_name, in_field_list))
        elif isinstance(field_names, basestring) and self.has_field(field_names):
            fields.append(self.load_field(field_names, doc_name, in_field_list))
        elif isinstance(field_names, (list, set)):
            for field_name in field_names:
                if self.has_childs(field_name):
                    fields.append(self.load_field(field_name, doc_name, in_field_list))
                else:
                    raise Exception, u'Unable to find field with name %s for document'%(`field_name`, `self.document.meta.doc_name`)
        else:
            raise Exception, u'Unable to find field with name %s for document %s'(`field_name`, `self.document.meta.doc_name`)
        return fields
    
    def has_fields(self):
        if not self.meta:
            return False
        return self.list_fields()>0
    
    def has_field(self, field_name, doc_name=''):
        if not self.meta:
            return False
        document = self._db.Document(self._db.Document.doc_name==doc_name) or self.meta
        return self._db(
            (self._db.DocumentField.document==document)&\
            (self._db.DocumentField.df_name==field_name)
        ).count()>0
    
    def load_field(self, field_name, doc_name='', in_field_list=True):
        if not self.meta or not self.has_field(field_name): 
            return
        document = self._db.Document(self._db.Document.doc_name==doc_name) or self.meta
        row = self._db(
            (self._db.DocumentField.document==document)&\
            (self._db.DocumentField.df_name==field_name)
        ).select().first()
        
        field = DocumentField(context=self.context)
        field.parent = self.meta
        field.load_doc_field(row.id)
        
        if in_field_list:    
            self.fields[row.df_name] = field
        
        return field
            
    def list_fields(self, only_active=True):
        if not self.meta and not self.has_fields(): 
            return []
        query = self._db.DocumentField.document==self.meta
        if only_active:
            query = query & (self._db.DocumentField.is_active==True)
        return self._db(query).select()
    
    def list_childs(self):
        if not self.meta and not self.has_childs():
            return []
        return self._db(self._db.DocumentField.doc_parent==self.meta)
    
    def has_childs(self):
        if not self.meta:
            return False
        return self._db(self._db.Document.doc_parent==self.meta).count()>0
        
    def has_child(self, child_name, doc_name=''):
        if not self.meta:
            return False
        doc_name = doc_name or self.meta.doc_name
        return self._db(
            (self._db.Document.doc_parent==doc_name)&\
            (self._db.Document.doc_name==child_name)
        ).count()>0
        
    def load_child(self, child_name, doc_name='', in_child_list=True):
        if not self.meta or not self.has_child(child_name, doc_name):
            return
        child = Document(context=self.context)
        child.parent = self._db.Document(self._db.Document.doc_name==doc_name) or self.meta
        child.doc_name = child_name
        child.load_document()
        if in_child_list:
            self.childs[child_name]=child
        return child 
        
    def load_childs(self, child_names=[], using=None, doc_name='', in_child_list=True):
        if not all(map(lambda x: not x, [child_names, doc_name, self.parent])):
            return
        
        childs = []
        
        if not child_names:
            for child in self.list_childs():
                childs.append(self.load_child(child.doc_name, doc_name, in_child_list))
        elif isinstance(child_names, basestring) and self.has_child(child_names, doc_name):
            childs.append(self.load_child(child_names, doc_name, in_child_list))
        elif isinstance(child_names, (list, set)):
            for child_name in child_names:
                if self.has_child(child_name, doc_name):
                    self.childs.append(self.load_child(child_name, doc_name, in_child_list))
                else:
                    raise Exception, u'Unable to find child with name %s for document'%('')
    
    @staticmethod
    def standardize_tag(tag):
        return str(tag).lower().capitalize()
    
    def _get_data_id(self, data_id=None):
        if not data_id and not self.data:
            raise DocumentDataNotLoaded
        return data_id if str(data_id).isdigit() else self.data.id
    
    def has_tags(self, data_id=None):
        data_id = self._get_data_id(data_id)
        return self._db((self._db.DocumentTags.document==self.meta.id)&(self._db.DocumentTag.data_id==data_id)).count()>0
    
    def has_tag(self, tag_name, data_id=None):
        data_id = self._get_data_id()
        if data_id:
            return self._db((self._db.Tags.tag_name.like('%'+Document.standardize_tag(tag_name)+'%'))&\
                            (self._db.DocumentTag.document==self.meta.id)&\
                            (self._db.DocumentTag.data_id==data_id)).count()>0
        return self._db(self._db.Tags.tag_name.like('%'+Document.standardize_tag(tag_name)+'%')).count()>0
        
    def list_tags(self, data_id=None):
        data_id = self._get_data_id(data_id)
        return [x.tag_name for x in self._db(
            (self._db.DocumentTag.document==self.meta.id)&\
            (self._db.DocumentTag.data_id==data_id)&\
            (self._db.DocumentTag.tag==self._db.Tags.id)).select(self._db.Tags.ALL)]
    
    def add_tag(self, tag_name, data_id=None):
        data_id = self._get_data_id(data_id)
        if not self.has_tag(tag_name, data_id):
            tag_id = self._db.Tags.insert(tag_name=Document.standardize_tag(tag_name))
        else:
            tag_id = self._db(self._db.Tags.tag_name.like('%'+Document.standardize_tag(tag_name)+'%')).select(self._db.Tags.id).first().id
        
        if self.data and not self.has_tag(tag_name, data_id):
            _id = self._db.DocumentTag.insert(document=self.meta.id, data_id=data_id, tag=tag_id)
            return _id
    
    def remove_tag(self, tag_name, data_id=None):
        data_id = self._get_data_id(data_id)
        if self.has_tag(tag_name):
            tag_id = self._db(self._db.Tags.tag_name.like('%'+Document.standardize_tag(tag_name)+'%')).select(self._db.Tags.id).first().id
            if self.has_tag(tag_name, data_id):
                self._db((self._db.DocumentTag.document==self.meta)&\
                         (self._db.DocumentTag.data_id==data_id)&\
                         (self._db.DocumentTag.tag==tag_id)).delete()
                return True
    
    def update_tags(self, tags, data_id=None):
        data_id = self._get_data_id(data_id)
        old_tags = self.list_tags(data_id)
        for tag in tags:
            if not tag in old_tags:
                self.add_tag(tag, data_id)
            else:
                old_tags.pop(tag)
                
        for tag in old_tags:
            self.remove_tag(tag, data_id)
            
    def has_comments(self, data_id=None):
        data_id = self._get_data_id(data_id)
        return self._db((self._db.DocumentComment.document==self.meta.id)&\
                        (self._db.DocumentComment.data_id==data_id)).count()>0

    def has_comment(self, comment, data_id=None):
        data_id = self._get_data_id(data_id)
        if not str(comment).isdigit():
            return self._db((self._db.DocumentComment.document==self.meta.id)&\
                        (self._db.DocumentComment.data_id==data_id)&\
                        (self._dn.DocumentComment.comment.like('%'+comment+'%'))
                        ).count()>0
        else:
            return self._db(self._db.DocumentComment.id==comment).count()>0 
                        
    def get_comment(self, comment, data_id=None):
        data_id = self._get_data_id(data_id)
        if self.has_comment(comment, data_id):
            if not str(comment).isdigit():
                row = self._db((self._db.DocumentComment.document==self.meta.id)&\
                         (self._db.DocumentComment.data_id==data_id)&\
                         (self._db.DocumentComment.comment.like('%'+comment+'%'))).select().first()
            else:
                row = self._db(self._db.DocumentComment.id==comment).select().first()
            return row
        
    def remove_comment(self, comment, data_id=None):
        data_id = self._get_data_id(data_id)
        if self.has_comment(comment, data_id):
            row = self.get_comment(comment, data_id)
            self._db(self._db.DocumentComment.id==row.id).delete()
            return True
        
    def add_comment(self, comment, data_id=None):
        data_id = self._get_data_id(data_id)
        if not self.has_comment(comment, data_id):
            self._db.DocumentComment.insert(
                    document=self.meta.id,
                    data_id=data_id,
                    comment=comment)
            return True
    
    def update_comment(self, comment, data_id=None):
        data_id = self._get_data_id(data_id)
        row = self.get_comment(comment, data_id)
        if not row:
            raise ValueError, u'Unable to update comment with data_id = %s'%`data_id`
        else:
            row.update_record(comment=comment)
    
    def has_files(self, data_id):
        data_id = self._get_data_id(data_id)
        return self._db((self._db.DocumentFile.document==self.meta.document)&\
                        (self._db.DocumentFile.data_id==data_id)).count()>0
                        
    def has_file(self, file_id, data_id=None):
        data_id = self._get_data_id(data_id)
        return self._db((self._db.DocumentField.document==self.meta.document)&\
                        (self._db.DocumentField.data_id==data_id)&\
                        (self._db.DocumentField.file==file_id)).count()>0
    
    def list_files(self, data_id=None):
        data_id = self._get_data_id(data_id)
        return dict([(row[self._db.DocumentFile].id, row[self._db.Files].title) for row in self._db(
            self._db.DocumentFile.document==self.meta.id)&\
            self._db.DocumentFile.data_id==data_id]&\
            self._db.DocumentFile.file==self._db.Files.id).select(self._db.DocumetFile.id, self._db.Files.title)
    
    def add_file(self, file_id, data_id=None):
        data_id = self._get_data_id(data_id)
        if not self.has_file(file_id, data_id):
            _id = self._db.DocumentFiles.insert(document=self.meta.id, data_id=data_id, file=file_id)
            return _id 
            
    def remove_file(self, file_id, data_id=None):
        data_id = self._get_data_id(data_id)
        if self.has_file(file_id, data_id):
            self._db((self._db.DocumentFile.document==self.meta.id)&\
                     (self._db.DocumentFile.data_id==data_id)&\
                     (self._db.DocumentFile.file==file_id)).delete()
            return True
    
    def define_tables(self):
        tables = [self.define_table()]
        [tables.append(child.define_table()) for child in self.childs.values()]
        
        self.db = self.app.db(tables)       
    
    def define_table(self):
        if not self.meta:
            raise DocumentNotLoaded
        class Model(Base):
            __name__ = self.meta.doc_name
            tablename = self.meta.doc_tablename
            fields = self.define_fields()
            visibility = self.define_visibility()
            validations = self.define_validations()
            labels = self.define_labels()
            representation = self.define_representation()
        return Model
    
    def define_virtual_table(self):
        from gluon.dal import Table, DAL
        [self.fields[x].field for x in self.fields]
        table = Table(
            DAL(None),
            self.meta.doc_name,
            *[self.fields[x]._field for x in self.fields]
        )
        return table
    
    def define_fields(self, with_form_fields=False):
        if not self.meta:
            raise DocumentNotLoaded
        fields = []
        for field in self.fields.values():
            if field.meta:
                if not with_form_fields and self.meta.df_type!='virtual':
                    fields.append(field)
                elif with_form_fields:
                    fields.append(field)
        if fields:
            from gluon.dal import Field
            fields.append(Field('status', 'integer'))
        return fields
    
    def define_visibility(self):
        if not self.meta:
            raise DocumentNotLoaded
        
        visibility = {}
        for field in self.fields.keys():
            visibility[field] = self.fields[field].define_field_visibility(field)
        
        return visibility
    
    def define_validations(self):
        if not self.meta:
            raise DocumentNotLoaded
        
        validations = {}
        
        for field in self.fields.keys():
            validations[field] = self.fields[field].define_field_validations()

    def define_labels(self):
        if not self.meta:
            raise DocumentNotLoaded
        
        from gluon import current
        
        labels = {}
        
        for field in self.fields.keys():
            label = self.fields[field].define_field_label()
            if label:
                labels[field] = current.T(label)
            
        return labels()
    
    def define_representation(self):
        if not self.meta:
            raise DocumentNotLoaded
        
        representation = {}
        
        for field in self.fields:
            representation[field] = self.fields[field].define_field_representation()
            
        return representation
    
    def define_comments(self):
        if not self.meta:
            raise DocumentNotLoaded
        
        comments = {}
        
        for field in self.fields:
            comments[field] = self.fields[field].define_field_comments()
        
        return comments
    
    def define_widgets(self):
        if not self.meta:
            raise DocumentNotLoaded
        
        widgets = {}
        
        for field in self.fields:
            widgets[field] = field.define_field_widget()
        
        return widgets
    
    def load_data(self, data_id=None, parent_id=None):
        if not any([data_id, parent_id, self.request.args]):
            raise UnableToLoadDocumentData
        if data_id or self.request.args:
            data_id = data_id or self.request.args[0]
            self._data = self.db(self.table.id==data_id)
        if parent_id:
            self._data = self.db(self.table.doc_parent==parent_id) 
        for child in self.childs:
            self.childs[child].load_data(parent_id=self.data.id)
    
    def create(self):
        from helpers.widgets import Document as FORM
        self.context.form = FORM(self)
    
    def show(self):
        self.context.document = self.meta
        
    def update(self):
        self.context.form = SQLFORM(self._db.Document, self.meta).process()
    
    def delete(self):
        self._db(self._db.Document.id==self.meta.id).delete()
        
    def list(self):
        self.context.documents = self.list_documents()
        
class DocumentField(Base):
    def start(self):
        from datamodel.document import Document as DocumentModel
        from datamodel.document import DocumentField as DocumentFieldModel
        
        self.app = MGK()
        self._db = self.app.db([DocumentModel, DocumentFieldModel], framework=True)
        self.auth = self.context.auth = self.app.auth
        self._parent = None
        self._field = None
        self.meta = None
        self.meta_type = None
        self.meta_validators = None  

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, parent):
        self._parent = parent
    @property
    def field(self):
        return self.define_field()
    
    @field.setter
    def field(self, value):
        raise AttributeError, 'Unable to redefine field'
    
    @property
    def vfield(self):
        return self.bluid_virtual_field()
    
    @vfield.setter
    def vfield(self, value):
        raise AttributeError, 'Unable to redefine field'

    def list_doc_fields(self):
        if not self._parent:
            query = (self._db.DocumentField.id)
        else:
            query = (self._db.DocumentField.document==self.parent)
        return self._db(query).select()
    
    def exist(self, df_name, document=''):
        if not self.parent and not document:
            raise Exception, u'Unable to check for `doc_field` without `document` or `parent`'
        document = self._db.Document(document) or self.parent
        return self._db(self._db.DocumentField.document==document).count()>0
    
    def load_doc_field(self, df_id=None, df_name='', document=''):
        from helpers.manager import ValidatorList, TypeManager
        assert any([df_id, df_name, document]), u'Unable for load `doc_field` without and `df_id` or `df_name` and `document`'
        #assert all(map(lambda x: not x, [self.parent, df_id])) and all([df_name, document]), u'Unable for load `doc_field` with an `df_name` and without `doc_name` or `parent`'

        if df_id:
            self.meta = self._db.DocumentField(df_id)
        else:
            document = self._db.Document(self._db.Document.doc_name==document) or self.parent
            if self.exist(df_name, document):
                self.meta = self._db(
                    (self._db.DocumentField.document==document)&\
                    (self._db.DocumentField.df_name==df_name)
                ).select().first()
            else:
                raise Exception('Unable to load %s'%(('doc_field `%s`'%df_id) if df_id else 'doc_field %s for document %s'%(`df_name`, `document.doc_name`)))
        
        self.meta_type = TypeManager(self.meta.df_type, self.meta.df_typemeta)
        self.meta_validators = ValidatorList(self.meta.df_validatorsmeta)
        
    def define_field(self):
        if not self.meta:
            raise DocumentFieldNotLoaded
        
        from gluon.dal import Field
        from helpers.document import policy_unique, policy_required
        
        if not self._field:
            self._field = Field(
                self.meta.df_name, 
                self.meta.df_type, 
                unique = policy_unique in self.meta.df_policy,
                required = policy_required in self.meta.df_policy,
                length=self.meta.df_length,
                default=self.meta.df_default,
            )
        return self._field
        
    def define_field_visibility(self):
        if not self.meta:
            raise DocumentFieldNotLoaded
        
        from helpers.document import policy_readable, policy_writable
        
        readable = policy_readable in self.meta.df_policy
        writable = policy_writable in self.meta.df_policy
        
        return (readable, writable)
    
    def define_field_validations(self):
        if not self.meta:
            raise DocumentFieldNotLoaded
        
        return self.meta_validators.validators()

    def define_field_label(self):
        if not self.meta:
            raise DocumentFieldNotLoaded
        
        return self.meta.df_label
             
    def define_field_representation(self):
        if not self.meta:
            raise DocumentFieldNotLoaded
        
        if self.meta.df_represent.startswith('eval:'):
            return eval(self.meta.df_represent.replace('eval:', ''))
        else:
            return self.meta.df_represent
    
    def define_field_widget(self):
        from helpers.widgets import widgets
        
        if not self.meta:
            raise DocumentFieldNotLoaded
        
        if getattr(self.meta, "df_widget", None):
            return widgets[self.meta.df_widget]
        else:
            return widgets[self.meta.df_type]
    
    def define_field_comments(self):
        if not self.meta:
            raise DocumentFieldNotLoaded
        return self.meta.df_description or ''
    
    def build_virtual_field(self):
        if not self._vfield:
            self._vfield = self.define_field()
            self._vfield.readable, self._vfield.writable = self.define_field_visibility()
            self._vfield.represent = self.define_field_representation()
            self._vfield.label = self.define_field_label()
            self._vfield.comments = self.define_field_comments()
            self._vfield.requires = self.define_field_validations()
        return self._vfield
    
    def has_field_options(self):
        if not self.meta:
            raise DocumentFieldNotLoaded
        return self.meta_type.has_options()
    
    def get_field_options(self):
        if self.has_field_options():
            return self.meta_type.get_options()
        
    def get_field_option(self, option, default=None):
        if self.has_field_options():
            return self.meta_type.get_option(option, default)
    
    def create(self):
        self.context.form = SQLFORM(self._db.DocumentField).process()
    
    def show(self):
        self.context.doc_field = self.meta
    
    def update(self):
        self._db(self._db.DocumentField.id==self.meta.id).delete()
        
    def list(self):
        self.context.documents = self.list_doc_fields() 