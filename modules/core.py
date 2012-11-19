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
    
    def __init__(self, config):
        
        from datamodel.document import Document, DocumentField, Tags, DocumentTag, DocumentComment
        
        self.config = config
        DataBase.__init__(self, config, [Document, DocumentField, Tags, DocumentTag, DocumentComment])
    
    def list_documents(self):
        return self().select(self.Document.ALL)
    
    def load_document(self, document_name):        
        row = self(self.Document.doc_name == document_name.lower()).select(self.Document.ALL).first()
        meta = DocumentMeta(self, **row.as_dict())
        self.define_datamodels([meta.datamodel()])
        return meta

    def get_document(self, document_name, data_id=None):
        meta = self.load_document(document_name)
        row = self[document_name][data_id] if data_id else meta
         
        return DocumentData(meta, **row.as_dict())
        

class DocumentMeta(Row):
    def __init__(self, db, *args, **kwargs):
        from helpers.properties import PropertyManager
        self._db = db
        Row.__init__(self, *args, **kwargs)
        
        PropertyManager(self, self.doc_meta)
        
        self.CHILDS = self._db(self._db.Document.doc_parent==self.id)
        self.DOC_FIELDS = self._db((self._db.DocumentField.document == self.id) & (self._db.DocumentField.df_type.belongs(fields.keys()))).select(self._db.DocumentField.ALL)
        map(lambda x, parent=self, proper=PropertyManager: (setattr(x, 'PARENT', parent), PropertyManager(x, x.df_meta)), self.DOC_FIELDS)
        
    def datamodel(self):
        from basemodel import BaseModel
        _fields = [fields[field.df_type].field(field) for field in self.DOC_FIELDS]
        
        class Document(BaseModel):
            __name__ = self.doc_name
            tablename = self.doc_tablename
            def set_properties(cls):
                cls.fields = _fields
                
        return Document

class DocumentData(Row):
    def __init__(self, meta, *args, **kwargs):
        self.META = meta
        Row.__init__(self, *args, **kwargs)
        self.COMMENTS = self.META._db((self.META._db.DocumentComment.document==self.META.id)&(self.META._db.DocumentComment.data_id==self.id))
        self.TAGS = self.META._db((self.META._db.DocumentTag.document==self.META.id)&(self.META._db.DocumentTag.data_id==self.id))
    
    def send_to_trash(self):
        self.update_record(is_active=False)
    
    def recover_from_trash(self):
        self.update_record(is_active=True)

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
