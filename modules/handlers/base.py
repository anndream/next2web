# -*- coding: utf-8 -*-


###############################################################################
# web2py modelless scaffold app
# Bruno Cezar Rocha <rochacbruno@gmail.com>
#
# Base handler for controller handlers
###############################################################################

from gluon import URL
from gluon import current
from helpers.widgets import DocumentPage

class Base(object):
    def __init__(
        self,
        hooks=[],
        meta=None,
        context=None
        ):
        from gluon.storage import Storage
        self.meta = meta or Storage()
        self.context = context or Storage()
        # you can user alers for response flash
        self.context.alerts = []

        self.response = current.response
        self.request = current.request
        self.session = current.session
        if not self.session['document']:
            self.session.document = Storage()
        self.T = current.T

        # hooks call
        self.start()
        self.build()
        self.pre_render()
        self.load_menus()

        # aditional hooks
        if not isinstance(hooks, list):
            hooks = [hooks]

        for hook in hooks:
            self.__getattribute__(hook)()

    def start(self):
        pass

    def before_create(self):
        pass
    def after_create(self):
        pass
    
    def before_read(self):
        pass
    def after_read(self):
        pass
    def before_update(self):
        pass
    def after_update(self):
        pass
    def before_delete(self):
        pass
    def after_delete(self):
        pass

    def before_validation(self):
        pass
    def validate(self):
        pass
    def after_validation(self):
        pass
    def on_validation_sucessful(self):
        pass
    def on_validation_failure(self):
        pass

    def build(self):
        pass

    def load_menus(self):
        self.response.menu = [
           (self.T('Home'), False, URL('default', 'index'), []),
           (self.T('New post'), False, URL('post', 'new'), []),
        ]

    def pre_render(self):
        pass


from core import Core
from helpers import exceptions

class Document(Base):
    def start(self):
        self.core = Core()
        self.db = self.core.db()
        self.auth = self.context.auth = self.core.auth
        self.session = self.core.session
        self.get()
        
    def get(self):
        self.context.document = self.db.get_document(*self.request.args[:2])
                     
    def create(self):
        self.before_create()
        self.context.form = DocumentPage(self.context.document)
        self.after_create()
        
    def edit(self):
        self.context.form = DocumentPage(self.context.document)

    def delete(self):
        self.db.send_to_trash(self.request.args[0], self.request.args[1])
        
    def show(self):
        self.context.form = DocumentPage(self.context.document, readonly=True)

    def render(self, view=None):
        viewfile = "%s.%s" % (view, self.request.extension)
        return self.response.render(viewfile, self.context)
