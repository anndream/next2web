#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 28/11/2012

@author: INFRA-PC1
'''

from base import BaseManager
from gluon import current
from gluon.html import FORM, INPUT, DIV, A, I, URL, TAG, SCRIPT, SPAN, XML, BUTTON
from gluon.validators import IS_NOT_EMPTY
from gluon.http import HTTP
from helpers import message
from gluon.compileapp import LOAD

class FileManager(BaseManager):
    _form = None
    def  __init__(self, *args, **kwargs):
        super(FileManager, self).__init__(*args, **kwargs)
        
        self.T = current.T
        self.request = current.request
        self.response = current.response
        
        if not self._part_name:
            self._part_name = self.__class__.__name__
        
        self._id = '%s_for_%s'%(self._part_name, self.document.META.doc_name)
        self._name = '%s_%s'%(self._part_name, self.document.META.doc_name)
        self._id_txt = 'text_for_%s'%(self._name)
        self._id_btn = 'btn_for_%s'%(self._name)
    
        self.base_url_file = dict(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args, vars={'__document_file_form': self.document.META.doc_name, '__action': 'form'})
        self.base_url_remove_file = dict(r=self.request, c=self.request.cotroller, f=self.request.function, args=self.request.args, vars={'__document_file_form': self.document.META.doc_name, '__action': 'remove'})
        self.basr_url_download_fiel = dict(r=self.request, c=self.request.cotroller, f=self.request.function, args=self.request.args, vars={'__document_file_form': self.document.META.doc_name, '__action': 'download'})

        if hasattr(self.request, 'application'):
            self.callback()
    
    @property
    def component(self):
        attrs = self.base_url_file.copy()
        attrs['ajax'] = True
        attrs['ajax_trap'] = True
        return LOAD(**attrs)
    
    def callback(self):
        if '__document_file_form' in self.request.vars and self.request.vars['__document_file_form'] == self.document.META.doc_name:
            if '__action' in self.request.vars and self.request.vars['__action'] == 'form':
                self.validate_and_save()
            if '__action' in self.request.vars and self.request.vars['__action'] == 'remove':
                self.remove_document_file(self.request.vars['__saved'], int(self.request.vars['__idx']))
            if '__action' in self.request.vars and self.request.vars['__action'] == 'download':
                raise HTTP(200, self.download(self.request.vars['__saved'], int(self.request.vars['__idx'])))
            raise HTTP(200, self.widget)
        
    def list_files_in_session(self):
        pass
        
    def list_files(self):
        return [{'title': row[self.db.File].title, '__saved': (True, row[self.db.DocumentFile.id])} for row in
                    self.db((self.db.DocumentFile.document==self.document.META.id)&
                            (self.db.DocumentFile.data_id==self.document.id)&
                            (self.db.DocumentFile.file==self.db.File.id)).select(
                                self.db.DocumentFile.ALL,
                                self.db.File.ALL
                            )
                ]

    def get_file_or_add(self, title, filename, path):
        files = self.db(self.db.File.path==path).select(self.db.File.ALL)
        if not files.first():
            return self.db.File.insert(title=title, filename=filename, path=path)
        else:
            file_row = files.first()
            updates = {}
            if file_row.title != title:
                updates['title'] = title
            if file_row.filename != filename:
                updates['filename'] = filename
            if len(updates.keys())>0:
                file_row.update_record(**updates)
            file_row.id        
    
    def get_file(self, file_id):
        file_row = self.db.File(file_id)
        if file_row:
            return file_row
        else:
            return False
        
    def delete_file(self, file_id):
        file_row = self.get_file(file_id)
        if file_row:
            file_row.delete_record()
            return True
        return False
        
    def has_document_file(self, file_id):
        return self.db((self.db.DocumentFile.document==self.document.META.id)&
                       (self.db.DocumentFile.data_id==self.document)&
                       (self.db.DocumentFile.file==file_id)).count()>0

    def get_document_file(self, documentfile_id):
        documentfile_row = self.db((self.db.DocumentFile.document==self.document.META.id)&
                                   (self.db.DocumentFile.data_id==self.document.id)&
                                   (self.db.DocumentFile.id==documentfile_id)&
                                   (self.db.DocumentFile.file==self.db.File.id)).select(self.db.DocumentFile.ALL, self.db.File.ALL).first()
        return documentfile_row or False
        
    def add_document_file(self, title, filename, path ):
        file_id = self.get_file_or_add(title, filename, path)
        
        if not self.has_document_file(file_id):
            return self.db.DocumentFile.insert(document=self.document.META.id, data_id=self.document.id, file=file_id)

    def file_referenced_by_others(self, file_id):
        return self.db(self.db.DocumentFile.file==file_id).count()>0
            
    def remove_document_file(self, documentfile_id, delete_file=False):
        documentfile_row = self.get_document_file(documentfile_id)
        if documentfile_row:
            if delete_file and not self.file_referenced_by_others(documentfile_row[self.db.File].id):
                documentfile_row[self.db.File].delete_record()
            else:
                message(self.T('DocumentFile does not exists.'))
            documentfile_row.delete_record()
            return True
        return False
    
    @property
    def form(self):
        if not self._form:
            self._form = FORM(
                INPUT(_type="file", _name=self._name, _style='display:none', requires=IS_NOT_EMPTY()),
                DIV(
                    INPUT(_id=self._id_txt, _type='text', _class='upload-text'),
                    A(I(_class='icon-folder-open'), _class='btn btn-mini', _id=self._id_btn),
                    A(I(_class='icon-upload'), _type='submit', _class='btn btn-mini', _id='submit_for_%s'%self._name),
                    _class='input-append'
                ),
                _id = self._id,
                
            ).process()
        return self._form
    
    def build_components(self):
        def remove_url(filerow):
            base = self.base_url_remove_file.copy()
            base['vars'].update({'__saved': filerow['__saved'][0], '__idx': filerow['__saved'][1]})
            return URL(**base)
        
        def download_url(filerow):
            base = self.base_url_downlaod_file.copy()
            base['vars'].update({'__saved': filerow['__saved'][0], '__idx': filerow['__saved'][1]})
            return URL(**base)
        
        components = []
        components.append(SPAN(self.T('Attachments'), _class='nav-header')),
        components.append(self.form)
        components.append(self.script())
        uploaded_files = self.list_files()
        if uploaded_files:
            files = []
            for filerow in uploaded_files:
                files.append(
                    DIV(
                        SPAN(I(_class='icon-file'), filerow['title']),
                        A(I(_class='icon-download'), _href=download_url(filerow), cid=self.request.cid),
                        A(XML('&times;'), _class='close', _href=remove_url(filerow), cid=self.request.cid),
                        _class='file-row'
                    )
                )
            components.append(files)
        return components

    @property
    def widget(self):
        return DIV(_class='files-component', *self.build_components(), _style="width: 140px;")
    
    def script(self):
        script = """
            ;(function($){
                $('#%(id_btn)s').click(function(){
                    $('input[name=%(name)s]').trigger('click');
                });
                $('input[name=%(name)s]').change(function(e){
                    var val = $(this).val();
                    console.log('val: '+val);
                    var file = val.split(/[\\\\/]/);
                    console.log('file:'+file.toString());
                    $('#%(id_txt)s').val(file[file.length-1]);
                });
                $('#%(submit)s').click(function(){
                    $('#%(id)s').submit();
                });
            })(jQuery);
        """%{
            'name': self._name,
            'id': self._id,
            'id_txt': self._id_txt,
            'id_btn': self._id_btn,
            'submit': 'submit_for_%s'%self._name
        }
        if self.request.ajax:
            self.response.js = (self.response.js or '') + script.strip();
            return TAG['']()
        return SCRIPT(script.strip())