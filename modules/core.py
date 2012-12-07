# -*- coding: utf-8 -*-

###############################################################################
# web2py modelless scaffold app
# Bruno Cezar Rocha <rochacbruno@gmail.com>
#
# This is the base of the app
# it acts like a proxy for the rest of the application
#
# Why subclassing Auth, DAL, Mail etc?
# 1. Because you can reuse the code better
# 2. Because you can have self configured instances ready to use
# 3. Because it is a way to change or replace some default behaviour when needed
#
###############################################################################

from gluon.tools import Auth, Crud, Mail
from gluon.dal import DAL, Row
from helpers.field import fields
from datamodel.user import User
from gluon.storage import Storage
from gluon import current

adapters = Storage()

class AdapterNotFound(Exception):
    pass

def register_adapter(doc_name, adapter):
    if not doc_name in adapters.keys():
        adapters[doc_name] = adapter
        
def get_adapter(doc_name, default=None):
    if doc_name in adapters:
        return adapters[doc_name]
    elif default:
        return default
    raise AdapterNotFound(doc_name)

class Core(object):
    def __init__(self):
        self.session, self.request, self.response, self.T = \
            current.session, current.request, current.response, current.T
        self.config = Storage(db=Storage(),
                              auth=Storage(),
                              crud=Storage(),
                              mail=Storage())
        # Global app configs
        # here you can choose to load and parse your configs
        # from JSON, XML, INI or db
        # Also you can put configs in a cache
        #### -- LOADING CONFIGS -- ####
        self.config.db.uri = "sqlite://storage.sqlite"
        self.config.db.migrate = True
        self.config.db.migrate_enabled = True
        self.config.db.check_reserved = [] #'all'
        #if not self.config.db.common_fields:
        #    self.config.db.common_fields = []
        #self.config.db.common_fields.append(self.auth.signature)
        self.config.auth.server = "default"
        self.config.auth.formstyle = "bootstrap"
        self.config.mail.server = "logging"
        self.config.mail.sender = "me@mydomain.com"
        self.config.mail.login = "me:1234"
        self.config.crud.formstyle = "bootstrap"
        #### -- CONFIGS LOADED -- ####

    def db(self, datamodels=None, framework=False):
        # here we need to avoid redefinition of db
        # and allow the inclusion of new entities
        if framework:
            self.config.db.check_reserved = []
        if not hasattr(self, "_db"):
            self._db = LDS(self.config)
        if datamodels:
            self._db.define_datamodels(datamodels)
        return self._db

    @property
    def auth(self):
        # avoid redefinition of Auth
        # here you can also include logic to del
        # with facebook based in session, request, response
        if not hasattr(self, "_auth"):
            self._auth = Account(self.db())
        return self._auth

    @property
    def crud(self):
        # avoid redefinition of Crud
        if not hasattr(self, "_crud"):
            self._crud = FormCreator(self.db())
        return self._crud

    @property
    def mail(self):
        # avoid redefinition of Mail
        if not hasattr(self, "_mail"):
            self._mail = Mailer(self.config)
        return self._mail

class DataBase(DAL):
    """
    Subclass of DAL
    auto configured based in config Storage object
    auto instantiate datamodels
    """
    _lazy_tables={}
    _tables = {}
    def __init__(self, config, datamodels=None):
        self.config = config
        DAL.__init__(self, **config.db)

        if datamodels:
            self.define_datamodels(datamodels)

    def define_datamodels(self, datamodels):
        # Datamodels will define tables
        # datamodel ClassName becomes db attribute
        # so you can do
        # db.MyEntity.insert(**values)
        # db.MyEntity(value="some")
        for datamodel in datamodels:
            if hasattr(self, datamodel.__name__):
                return
            obj = datamodel(self)
            self.__setattr__(datamodel.__name__, obj.entity)
            if obj.__class__.__name__ == "Account":
                self.__setattr__("auth", obj)

