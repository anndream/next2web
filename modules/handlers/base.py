# -*- coding: utf-8 -*-


###############################################################################
# web2py modelless scaffold app
# Bruno Cezar Rocha <rochacbruno@gmail.com>
#
# Base handler for controller handlers
###############################################################################

from gluon import URL
from gluon.tools import prettydate
from gluon import current

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

        self.context.prettydate = prettydate
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

    def build(self):
        pass

    def load_menus(self):
        self.response.menu = [
           (self.T('Home'), False, URL('default', 'index'), []),
           (self.T('New post'), False, URL('post', 'new'), []),
        ]

    def pre_render(self):
        pass

    def render(self, view=None):
        viewfile = "%s.%s" % (view, self.request.extension)
        return self.response.render(viewfile, self.context)