#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 26/11/2012

@author: INFRA-PC1
'''

from base import BaseManager
from gluon.html import FORM, INPUT, URL, SCRIPT, TAG, DIV, SPAN, A, XML
from gluon import current
from gluon.tools import prettydate
from gluon.http import HTTP
from gluon.validators import IS_NOT_EMPTY

class CommentManager(BaseManager):
    _form = None
    def __init__(self, *args, **kwargs):
        super(CommentManager, self).__init__(*args, **kwargs)
        
        if not self._part_name:
            self._part_name = self.__class__.__name__
        
        self._id = '%s_for_%s'%(self._part_name, self.document.META.doc_name)
        self._name = '%s_%s'%(self._part_name, self.document.META.doc_name)
        
        self.T = current.T
        self.request = current.request
        self.response = current.response
        
        self.base_url_form_comment = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_comment_form': self.document.META.doc_name, '__action': 'form'})
        self.base_url_remove_comment = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_comment_form': self.document.META.doc_name, '__action': 'remove'})
        self.base_url_all_comments = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_comment_form': self.document.META.doc_name, '__action': 'all_comments'})
        self.base_url_last_comments = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_comment_form': self.document.META.doc_name, '__action': 'last_comments'})
        
    def callback(self): 
        if '__document_comment_form' in self.request.vars and self.request.vars['__document_comment_form'] == self.document.META.doc_name:
            if '__action' in self.request.vars and self.request.vars['__action'] == 'form':
                raise HTTP(200, self.validate_and_save())
            elif '__action' in self.request.vars and self.request.vars['__action'] == 'remove':
                self.remove_comment(self.request.vars['__saved'], self.request.vars['__idx'])
                raise HTTP(200, self.widget)
        
    def list_comments(self):
        comments = [{'comment': row.comment, 'by': row.created_by, 'on': row.created_on, '__saved': (True, row[self.db.DocumentComment].id)} for row in self.db((self.db.DocumentComment.document==self.document.META.id)&
                                          (self.db.DocumentComment.data_id==self.document.id)).select(self.DocumentComment.ALL)]
        return comments
    
    
    def list_last_comments(self, limit=5):
        comments = self.list_last_comments_in_session(limit)
        diff = limit - len(comments)
        if not diff == limit:
            comments.extend(self.list_last_comments_in_db(diff))
        return comments
    
    def list_last_comments_in_session(self, limit=5):
        i = 0
        comments = []
        for comment in self.data:
            comments.append(comment)
            i += 1
            if i == limit:
                break
        return comments
            
    def list_last_comments_in_db(self, limit=5):
        comments = [{'comment': row.comment, 'by': row.created_by, 'on': row.created_on, '__saved': (True, row[self.db.DocumentComment].id)} for row in self.db((self.db.DocumentComment.document==self.document.META.id)&
                                          (self.db.DocumentComment.data_id==self.document.id)).select(
                                                            self.db.DocumentComment.ALL,  
                                                            limitby=(0, limit),
                                                            orderby=(~self.db.DocumentComment.id))]
        return comments
    
    def get_comment(self, comment_id):
        comment_row = self.db((self.db.DocumentComment.document==self.document.META.id)&
                              (self.db.DocumentComment.data_id==self.document.id)&
                              (self.db.DocumentComment.id==comment_id)).select(self.db.DocumentComment.ALL).first()
        if comment_row:
            return comment_row
        else:
            return False

    def remove_comment(self, saved, comment_id):
        from helpers import safe_bool
        if safe_bool(saved):
            return self.remove_comment_in_db(int(comment_id))
        else:
            return self.remove_comment_in_session(int(comment_id))

    def remove_comment_in_session(self, comment_id):
        self.data.pop(comment_id)
        self._session_reindex()
        return True
        
    def remove_comment_in_db(self, comment_id):
        comment_row = self.get_comment(comment_id)
        if comment_row:
            comment_row.delete_record()
            return True
        else:
            return False
    
    def add_comment(self, comment):
        comment_id = self.db.DocumentComment.insert(
            document=self.document.META.id,
            data_id=self.document.id,
            comment=comment)
        return comment_id
    
    def update_comment(self, comment_id, comment):
        comment_row = self.get_comment(comment_id)
        if comment_row:
            comment_row.update_record(comment=comment)
            return True
        else:
            return False

    def add_or_update_comment(self, comment_id, comment):
        comment_row = self.get_comment(comment_id)
        if comment_row:
            return self.update_comment(comment_id, comment)
        else:
            return self.add_comment(comment)
        
    @property
    def form(self):
        if not self._form:
            self._form = FORM(
                INPUT(_type='text', _name=self._name, _class='comment', _placeholder=self.T('Comment'), _style='width: 180px;', requires=IS_NOT_EMPTY()),
                _id=self._id,
                _class='comments form-inline'
            )
        return self._form
            
    def _session_reindex(self):
        for i, comment in enumerate(self.data):
            comment['__saved'] = (False, i)
    
    def validate_and_save(self):
        def processor(vars):            
            if self._name in vars:
                data = self.data
                data.insert(0, {'comment': vars[self._name], 'on': self.request.now, 'by': (self.document.AUTH.user.firt_name if hasattr(self.document, 'AUTH') else 1), '__saved': (False, len(data))})
                self._session_reindex(data)
                return (True, data)
            else:
                return (False, None)
            
        if self.form.accepts(self.request.vars):
            self.save_data(processor)
        return self.widget
            
    def script(self):
        script = ''
        
        if self.response.ajax:
            self.response.js = (self.response.js or '') + self.script.strip()
            print self.response.js
            return TAG['']()
        else:
            return SCRIPT(script.strip())
        
    def build_components(self):
        
        def remove_url(comment):
            base = self.base_url_remove_comment.copy()
            base['vars'].update({'__saved': comment['__saved'][0], '__idx': comment['__saved'][1]})
            return URL(**base)
        
        components = []
        components.append(SPAN(self.T('Comments'), _class='nav-header'))
        components.append(self.form)
        components.append(self.script())
        last_comments = self.list_last_comments()
        if last_comments:
            comments = []
            for comment in last_comments:
                comments.append(
                    DIV(
                         DIV(
                            comment['comment'],
                            A(XML('&times'), _class='close', _href=remove_url(comment), cid=self.request.cid),
                            _class='comment-text'
                         ), 
                        DIV(
                            TAG['small']('%s : %s'%(self.T('by'), comment['by']), _class='comment-by'),
                            TAG['small']('%s : %s'%(self.T('on'), prettydate(comment['on'], self.T)), _class='comment-on'),
                            _class='comment-help'
                        ),
                        _class='comment-row'
                    )
            )
            components.append(DIV(*comments, _class='comment-container'))
        return components
    
    @property            
    def widget(self):
        return DIV(
            *self.build_components()
        )
        
    def store(self):
        pass