class LDS(DataBase):
    """
    Level Document Structure and Datata Access Layer
    Subclass of DataBase
    auto configured based in config Storage object
    auto instantiate datamodels from database
    """
    _lazy_tables = {}
    _tables = {}
    _documents_and_datamodels = {}
    
    def __init__(self, config):
        from gluon import Field
        from datamodel.document import Document, DocumentField, Tags, DocumentTag, DocumentComment, File, DocumentFile
                
        self.config = config
        #self.config.common_fields.append(
        #    Field('idx', 'integer', notnull=True, required=True),
        #    Field('document', 'reference tabDocument', notnull=True, required=True),
        #   Field('doc_parent', 'reference tabDocument'),
        #   Field('doc_parent_id', 'integer')
        #)
        DataBase.__init__(self, config, [])
        self.define_datamodels({'document': Document, 'documentfield': DocumentField, 'tags': Tags, 'documenttag': DocumentTag, 'documentcomment': DocumentComment, 'files': File, 'documentfile': DocumentFile })
    
    def __getitem__(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        elif hasattr(self, self.datamodel(key)):
            return getattr(self, self.datamodel(key))
        elif default:
            return default
        else:
            raise KeyError(key)
    
    def datamodel(self, document_name):
        return self._documents_and_datamodels.get(document_name, None)
    
    def define_datamodels(self, datamodels):
        # Datamodels will define tables
        # datamodel ClassName becomes db attribute
        # so you can do
        # db.MyEntity.insert(**values)
        # db.MyEntity(value="some")
        for document in datamodels:
            datamodel = datamodels[document]
            if hasattr(self, datamodel.__name__):
                return
            obj = datamodel(self)
            self.__setattr__(datamodel.__name__, obj.entity)
            self._documents_and_datamodels[document] = datamodel.__name__
            if obj.__class__.__name__ == "Account":
                self.__setattr__("auth", obj)
    
    def _check_update(self, doc_name, definition):
        from helpers import md5sum
        from helpers.document import load_definition, definition_lookup
        
        path = definition_lookup(definition)
        
        md5 = md5sum(path)
        if not self.has_document(doc_name):
            load_definition(self, path)
            row = self.load_document(doc_name)
            row.update_property('info', 'definition_hash', md5)
        else:
            row = self.load_document(doc_name)
            if md5!=row.property('info', 'definition_hash'):
                #load_definition(self, path)
                row.update_property('info', 'definition_hash', md5)
    
    def has_document(self, document_name):
        return self(self.Document.doc_name == document_name.lower()).count()>0
    
    def get_document_name_from_table(self, tablename):
        document_row = self(self.Document.doc_tablename==tablename).select().first()
        if document_row:
            return document_row['doc_name']
        else:
            return None
    
    def list_documents(self):
        return self().select(self.Document.ALL)
    
    def load_document(self, document_name):        
        from gluon.dal import RecordUpdater, RecordDeleter
        row = self(self.Document.doc_name == document_name.lower()).select(self.Document.ALL).first() or Row({'id':None})
        meta = DocumentMeta(self, **row.as_dict())
        
        if getattr(meta, "doc_istable", False):
            self.define_datamodels([{document_name:meta.datamodel()}])
            meta.update_meta = RecordUpdater(meta, self[self.datamodel(document_name)], meta.id)
            meta.delete_meta = RecordDeleter(self[self.datamodel(document_name)], meta.id)
        
        return meta

    def get_document(self, document_name, data_id=None):
        from gluon.dal import RecordUpdater
        
        meta = self.load_document(document_name)
        row = self[document_name][data_id] if data_id else Row({'id':None})
                    
        adapter = get_adapter(document_name, DocumentData)
        
        document = adapter(meta, **row.as_dict())
        document.update_document = RecordUpdater(document, self[document_name], document.id)
        
        return document
    
    def get_document_childs(self, childname, doc_parent, doc_parent_id):
        from gluon.dal import RecordUpdater
        
        meta = self.load_document(childname)
        childs = self((self[childname].document==meta.id)&
                         (self[childname].doc_parent==doc_parent)&
                         (self[childname].doc_parent_id==doc_parent_id)).select(self[childname].ALL)
        
        adapter = get_adapter(childname, DocumentData)
        
        childs = map(lambda x: adapter(meta, **x), childs)                 
        map(lambda x: (x.__setitem__('__saved', (True, x.id)), x.setattr('update_document', RecordUpdater(x, self[childname], x.id))), childs)
        return childs

    def store_files(self, files):
        stored = []
        for title, filename, filedata in files:
            stored.append(self.store_file(title, filename, filedata))
        return stored
        
    def store_file(self, title, filename, filedata):
        return self.File.insert({
            'title': title,
            'filename': filename,
            'path': self.File.path.store(filedata)
        })
        
        
class DocumentMeta(Row):
    def __init__(self, db, *args, **kwargs):
        from helpers.properties import PropertyManager, PMDocumentField
        self._db = db
        Row.__init__(self, *args, **kwargs)
        
        self.DOC_FIELDS = self._db((self._db.DocumentField.document == 2)&
                                   (self._db.DocumentField.doc_parent==self.id)&
                                   (self._db.DocumentField.doc_parent_id==self.id)).select(self._db.DocumentField.ALL, orderby=self._db.DocumentField.idx) #& (self._db.DocumentField.df_type.belongs(fields.keys()))
        
        map(lambda x: (setattr(x, 'PARENT', self), PropertyManager(x, x.df_meta)), self.DOC_FIELDS)
        
        PropertyManager(self, self.doc_meta)

    @property
    def _DOC_FIELDS(self):
        if not hasattr(self, '__doc_fields'):
            self.__doc_fields = self._db.get_document_childs('documentfield', self.id, self.id)
        return self.__doc_fields        

    def exist_doc_field(self, df_name):
        return len(filter(lambda x: x.df_name==df_name, self.DOC_FIELDS))>0        

    def get_doc_field(self, df_name):
        if self.exist_doc_field(df_name):
            return filter(lambda x: x.df_name==df_name, self.DOC_FIELDS)[0]
        raise ValueError('DocField %s does not exists in document %s'%(`df_name`, `self.doc_name`))

    def get_df_title(self, df_name):
        if self.exist_doc_field(df_name):
            df = self.get_doc_field(df_name)
            return df.df_title or df.df_name
        raise ValueError('DocField %s does not exists in document %s'%(`df_name`, `self.doc_name`))
        
    def datamodel(self):
        from basemodel import BaseModel
        _fields = [fields[field.df_type].field(field) for field in self.DOC_FIELDS if field.df_type in fields.keys()]
        
        class Document(BaseModel):
            __name__ = self.doc_name
            tablename = self.doc_tablename
            def set_properties(self):
                self.fields = _fields
                
        return Document

class DocumentData(Row):
    def __init__(self, meta, *args, **kwargs):
        self.META = meta
        Row.__init__(self, *args, **kwargs)
        self['__saved'] = (True, self['id'])
    
    def save(self):
        if not hasattr(self, 'id'):
            _id = self.META._db[self.META.df_tablename].validate_and_insert(**self.__dict__)
            if _id:
                self.id = _id
        else:
            self.update_document(**self.__dict__)
        return self
    
    def send_to_trash(self):
        self.update_document(is_active=False)
        
    delete_document = send_to_trash
    
    def recover_from_trash(self):
        self.update_document(is_active=True)
        
    def _property(self, group, name, default=None):
        if self.has_key('df_default') or self.has_key('doc_default'):
            if self.has_key('df_default'):
                defaults = self['df_default'] or self.META.get_doc_field('df_default').df_meta
        
class DocFieldLazy(Row):
    def __init__(self, meta, *args, **kwargs):
        self.META = meta

class Account(Auth):
    """Auto configured Auth"""
    def __init__(self, db):
        self.db = db
        self.hmac_key = Auth.get_or_create_key()
        Auth.__init__(self, self.db, hmac_key=self.hmac_key)
        user = User(self)
        self.entity = user.entity

        # READ AUTH CONFIGURATION FROM CONFIG
        self.settings.formstyle = self.db.config.auth.formstyle
        if self.db.config.auth.server == "default":
            self.settings.mailer = Mailer(self.db.config)
        else:
            self.settings.mailer.server = self.db.config.auth.server
            self.settings.mailer.sender = self.db.config.auth.sender
            self.settings.mailer.login = self.db.config.auth.login


class Mailer(Mail):
    def __init__(self, config):
        Mail.__init__(self)
        self.settings.server = config.mail.server
        self.settings.sender = config.mail.sender
        self.settings.login = config.mail.login


class FormCreator(Crud):
    def __init__(self, db):
        Crud.__init__(db)
        self.settings.auth = None
        self.settings.formstyle = self.db.config.crud.formstyle
