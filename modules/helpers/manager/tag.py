#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 23/11/2012

@author: INFRA-PC1
'''

from base import BaseManager
from gluon.html import FORM, INPUT, URL, SCRIPT, TAG, DIV, SPAN
from gluon import current
from gluon.http import HTTP
from gluon.compileapp import LOAD

def pretty(tag):
    return str(tag).lower().capitalize()

class TagManager(BaseManager):
    _form = None
    def __init__(self, *args, **kwargs):
        super(TagManager, self).__init__(*args, **kwargs)
        
        self.T = current.T
        
        if not self._part_name:
            self._part_name = self.__class__.__name__
        
        self._id = 'tags_for_%s'%self.document.META.doc_name
        self._name = 'tags_%s'%self.document.META.doc_name
        self.request = current.request
        self.response = current.response
        
        self.base_url_all_tags = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_tag_form': self.document.META.doc_name, '__action': 'all_tags'})
        self.base_url_tag = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_tag_form': self.document.META.doc_name, '__action': 'form'})

        if hasattr(self.request, 'application'):
            self.callback()
            
    @property
    def component(self):
        attrs = self.base_url_tag.copy()
        attrs['ajax'] = True
        attrs['ajax_trap'] = True
        return LOAD(**attrs)
    
    def callback(self):
        if '__document_tag_form' in self.request.vars and self.request.vars['__document_tag_form'] == self.document.META.doc_name:
            if '__action' in self.request.vars and self.request.vars['__action'] == 'form':
                raise HTTP(200, self.validate_and_save())
            elif '__action' in self.request.vars and self.request.vars['__action'] == 'all_tags':
                raise HTTP(200, self.list_all_tags() or '[]')
            
    @property
    def widget(self):
        return DIV(
            *self.build_components()
        )
    
    def build_components(self):
        components = []
        components.append(SPAN(self.T('Tags'), _class='nav-header'))
        components.append(self.form)
        components.append(self.script())
        return components
    
    def list_all_tags(self):
        return [row.tag_name for row in self.db(self.db.Tags.id>0).select(self.db.Tags.tag_name)]
    
    def list_tags_in_db(self):
        return [row.tag_name for row in self.db((self.db.DocumentTag.document==self.document.META.id)&
                                                (self.db.DocumentTag.data_id==self.document.id)&
                                                (self.db.DocumentTag.tag==self.db.Tags.id)).select(self.db.Tags.tag_name)]
    
    def list_tags_in_session(self):
        return self.data
    
    def list_tags(self):
        tags = self.list_tags_in_session()
        tags.extend(self.list_tags_in_db())
        return tags
    
    def tag_referenced_by_others(self, tag_id):
        return self.db(self.db.DocumentTag.tag==tag_id).count()>0
    
    def has_tag(self, tag_name):
        return self.db((self.db.Tags.tag_name==pretty(tag_name))&
                       (self.db.DocumentTag.document==self.document.META.id)&
                       (self.db.DocumentTag.data==self.db.document.id)).count()>0
    
    def has_tag_in_all(self, tag_name):
        return self.db(self.db.Tags.tag_name==pretty(tag_name)).count()>0
    
    def add_tag(self, tag_name):
        if not self.has_tag(tag_name):
            if not self.has_tag_in_all(tag_name):
                tag_id = self.db.Tags.insert(tag_name=pretty(tag_name))
            else:
                tag_id = self.db(self.db.Tags.tag_name==pretty(tag_name)).select(self.db.Tags.ALL).first().id
            if self.document.id:
                _id = self.db.DocumentTag.insert(document=self.document.META.id, data_id=self.document.id, tag=tag_id)
                return _id
    
    def remove_tag(self, tag_name):
        if self.has_tag(tag_name):
            tag_id = self.db(self.db.Tags.tag_name==pretty(tag_name)).select(self.db.Tags.ALL).first().id
            if self.has_tag(tag_name):
                self.db((self.db.DocumentTag.document==self.document.META.id)&
                        (self.db.DocumentTag.data_id==self.document.id)&
                        (self.db.DocumentTag.tag==tag_id)).delete()
                if not self.tag_referenced_by_others(tag_id):
                    self.db(self.db.Tags.id==tag_id).delete()
                return True
            
    def update_tags(self, tags):
        old_tags = self.list_tags()
        if not isinstance(tags, list):
            if isinstance(tags, basestring):
                if ' ' in tags:
                    tags=tags.split(' ')
                else:
                    tags = tags.split(',')
            else:
                ValueError
        for tag_name in tags:
            if not tag_name in old_tags:
                self.add_tag(tag_name)
            else:
                old_tags.pop(old_tags.index(tag_name))
        
        for tag_name in old_tags:
            self.remove_tag(tag_name)
        
        self.build_components()    
        return self.xml()

    @property            
    def form(self):            
        if not self._form:
            self._form = FORM(
            INPUT(_type='hidden', _name=self._name, _class='tags', _style='width: 180px;', value=', '.join(self.list_tags())),
            _id=self._id,
            _class='tags'
        )
        return self._form
    
    def validate_and_save(self):
        def processor(vars):
            if self._name in vars:
                return (True, vars[self._name].split(' ' if ' ' in vars[self._name] else ','))
            
        if self.form.accepts(self.request.vars):
            self.save_data(processor)
        self.build_components()
        return self.widget.xml()        
    
    def script(self):
        from helpers import ajax_set_files
        files = []
        files.append(URL(c='static', f='templates', args=['bootstrap', 'third-party', 'jQuery-Select2', 'select2.css']))
        files.append(URL(c='static', f='templates', args=['bootstrap', 'third-party', 'jQuery-Select2', 'select2.min.js']))
        
        ajax_set_files(files)
        
        script = """
                ;(function($){
                    var el = $('input[name=%(name)s]');
                    function load_tags(){
                        var all_tags = [];
                        $.getJSON('%(url_all_tags)s', function (data) { all_tags = data });
                        el.select2({
                            'tags': all_tags,
                            'tokenSeparators': [',', ' ']
                        });
                        el.on('change', function(){
                            $('#%(id)s').submit();
                        });
                    }
                    if (el.select2 == undefined) {
                        setTimeout(load_tags, 500);
                        return true;
                    }
                    load_tags();
                })(jQuery);
            """%{
                'url_all_tags' : URL(**self.base_url_all_tags),
                'id' : self._id,
                'name' : self._name
             }
        if self.request.ajax:
            self.response.js = (self.response.js or '') + script.strip()
            return TAG['']()
        return SCRIPT(script.strip())
    
    def store(self):
        self.update_tags(self.data)