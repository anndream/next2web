#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 25/10/2012

@author: INFRA-PC1
'''

from gluon.sqlhtml import StringWidget, TextWidget, \
OptionsWidget, ListWidget, RadioWidget, CheckboxesWidget, PasswordWidget, \
UploadWidget, AutocompleteWidget

from gluon.storage import Storage
from gluon import current, validators

from helpers.document import types, vtypes

from gluon.html import *

T = current.T

pretty = lambda s: s.replace('default', str(T('Home'))).replace('_', ' ').capitalize()

class FormWidget(object):
    _class= 'generic-widget'
    _row_id_sufix = '_row'
    
    @classmethod
    def requires(cls, df):
        req = []
        if df.property('policy', 'is_required') == 'ALWAYS':
            req.append(validators.IS_NOT_EMPTY())
    
    @classmethod
    def label(cls, df):
        return LABEL(df.df_label, _for = df.df_name) if df.df_label else TAG['']()
    
    @classmethod
    def control(cls, df, value, **attrs):
        raise NotImplementedError
    
    @classmethod
    def writable(cls, df):
        return df.property('policy', 'is_writable')
    
    @classmethod
    def readable(cls, df):
        return df.property('policy', 'is_readable')
    
    @classmethod
    def readonly(cls, df, value, **attrs):
        if 'value' in attrs:
            value = attrs.pop('value')
        return SPAN(value, **attrs)
    
    @classmethod
    def _attributes(cls, doc_field, widget_attributes, **attributes):
        attr = dict(
            _id = '%s_%s' % (doc_field.PARENT.doc_name, doc_field.df_name),
            _class = cls._class or types[doc_field.df_type]._class,
            _name = doc_field.df_name,
            requires = cls.requires(doc_field),
        )
        attr.update(widget_attributes)
        attr.update(attributes)
        return attr
    
    @classmethod
    def widget(cls, df, value, **attrs):
        #data = df_type.dump()['data'] or (df_type.default() or None)
        #if data:
        #    attrs['_data-type'] = data
        
        _id = '%s__%s'%(df.df_name, cls._row_id_sufix) 
        return DIV(cls.label(df), (cls.control if cls.writable(df) else cls.readonly)(df, value, **attrs), widget_help(df.df_description), _id=_id,  _class='control-group'
        )
        
        
class String(FormWidget):
    _class = types.string._class
    _type = 'text'
    
    @classmethod
    def control(cls, df, value, **attrs):
        default = dict (
            _type = cls._type,
            value = (not value is None and str(value)) or ''
        )
        attr = cls._attributes(df, default, **attrs)
        
        return INPUT(**attr)
    
class Integer(String):
    _class = types.integer._class
    
class Double(StringWidget):
    _class = types.double._class
    
class Decimal(String):
    _class = types.decimal._class
    
class Date(String):
    _class = types.date._class
    prepend = SPAN(I(_class='icon-calendar'), _class='add-on'),
    
    @staticmethod
    def control(cls, df, value, **attributes):
        widget = String.control( df, value, **attributes)
        _class = 'input-prepent %s-control'%df.df_type
        return DIV(cls.prepend, widget, _class=_class)
    
class Time(Date):
    _class = types.time._class
    prepend = SPAN(I(_class='icon-time'), _class='add-on')
    
class Datetime(Date):
    _class = types.datetime._class
    prepend = SPAN(I(_class='icon-calendar'), _class='add-on')
    
class Currency(Date):
    _class = types.currency._class
    prepend = SPAN(T('$'), _class='add-on')
    
class Url(Date):
    _class = types.email._class
    prepend = SPAN(I(_class='icon-globe'), 'add-on')
    
class Email(Date):
    _class = types.email._class
    prepend = SPAN(I(_class='icon-envelope'), _class='add-on')
    
class Phone(Date):
    _class = types.phone._class
    #TODO: O Css necessita de um icone de telefone, o novo glyphicons possui
    prepend = SPAN(I(_class='icon-leaf'), _class='add-on')
    
class Text(FormWidget):
    _class = types.text._class
    
    @classmethod
    def control(cls, df, value, **attrs):
        #data = df_type.dump()['data']
        #if data:
        #    attrs['_data-type'] = `data`
        attrs = cls._attributes(df, {'valeu': value}, **attrs)
        return TEXTAREA(**attrs) 
    
class Smalltext(Text):
    _class = types.smalltext._class
    
class Texteditor(Text):
    _class = types.texteditor._class
    
class Rule(Text):
    _class = types.rule._class
    
class Boolean(String):
    _class = types.boolean._class
    
class Select(OptionsWidget):
    _class = types.select._class
    
    @staticmethod
    def has_options(df):
        return df.has_options()
        
    @classmethod
    def widget(cls, df, value, **attrs):
                
        return OptionsWidget.widget(df.field, value, **attrs)

class MultipleSelect(Select):
    
    @classmethod
    def widget(cls, df, value, size=5, **attrs):
        
        attrs.update(_size=size, _multiple=True)
        
        return Select.widget(df, value, **attrs)

class Radio(Select):
    @classmethod
    def widget(cls, df, value, **attrs):
        
        return RadioWidget.widget(df.field, value, **attrs)
    
class Checkbox(Select):
    @classmethod
    def widget(cls, df, value, **attrs):
        return CheckboxesWidget.widget(df.field, value, **attrs)
    
class List(ListWidget):
    _class = types.list._class
    
    @classmethod
    def widget(cls, df, value, **attrs):
        return ListWidget.widget(df.field, value, **attrs)
    
class Password(PasswordWidget):
    _class = types.password._class
    
    @classmethod
    def widget(cls, df, value, **attrs):
        return PasswordWidget.widget(df.field, value, **attrs)
    
class Filelink(UploadWidget):
    _class = types.filelink._class
    
    @classmethod
    def widget(cls, df, value, download_url=None, **attrs):
        return UploadWidget.widget(df.field, value, download_url, **attrs)
    
    @classmethod
    def represent(cls, df, value, download_url=None):
        return UploadWidget.represent(df.field, value, download_url)

class Link(object):
    _class = types.link._class
    _row_id_sufix = '_row'
    
    AGGREGATION = 'agg'
    CONDITION = 'condition'
    DOC_FIELD = 'doc_field'
    KEYWORD = 'keyword'
    LIST_AGGREGATIONS = [('and', T('And')),
                         (('or'), T('Or'))
                        ]
    LIST_CONDITIONS = [('eq', T('Equals'), lambda field, value: field == value),
                       ('gt', T('Greater than'), lambda field, value: field > value),
                       ('lt', T('Less than'), lambda field, value: field < value),
                       ('ne', T('Not Equals'), lambda field, value: field != value),
                       ('ge', T('Greater or equals'), lambda field, value: field >= value),
                       ('gt', T('Less or equals'), lambda field, value: field <= value),
                       ('contains', T('Contains'), lambda field, value: field.like('%'+value+'%')),
                       ('start_with', T('Start with'), lambda field, value: field.like(value + '%')),
                       ('ends_with', T('Ends with'), lambda field, value: field.like('%'+value))
                      ]
        
    def __init__(self, doc_field, value, **attrs):
        self.doc_field = doc_field
        
        self._id = '%s_%s'%(self.doc_field.df_name, self._row_id_sufix)
        self.modal_id = 'modal_for_%s' % self.doc_field.df_name
        self.form_id = 'form_for_%s' % self.doc_field.df_name
        self.text_id = 'text_for_%s' % self.doc_field.df_name
        
        self.db = doc_field.PARENT._db
        self.table = doc_field.PARENT.doc_tablename
        self.label = doc_field.property('type', 'label')
        self.help_string = doc_field.property('type', 'help_string')
        self.request = current.request
        
        if hasattr(self.request, 'application'):
            self.url_form = URL(args=self.request.args, vars={'__meta_form': self.doc_field.df_name})
            self.url_form_js = URL(r=self.request, c=self.request.controller, f=self.request.function + '.js', vars={'__meta_form': self.doc_field.df_name})
            self.url_keyword = URL(args=self.request.args, vars={'__meta_keywords': self.doc_field.df_name})
            self.callback()
        else:
            self.url_form = self.request
            self.url_form_js = self.request
            self.url_keyword = self.request

    def requires(self):
        req = []
        if self.doc_field.property('policy', 'is_required') == 'ALWAYS':
            req.append(validators.IS_NOT_EMPTY())
        if self.doc_field.property('type', 'document'):
            req.append(validators.IS_IN_DB(self.db, 'tabDocument.id', '%(' + self.doc_field.property('type', 'label') + ')s'))            
        return req
            
    @staticmethod
    def widget(df, value, **attrs):
        widget = Link(df, value, **attrs)
        return widget.build(df, value, **attrs)

    def build_query(self):
        query = None
        i = int(self.request.vars.pop('idx', 1))
        operators = dict([(x[0], x[2]) for x in self.LIST_CONDITIONS])
        for x in range(i):
            sfx = '_%d'%x
            field = self.doc_field.document.fields[self.request.vars[self.DOC_FIELD+sfx]]._field
            field.db = self.db
            field.tablename = self.table
            op = self.request.vars[self.CONDITION+sfx]
            val = self.request.vars[self.KEYWORD+sfx]
            atom = operators[op](field, val)
            if x == 0:
                query = atom
            else:
                agg_op = self.request.vars[self.AGGREGATION+sfx]
                if agg_op == 'or':
                    query = (query | atom) if query else atom
                else:
                    query = (query & atom) if query else atom
        return query or (self.document.table.id > 0)
    
    def callback(self):
        from gluon.http import HTTP
        if '__meta_form' in self.request.vars and self.request.vars['__meta_form']==self.doc_field.df_name:
            
            doc_fields = []
            
            [doc_fields.append((doc_field.df_name, doc_field.df_label or pretty(doc_field.df_name))) for doc_field in self.db(self.db.DocumentField.document==self.doc_field.document).select()]
            
            form = FORM(
                DIV(
                    SELECT(*[OPTION(y,_value=x) for x,y in self.LIST_AGGREGATIONS], _class=self.AGGREGATION, _name=self.AGGREGATION+'_0'),
                    SELECT(*[OPTION(y,_value=x) for x,y in doc_fields], _class=self.DOC_FIELD, _name=self.DOC_FIELD+'_0'),
                    SELECT(*[OPTION(x[1],_value=x[0]) for x in self.LIST_CONDITIONS], _class=self.CONDITION, _name=self.CONDITION+'_0'),
                    INPUT(_name=self.KEYWORD+'_0', _type='text', _class=self.KEYWORD),
                    _class='link-condition first control-group'
                ),
                DIV(BUTTON(I(_class='icon-search'), ' ' +str( T('Filter')), _type="submit", _class="btn"), _class="actions"),
                _id=self.form_id,
                _action=self.url_form
            )
            raise HTTP(200, form.xml())
        
        elif '__meta_keywords' in self.request.vars and self.request.vars['__meta_keywords']==self.doc_field.df_name:
            query = self.build_query()
            rows = self.db.executesql('SELECT * FROM %s WHERE %s'%(self.table, str(query)), as_dict=True)
            if rows:
                if self.help_string:
                    results = [DIV(A(row[self.label], _class='result', _href='javascript:void(0)', **{'_data-id': row['id'], '_data-label': row[self.label]}), P(row%self.help_string, _class='.small'), _class='result-line') for row in rows]
                else:
                    results = [DIV(A(row[self.label], _class='result', _href='javascript:void(0)', **{'_data-id': row['id'], '_data-label': row[self.label]}), _class='result-line') for row in rows]
                raise HTTP(200, TAG[''](*results).xml())
                
            else:
                raise HTTP(200, DIV(T('No results found', _class='no-results')).xml())

    def build(self, df, value, **attributes):
        
        label = lambda df: LABEL(df.df_label or '', _for=df.df_name)
        
        default = dict(
            _type="text",
            value = (not value is None and str(value)) or '',
        )
        _id = "%s_%s" % (df.PARENT.doc_name, df.df_name)
        
        attr = String._attributes(df, default, **attributes)
        
        attr['_id'] = self.text_id
        attr['_autocomplete'] = 'off'
        attr['_class'] = 'link-text',
        attr['_class'] = ''
        
        name = attr.pop('_name')
        value = attr['value']
        
        record = self.db(self.db[self.table].id==value).select(self.db[self.table].ALL).first()
        if record: 
            attr['value'] = record[self.label]
        
        return DIV(
                label(df),
                DIV(
                    INPUT(_type='hidden', value=value, _name=name, requires=self.requires()),
                    INPUT(**attr),
                    A(I(_class='icon-search'), _class='btn btn-mini', _title=T('Search')),
                    A(I(_class='icon-play'), _class='btn btn-mini', _title=T('Open Link'), _onclick=''),
                    A(I(_class='icon-plus'), _class='btn btn-mini', _title=T('Add')),
                    _class="input-append link-control"
                ),
                widget_help(df.df_description),
                DIV(
                    DIV(
                        BUTTON(XML('&times;'), _type='button', _class='close', **{'_data-dismiss': 'modal', '_aria-hidden': 'true'}),
                        H3(str(T('Select')) + ' ' + df.PARENT.doc_title or ''),
                        _class='modal-header'
                    ),
                    DIV(
                        DIV(_class='link-filter'),
                        DIV(_class='link-results'),
                        _class='modal-body'
                    ),
                    _id=self.modal_id,
                    _class="link-modal modal hide fade",
                    **{'_data-backdrop': 'false'}
                ),
                SCRIPT(
                    '''jQuery(document).ready(function(){
                        jQuery('#%(modal_id)s').appendTo('.dialogs');
                        jQuery('#%(modal_id)s').on('hide', function(){
                            $('#%(modal_id)s .modal-body .link-filter, #%(modal_id)s .modal-body .link-filter').html('');
                        });
                        jQuery('#%(modal_id)s').on('show', function(){
                            jQuery.get('%(url_form)s', function(data){
                                jQuery('#%(modal_id)s .modal-body .link-filter').html(data);
                                function add(e){
                                    if (!valid(e)) return;
                                    parent = jQuery(e)
                                    row = parent.clone(true);
                                    row.removeClass('first').insertBefore(parent.parent().find('.actions'));
                                    reorder(parent.parent());
                                    row.find(':text').val('').focus();
                                }
                                function reorder(e){
                                    $(e).find('.link-condition').each(function(i,v){
                                       $(v).find('select, input').each(function(x,y){
                                           $(y).attr(name, $(y).attr('class') + '_' + i);
                                       }); 
                                    });
                                }
                                function del(e){
                                    parent = e.parent();
                                    $(e).remove();
                                    reorder(parent);
                                }
                                function valid(e){
                                    parent = $(e);
                                    if (!parent.find(':text').val()) {
                                        if (!parent.is('.error')){
                                            parent.addClass('error');
                                        }
                                        return false;
                                    };
                                    if (parent.is('.error')) parent.removeClass('error');
                                    return true;
                                }
                                jQuery.fn.grow_div = function(){
                                    return this.each(function(i,v){
                                        jQuery(v).find(':text').after('<a class="btn btn-mini add" href="javascript:void(0)"><i class="icon-plus"></i></a>').next().click(function(){add(v);}).after('<a class="btn btn-mini remove" href="javascript:void(0)"><i class="icon-remove"></i></a>').next().click(function(){del(v);});
                                    })
                                }
                                jQuery('.link-condition').first().addClass('first');
                                jQuery('#%(form_id)s .link-condition').grow_div();
                                jQuery('#%(form_id)s').submit(function(e){
                                    e.preventDefault();
                                    jQuery('#%(form_id)s').find('.link-condition').each(function(i,v){
                                        valid(v);
                                        if ($(v).is(':not(.first)')){
                                            $(v).find('.remove').click();
                                        }
                                    });
                                    reorder('%(form_id)s');
                                    jQuery.get('%(url_key)s&' + jQuery('#%(form_id)s').serialize() + '&idx=' +jQuery('#%(form_id)s').find('.link-condition').length , function(data){
                                        $('#%(modal_id)s .modal-body .link-results').html(data).show().focus();
                                        $('#%(modal_id)s .modal-body .link-results').find('.result-line').each(function(i,v){
                                            $(v).click(function(){
                                                $('input[name=%(name)s]').val($('a', v).data('id'));
                                                $('#%(text_id)s').val($('a', v).data('label'));
                                                $('#%(modal_id)s').modal('hide');
                                            });
                                        });
                                    });
                                });
                            });
                        });
                        jQuery('#%(id)s').find('.link-control a:first').click(function(){    
                            jQuery('#%(modal_id)s').modal('show');
                        });
                    });'''%dict(
                        name=self.doc_field.df_name,
                        form_id=self.form_id, 
                        modal_id=self.modal_id,
                        text_id=self.text_id,
                        id=self._id,
                        url_key=self.url_keyword,
                        url_form=self.url_form,
                        url_js=self.url_form_js,
                    ),
                    _type="text/javascript"
                ),
                _class="control-group",
                _id = self._id
            )
        

class Property(object):
    _class = types.property._class
    _row_id_sufix = '_row'
    _property_row_prefix = 'property'
    
    def __init__(self, doc_field, value, **attrs):
        #TODO0: Continuar a implementação do Widget Property
        from helpers.properties import PropertyManager
        self.doc_field = doc_field
        self.groups = value.keys()
        self._id = 'properties_for_'
        
        PropertyManager(self, value)
        
    def build(self):
        label = lambda f: LABEL(pretty(f.label or f.name), _for=f.name)
        
        widget = DIV(
            _class='acordion'
        )
        

class Suggest(AutocompleteWidget):
    _class = vtypes.suggest._class
    
    def __init__(self, request, df, id_df=None, db=None, orderby=None,
                 limitby=(0,10), distinct=False,
                 keyword = '_autocomplete_%(tablename)s_%(fieldname)s',
                 min_length=2, help_fields=None, help_string=None):
        self._class = ' '.join([df.df_type, self._type])
        AutocompleteWidget.__init__(
            request, df.field, id_df.field if id_df else None, db, orderby,
            limitby, distinct, keyword, min_length, help_fields, help_string
        )
        
    def __call__(self, df, value, **attrs):
        return AutocompleteWidget.__call__(self, df.field, value, **attrs)

class Virtual(FormWidget):
    _class = 'virtual-field-widget'
    
    @classmethod
    def _attributes(cls, df, widget_attrs, **attrs):
        attr = dict(
            _id= '%s_%s'%(df.PARENT.doc_name, df.df_name),
            _class = cls._class,
            _name = df.df_name,        
        )
        attr.update(widget_attrs)
        attr.update(attrs)
        return attr
    
    @classmethod
    def widget(cls, df, value, **attrs):
        
        raise NotImplementedError
    
class Table(Virtual):
    _class = vtypes.table._class
    
    @classmethod
    def widget(cls, df, value, **attrs):        
        attr = cls._attributes(df, {}, **attrs)
        
        return DIV(df.get_child(df_type.get_option('child')), **attr)
    
class SectionBreak(Virtual):
    _class = vtypes.sectionbreak._class + ' row-fluid'
    
    @classmethod
    def widget(cls, doc_field, value, **attrs):        
        attr = cls._attributes(doc_field, {}, **attrs)
        
        return DIV(H2(doc_field.df_label) if doc_field.df_label else '', P(doc_field.df_description) if doc_field.df_description else '', **attr)
    
class ColumnBreak(Virtual):
    _class = vtypes.columnbreak._class + " span6"
    
    @classmethod
    def widget(cls, df, value, **attrs):
        return DIV(*[],_class=cls._class)
    
class Button(Virtual):
    _class = vtypes.button._class
    
    @classmethod
    def widget(cls, df, **attrs):
        
        attr = cls._attributes(df, {}, **attrs)
        
        return DIV(df.df_label, **attr)
    
widgets = Storage(
    string = String,
    integer = Integer,
    double = Double,
    decimal = Decimal,
    currency = Currency,
    date = Date,
    time = Time,
    datetime = Datetime,
    text = Text,
    smalltext = Smalltext,
    texteditor = Texteditor,
    rule = Rule,
    boolean = Boolean,
    select = Select,
    multipleselect = MultipleSelect,
    radio = Radio,
    checkbox = Checkbox,
    list = List,
    password = Password,
    upload = Filelink,
    suggest = Suggest,
    link = Link,
    table = Table,
    sectionbreak = SectionBreak,
    columnbreak = ColumnBreak,
    button = Button,
)

def widget_help(strhelp):        
    if len(strhelp or '')<=30:
        return SPAN(strhelp or '', _class='help-block')
    else:
        attrs = {
            '_data-animation': 'true',
            '_data-placement': 'bottom',
            '_data-trigger': 'hover',
            '_data-content': strhelp or '',
            
        }
        return SPAN( A(I(_class='icon-exclamation-sign'), **attrs), _class='help-block')



class Document(DIV):
    def __init__(self,
        document,
        submit_button = T('Save'),
        readonly = False,
        actions = ['new', 'list', 'print', 'send', 'delete'],
        **attrs
    ):
        DIV.__init__(self, _class="page", **attrs)
        self.T = current.T
        self.response = current.response
        self.request = current.request
        self.session = current.session
    
        self.document = document
        self.submit_button = submit_button
        self.readonly = readonly
        self.actions = actions
        
        self.components=self.build_page()
        
    def formstyle_document_help(self, strhelp):        
        if len(strhelp or '')<=30:
            return SPAN(strhelp or '', _class='help-block')
        else:
            attrs = {
                '_data-animation': 'true',
                '_data-placement': 'bottom',
                '_data-trigger': 'hover',
                '_data-content': strhelp or '',
                
            }
            return SPAN( A(I(_class='icon-exclamation-sign'), **attrs), _class='help-block')
        
    def formstyle_document(self):        
        i = 0
        element = TAG['']()
        
        def _column_break(widget, i):
            _type = _type = self.document.META.DOC_FIELDS[i].df_type
            df_name = self.document.META.DOC_FIELDS[i].df_name
            while i < len(self.document.META.DOC_FIELDS) and _type not in ('sectionbreak', 'columnbreak'):
                subwidget = widgets[_type].widget(self.document.META.DOC_FIELDS[i], self.document[df_name] if self.document.data else '' )
                widget.components.append(subwidget)
                if (i+1) >= len(self.document.META.DOC_FIELDS) or self.document.META.DOC_FIELDS[i+1].df_type in  ('sectionbreak', 'columnbreak') : 
                    break
                else:
                    i += 1
                    _type = self.document.META.DOC_FIELDS[i].df_type
            return widget, i
        
        def _section_break(widget, i):
            _type = self.document.META.DOC_FIELDS[i].df_type
            df_name = self.document.META.DOC_FIELDS[i].df_name
            while i < len(self.document.META.DOC_FIELDS) and _type != 'sectionbreak':
                subwidget = widgets[_type].widget(self.document.META.DOC_FIELDS[i], self.document[df_name] if self.document.data else '' )
                if _type == 'columnbreak':
                    subwidget, i = _column_break(subwidget, i+1)
                widget.components.append(subwidget)
                if (i+1) >= len(self.document.META.DOC_FIELDS) or self.document.META.DOC_FIELDS[i+1].df_type == 'sectionbreak': 
                    break
                else:
                    i += 1
                    _type = self.document.META.DOC_FIELDS[i].df_type
            return widget, i
        
        while i < len(self.document.META.DOC_FIELDS):
            _type = self.document.META.DOC_FIELDS[i].df_type
            df_name = self.document.META.DOC_FIELDS[i].df_name
            wgt = widgets[_type].widget(self.document.META.DOC_FIELDS[i], self.document[df_name] if self.document[df_name] else '' )
            if _type == 'sectionbreak':
                subwgt, i = _section_break(wgt, i+1)
                i += 1
                element.components.append(subwgt)
                continue
            elif _type == 'columnbrek':
                subwgt, i = _column_break(wgt, i+1)
                i += 1
                element.components.append(subwgt)
                continue
            else:
                element.components.append(wgt)
            i += 1
            
        return element
    
    def build_page(self):
        return self.build_page_header(), self.build_page_content()
        
    def build_page_header(self):
        
        menus = [LI(A(I(_class="icon-home"), _title=T('Home'), _href=URL(r=self.request, c='default', f='index')))]
        
        if self.request.function == 'index':
            menus.append(LI(A(T(pretty(self.request.controller)), _href=URL(r=self.request, c=self.request.controller, f='index', args=self.request.args))))
        else:
            menus[-1] = LI(A(T(pretty(self.request.controller)), _href=URL(r=self.request, c=self.request.controller, f=self.request.function, args=self.request.args)))
        
        return DIV(
            DIV(
                A(XML('&times;'),_class="close well-small"),
                UL(*menus, _class="breadcrumb pull-right"),
                _class="pull-right"
            ),
            H1(self.document.doc_title),
            TAG['small'](self.document.doc_description),
            _class="page-header"
        )

    def build_page_content(self):
        return DIV(
                   FORM(self.formstyle_document()), 
                   DIV(_class='dialogs'),
                   _class='page-content'
                )
                
    def buid_page_menu(self):
        
        return DIV(
            UL(
               LI()
            )
        )
        
                
    def build_actions(self):
        pass
    