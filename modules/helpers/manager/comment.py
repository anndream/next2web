#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 26/11/2012

@author: INFRA-PC1
'''

from base import BaseManager
from gluon.html import FORM, INPUT, URL, SCRIPT, TAG, DIV, SPAN
from gluon import current
from gluon.tools import prettydate


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
        
        self.base_url_all_comments = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_comment_form': self.document.META.doc_name, 'method': 'all_comments'})
        self.base_url_last_comments = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_comment_form': self.document.META.doc_name, 'method': 'last_comments'})
        self.base_url_post_comments = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_comment_form': self.document.META.doc_name, 'method': 'post'})
        
    def callback(self):
        pass
    
    def list_comments(self):
        comments = [{'comment': row[self.db.DocumentComment].comment, 'by': row.auth_user.first_name, 'on': prettydate(row[self.db.DocumentComment].created_on, self.T), '__saved': (True, row[self.db.DocumentComment].id)} for row in self.db((self.db.DocumentComment.document==self.document.META.id)&
                                          (self.db.DocumentComment.data_id==self.document.id)&
                                          (self.db.DocumentComment.created_by==self.db.auth_user)).select(self.DocumentComment.ALL, self.db.auth_user.ALL)]
        return comments
    
    def list_last_comments(self, limitby=(0, 5)):
        comments = [{'comment': row[self.db.DocumentComment].comment, 'by': row.auth_user.first_name, 'on': prettydate(row[self.db.DocumentComment].created_on, self.T), '__saved': (True, row[self.db.DocumentComment].id)} for row in self.db((self.db.DocumentComment.document==self.document.META.id)&
                                          (self.db.DocumentComment.data_id==self.document.id)&
                                          (self.db.DocumentComment.created_by==self.db.auth_user)).select(
                                                            self.DocumentComment.ALL, 
                                                            self.db.auth_user.ALL, 
                                                            limitby=limitby,
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
        
    def remove_comment(self, comment_id):
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
                INPUT(_type='text', _name=self._name, _class='comment', _placeholder=self.T('Comment')),
                _method='post',
                _action = URL(**self.base_url_post_comments),
                _id=self._id,
                _class='comments form-inline'
            )
            
    def validate_and_save(self):
        if self.form.validate():
            self.save()
        self.build_components()
        return self.xml()
            
    def script(self):
        script = """jQuery(document).ready(function(){
            $('input[name=%(name)s]').keypress(function(e){
                if (e && e.keyCode == 13){
                    $('#%(id)s').submit();
                }
            });
        });"""
        
        if self.response.ajax:
            if not self.response.js:
                self.resposne.js = ''
            self.response.js+=self.script.strip()
            return TAG['']()
        else:
            return SCRIPT(script.strip())
        
    def build_components(self):
        if not self.components:
            self.components.append(SPAN(self.T('Tags'), _class='nav-header'))
            self.components.append(self.form)
            self.components.append(self.script())
            last_comments = self.list_last_comments()
            if last_comments:
                comments = []
                for comment in last_comments:
                    comments.append(
                        SPAN(
                             SPAN(
                                  comment['comment'], 
                                  _class='comment-text'
                             ), 
                             TAG['small'](('%s : %s'%(self.T('by'), comment['by'])), _class='comment-by'),
                             TAG['small'](('%s : %s'%(self.T('on'), comment['on'])), _class='comment-on')
                        )
                )
                self.components.append(DIV(*comments, _class='comment-container'))

    @property            
    def widget(self):
        self.build_components()
        return DIV(
            *self.components
        )
        
    def store(self):
        pass