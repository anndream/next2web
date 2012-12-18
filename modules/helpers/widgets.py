#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 25/10/2012

@author: INFRA-PC1
'''

from gluon.storage import Storage
from gluon import current, validators
from helpers.document import types, vtypes
from gluon.html import *
from gluon.http import HTTP

from helpers.storage import storage
from helpers.manager import ChildManager

T = current.T

pretty = lambda s: s.replace('default', str(T('Home'))).replace('_', ' ').capitalize()
get_default = lambda opts, name: filter(lambda opt: opt.name==name, opts)[0].default

class FormWidget(object):
    _class= 'generic-widget'
    _row_id_sufix = '_row'
    
    @classmethod
    def isrequired(cls, df):
        return df.property('policy', 'is_required') == 'ALWAYS'
    
    @classmethod
    def requires(cls, df):
        req = []
        if cls.isrequired(df):
            req.append(validators.IS_NOT_EMPTY())
        return req
    
    @classmethod
    def label(cls, df):
        return LABEL('%s'%(df.df_label), SPAN(' *', _style='color:#d00;font-weight:bold;') if cls.isrequired(df) else '' , _for = df.df_name) if df.df_label else TAG['']()
    
    @classmethod
    def control(cls, df, value, **attrs):
        raise NotImplementedError
    
    @classmethod
    def writable(cls, df, stage):
        #print df.df_name, stage, df.property('policy', 'is_writable')
        return df.property('policy', 'is_writable') in (stage, 'ALWAYS') 
    
    @classmethod
    def readable(cls, df, stage):
        return df.property('policy', 'is_readable') in (stage, 'ALWAYS')
    
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
        
        stage = ('ON_CREATE' if not attributes['row']['id'] else 'ALWAYS')
        
        if not cls.writable(doc_field, stage):
            attr['_disabled']='disabled'
        return attr
    
    @classmethod
    def widget(cls, df, value, **attrs):
        #data = df_type.dump()['data'] or (df_type.default() or None)
        #if data:
        #    attrs['_data-type'] = data
        
        _id = '%s__%s'%(df.df_name, cls._row_id_sufix) 
        return DIV(cls.label(df), cls.control(df, value, **attrs), widget_help(df.df_description), _id=_id,  _class='control-group'
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
    
    @classmethod
    def requires(cls, df):
        req = String.requires(df)
        minimun = df.property('type', 'minimun')
        maximun = df.property('type', 'maximun')
        
        if minimun and maximun:
            req.append(validators.IS_INT_IN_RANGE(minimun = minimun, maximun = maximun))
        elif minimun:
            req.append(validators.IS_INT_IN_RANGE(minimun = minimun))
        elif maximun:
            req.append(validators.IS_INT_IN_RANGE(maximun = maximun))
            
        return req
        
class Double(String):
    _class = types.double._class
    
    @classmethod
    def requires(cls, df):
        req = String.requires(df)
        minimun = df.property('type', 'minimun')
        maximun = df.property('type', 'maximun')
        dot = df.property('type', 'dot') or '.'
        
        if minimun and maximun:
            req.append(validators.IS_FLOAT_IN_RANGE(minimun = minimun, maximun = maximun, dot = dot))
        elif minimun:
            req.append(validators.IS_FLOAT_IN_RANGE(minimun =  minimun, dot = dot))
        elif maximun:
            req.append(validators.IS_FLOAT_IN_RANGE(maximun = maximun, dot = dot))
        
        return req
    
class Decimal(Double):
    _class = types.decimal._class
    
class Date(String):
    _class = types.date._class
    prepend = SPAN(I(_class='icon-calendar'), _class='add-on')
    
    @classmethod
    def requires(cls, df):
        req = String.requires(df)        
        maximun = df.property('type', 'maximun')
        minimun = df.property('type', 'minimun')
        format = df.property('type', 'format')
        
        if maximun and minimun:
            req.append(validators.IS_DATE_IN_RANGE(minimun = minimun, maximun = maximun, format=format))
        elif minimun:
            req.append(validators.IS_DATE_IN_RANGE(minimun = minimun, format = format))
        elif maximun:
            req.append(validators.IS_DATE_IN_RANGE(maximun = maximun, format=format))
        else:
            req.append(validators.IS_DATE(format=format))
    
        return req
    
    @classmethod
    def control(cls, df, value, **attributes):
        
        default = {'value': value}
        
        attrs = cls._attributes(df, default, **attributes)
        attrs['_data-strftime'] = df.property('type', 'format') or get_default(types[cls._class].options, 'format') 
        
        widget = INPUT(**attrs)
        _class = 'input-prepend %s-control'%df.df_type
        return DIV(cls.prepend, widget, _class=_class)
    
class Time(Date):
    _class = types.time._class
    prepend = SPAN(I(_class='icon-time'), _class='add-on')
    
    @classmethod
    def requires(cls, df):
        req = String.requires(df)
        maximun = df.property('type', 'maximun')
        minimun = df.property('type', 'maximun')
        format = df.property('type', 'format')
        
        if maximun and minimun:
            req.append(validators.IS_DATETIME_IN_RANGE(minimun=minimun, maximun=maximun, format=format))
        elif minimun:
            req.append(validators.IS_DATETIME_IN_RANGE(minimun=minimun, format=format))
        elif maximun:
            req.append(validators.IS_DATETIME_IN_RANGE(maximun=maximun, format=format))
        else:
            req.append(validators.IS_DATETIME(format=format))
        
        return req
        
    
class Datetime(Time):
    _class = types.datetime._class
    prepend = SPAN(I(_class='icon-calendar'), _class='add-on')
    
class Currency(String):
    _class = types.currency._class
    prepend = SPAN(T('$'), _class='add-on')
    
    @classmethod
    def control(cls, df, value, **attributes):        
        symbol = df.property('type', 'symbol') or get_default(types.currency.options, 'symbol')
        decimalDigits = df.property('type', 'decimalDigits') or get_default(types.currency.options, 'decimalDigits')
        decimalSeparator = df.property('type', 'decimalSeparator') or get_default(types.currency.options, 'decimalSeparator')
        thousandDigits = df.property('type', 'thousandDigits') or get_default(types.currency.options, 'thousandDigits')
        thousandSeparator = df.property('type', 'thousandSeparator') or get_default(types.currency.options, 'thousandSeparator')
        
        attrs = cls._attributes(df, {'value': value}, **attributes)
        
        attrs['_data-fmt_symbol'] = symbol
        attrs['_data-fmt_decdig'] = decimalDigits
        attrs['_data-fmt_decsep'] = decimalSeparator
        attrs['_data-fmt_thodig'] = thousandDigits
        attrs['_data-fmt-thosep'] = thousandSeparator  
        
        widget = INPUT(**attrs)
        _class = 'input-prepend %s-control'%df.df_type
        return DIV(cls.prepend, widget, _class=_class)
    
class Url(Date):
    _class = types.email._class
    prepend = SPAN(I(_class='icon-globe'), 'add-on')
    
    @classmethod
    def requires(cls, df):
        req = String.requires(df)
        
        validate = df.property('type', 'validate')
        if validate:
            req.append(validators.IS_URL())
            
        return req
    
class Email(Date):
    _class = types.email._class
    prepend = SPAN(I(_class='icon-envelope'), _class='add-on')
    
    @classmethod
    def requires(cls, df):
        req = String.requires(df)
        validate = df.property('type', 'validate')
        if validate:
            req.append(validators.IS_EMAIL())
        return req
    
class Phone(Date):
    _class = types.phone._class
    #TODO: O Css necessita de um icone de telefone, o novo glyphicons possui
    prepend = SPAN(I(_class='icon-leaf'), _class='add-on')
    
class Text(FormWidget):
    _class = types.text._class
    
    @classmethod
    def control(cls, df, value, **attrs):
        attrs = cls._attributes(df, {'value': value}, **attrs)
        return TEXTAREA(**attrs) 
    
class Smalltext(Text):
    _class = types.smalltext._class
    
class Texteditor(Text):
    _class = types.texteditor._class
    
class Rule(Text):
    _class = types.rule._class
    
class Boolean(String):
    _class = types.boolean._class
    
class Select(FormWidget):
    _class = types.select._class
    
    @classmethod
    def requires(cls, df):
        req = []
        if not cls.isrequired(df):
            req.append(validators.IS_EMPTY_OR(validators.IS_IN_SET(cls.get_options(df))))
        else:
            req.append(validators.IS_IN_SET(cls.get_options(df)))
        return req
    
    @classmethod
    def has_options(cls, df):
        return df.df_default and len(df.df_default or [])>0

    @classmethod
    def get_options(cls, df):
        return df.df_default
        
    @classmethod
    def control(cls, df, value, **attrs):
        
        default = {"value": value, '_class':cls._class}
        attr = cls._attributes(df, default, **attrs)
        
        if cls.has_options(df):
            options = cls.get_options(df)
        else:
            raise SyntaxError, 'widget Select cannot determine options of %s'%df.df_name

        opts = [OPTION(k.values()[0], _value=k.keys()[0]) for k in options]
                
        return SELECT(*opts, **attr)
    
class MultipleSelect(Select):
    
    @classmethod
    def widget(cls, df, value, size=5, **attrs):
        
        attrs.update(_size=size, _multiple=True)
        
        return Select.widget(df, value, **attrs)

class Radio(Select):
    @classmethod
    def widget(cls, df, value, **attrs):
        
        return FormWidget(df.field, value, **attrs)
    
class Checkbox(Select):
    @classmethod
    def widget(cls, df, value, **attrs):
        return FormWidget.widget(df.field, value, **attrs)
    
class List(FormWidget):
    _class = types.list._class
    
    @classmethod
    def widget(cls, df, value, **attrs):
        return FormWidget.widget(df.field, value, **attrs)
    
class Password(String):
    _class = types.password._class
    
    @classmethod
    def widget(cls, df, value, **attrs):
        return String.widget(df.field, value, **attrs)
    
class Filelink(FormWidget):
    _class = types.filelink._class
    
    @classmethod
    def widget(cls, df, value, download_url=None, **attrs):
        return FormWidget.widget(df.field, value, download_url, **attrs)
    
    @classmethod
    def represent(cls, df, value, download_url=None):
        return FormWidget.represent(df.field, value, download_url)

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
        self.document_referenced = self.doc_field.property('type', 'document')
        
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
            req.append(validators.IS_IN_DB(self.db, 'tabDocument.id', '%(' + self.doc_field.property('type', 'label') + ')s'))
        if self.doc_field.property('type', 'document'):
            req.append(validators.IS_EMPTY_OR(validators.IS_IN_DB(self.db, 'tabDocument.id', '%(' + self.doc_field.property('type', 'label') + ')s')))            
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
            
            DOC_FIELDS = []
            
            [DOC_FIELDS.append((doc_field.df_name, doc_field.df_label or pretty(doc_field.df_name))) for doc_field in self.db(self.db.DocumentField.document==self.doc_field.document).select()]
            
            form = FORM(
                DIV(
                    SELECT(*[OPTION(y,_value=x) for x,y in self.LIST_AGGREGATIONS], _class=self.AGGREGATION, _name=self.AGGREGATION+'_0'),
                    SELECT(*[OPTION(y,_value=x) for x,y in DOC_FIELDS], _class=self.DOC_FIELD, _name=self.DOC_FIELD+'_0'),
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
        attr['_class'] = 'link-text'
        
        name = attr.pop('_name')
        value = attr['value']
        
        record = self.db.get_document(self.document_referenced, value) if value else None

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
                                           $(y).attr($('y').attr('name'), $(y).attr('class') + '_' + i);
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

class Suggest(Link):
    _class = vtypes.suggest._class
    
    def __init__(self, request, df, id_df=None, db=None, orderby=None,
                 limitby=(0,10), distinct=False,
                 keyword = '_autocomplete_%(tablename)s_%(fieldname)s',
                 min_length=2, help_fields=None, help_string=None):
        self._class = ' '.join([df.df_type, self._type])
        Link.__init__(
            request, df.field, id_df.field if id_df else None, db, orderby,
            limitby, distinct, keyword, min_length, help_fields, help_string
        )
        
    def __call__(self, df, value, **attrs):
        return Link.__call__(self, df.field, value, **attrs)

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
    property = Smalltext,
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
    icons = Storage({
        'new': I(_class='icon-plus'),
        'list': I(_class='icon-list-alt'),
        'print': I(_class='icon-print'),
        'send': I(_class='icon-envelope'),
        'delete': I(_class='icon-trash')
    })
    url_binds = Storage()
    
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
        self.db = self.document.META._db
        
        self.storage = storage.session(prefix=document.META.doc_name + '_' + (str(self.document.id) or 'new'))
        
        self.submit_button = submit_button
        self.readonly = readonly
        self.actions = actions
        
        self.init_managers()
    
    def init_managers(self):
        from helpers.manager import TagManager, CommentManager, FileManager
        
        self.manager_tag = TagManager(self.db, self.document, self.storage)
        self.manager_comment = CommentManager(self.db, self.document, self.storage)
        self.manager_file = FileManager(self.db, self.document, self.storage)
    
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
        
    def _section_break(self, widget, i):
        _type = self.document.META.DOC_FIELDS[i].df_type
        while i < len(self.document.META.DOC_FIELDS) and _type != 'sectionbreak':
            doc_field = self.document.META.DOC_FIELDS[i] 
            df_name = doc_field.df_name
            subwidget = widgets[_type].widget(self.document.META.DOC_FIELDS[i], self.document[df_name] if hasattr(self.document, df_name) else '' , row=self.document)
            if doc_field.property('policy', 'visible') == 'NEVER':
                i += 1
                continue    
            elif _type == 'columnbreak':
                subwidget, i = self._column_break(subwidget, i+1)
            widget.components.append(subwidget)
            if (i+1) >= len(self.document.META.DOC_FIELDS) or self.document.META.DOC_FIELDS[i+1].df_type == 'sectionbreak': 
                break
            else:
                i += 1
                _type = self.document.META.DOC_FIELDS[i].df_type
        return widget, i
    
    def _column_break(self, widget, i):
        _type = _type = self.document.META.DOC_FIELDS[i].df_type
        while i < len(self.document.META.DOC_FIELDS) and _type not in ('sectionbreak', 'columnbreak'):
            doc_field = self.document.META.DOC_FIELDS[i] 
            df_name = doc_field.df_name
            subwidget = widgets[_type].widget(self.document.META.DOC_FIELDS[i], self.document[df_name] if hasattr(self.document, df_name) else '', row=self.document)
            widget.components.append(subwidget)
            if doc_field.property('policy', 'visible') == 'NEVER':
                i += 1
                continue
            elif (i+1) >= len(self.document.META.DOC_FIELDS) or self.document.META.DOC_FIELDS[i+1].df_type in  ('sectionbreak', 'columnbreak') : 
                break
            else:
                i += 1
                _type = self.document.META.DOC_FIELDS[i].df_type
        return widget, i
        
    def formstyle_document(self):        
        i = 0
        element = TAG['']()
        
        while i < len(self.document.META.DOC_FIELDS):
            doc_field = self.document.META.DOC_FIELDS[i] 
            _type = doc_field.df_type
            df_name = doc_field.df_name
            wgt = widgets[_type].widget(self.document.META.DOC_FIELDS[i], self.document[df_name] if hasattr(self.document, df_name) else '', row=self.document )
            if doc_field.property('policy', 'visible') == 'NEVER':
                i += 1
                continue
            elif _type == 'sectionbreak':
                subwgt, i = self._section_break(wgt, i+1)
                i += 1
                element.components.append(subwgt)
                continue
            elif _type == 'columnbrek':
                subwgt, i = self._column_break(wgt, i+1)
                i += 1
                element.components.append(subwgt)
                continue
            else:
                element.components.append(wgt)  
            i += 1
        
        return element        
                
    def build_actions(self):
        pass
    
class DocumentPage(Document):
    def __init__(self, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
    
        self.build_page()
    
    def build_page(self):
        self.components = [
            self.build_page_header(), 
            self.build_page_content(), 
            self.buid_page_menu()
        ]
        
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
                   FORM(self.formstyle_document()).process(), 
                   DIV(_class='dialogs'),
                   current.response.toolbar(),
                   _class='page-content'
                )
                
    def buid_page_menu(self):
        
        return DIV(
            UL(
               LI(self.T('Actions'), _class='nav-header'),
               *[LI(A(self.icons[action], action.lower().capitalize(), _href=URL(vars={'action': action}))) for action in self.actions],
               _class='nav nav-tabs nav-stacked'
            ),
            self.manager_file.component,
            self.manager_tag.component,
            self.manager_comment.component,
            _class='page-menu'
        )
    
class ChildModal(Document, ChildManager):
    _form = None
    def __init__(self, 
        document,
        parent,
        submit_button = T('Save'),
        readonly = False,
        actions = ['new', 'list', 'print', 'send', 'delete'],
        **attrs
    ):
        Document.__init__(self, document, submit_button, readonly, actions, **attrs)
        ChildManager.__init__(self, self.db, self.document, parent, self.storage )
        
    def build_menu(self):
        return DIV(
            BUTTON(I(_class="icon-cog"), _class="btn pull-left", **{"_data-toggle": "dropdown"}),
            UL(
               LI(A(
                    self.T('Attachments'),
                    I(_class="icon-file"), 
                    _tabindex="-1", 
                    **{
                       '_data-animation': 'true', 
                       '_data-html': 'true', 
                       '_data-placement': 'right', 
                       '_data-trigger': 'manual', 
                       '_data-content': '#popover_file_content', 
                       '_data-title': self.T('Attachments')
                       }
                    )
                  ),
               LI(A(
                    self.T('Tags'),
                    I(_class="icon-tag"), 
                    _tabindex="-1", 
                    **{
                       '_data-animation': 'true', 
                       '_data-html': 'true', 
                       '_data-placement': 'right', 
                       '_data-trigger': 'manual', 
                       '_data-content': '#popover_tag_content', 
                       '_data-title': self.T('Tags')
                       }
                    )
                  ),
               LI(A(
                    self.T('Comments'),
                    I(_class="icon-comment"), 
                    _tabindex="-1", 
                    **{
                       '_data-animation': 'true', 
                       '_data-html': 'true', 
                       '_data-placement': 'right', 
                       '_data-trigger': 'manual', 
                       '_data-content': '#popver_comment_content', 
                       '_data-title': self.T('Comments')
                       }
                    )
                  ),
               _class="dropdown-menu",
            ),
            DIV(self.manager_file.component, _id="popover_file_content", _class='hide'),
            DIV(self.manager_tag.component, _id="popover_tag_content", _class='hide'),
            DIV(self.manager_comment.component, _id="popover_comment_content", _class='hide'),
            _class="btn-group dropup",
        )
        
    def build_modal(self):
        return DIV(
            DIV(
                H3(self.document.META.doc_title),
                _class='modal-header'
            ),
            DIV(
                _class='modal-body'
            ),
            DIV(
                self.build_menu(),
                BUTTON(self.T('Close'), _class='btn', **{'_data-dismiss': 'modal'}),
                BUTTON(self.T('Save Changes'), _class='btn btn-primary', _id="submit_%s"%self._id),
                _class='modal-footer'
            ),
            self.build_script_modal(),
            _id = self._id,
            _class="childmodal modal hide fade",
            **{'_data-backdrop': 'false'}
        )
    
    def build_script_modal(self):
        script = """;(function($){
            $('div#%(id)s').appendTo('.dialogs');
            $('#submit_%(id)s').on('click', function(){
                $('form#%(id)s').submit();
            });
        })(jQuery);"""%{
            'id': self._id,
            'name': self._name,
        }
        if self.request.ajax:
            self.response.js = (self.response.js or '') + script.strip()
            return TAG['']()
        else:
            return SCRIPT(script.strip())
    
    @property
    def form(self):
        if not self._form:
            
            self._form = FORM(self.formstyle_document(), _formname=self._name, _id=self._id, _action=URL(**self.base_url_form)).process()
        return self._form
    
    @classmethod
    def widget(cls, df, value, **attrs):
        raise NotImplementedError
    
    def script(self):
        return self.build_script()  
        
        
class ChildTable(ChildModal):
    _form = None
    _cols = None
    
    def __init__(self, *args, **kwargs):
        ChildModal.__init__(self, *args, **kwargs)
                
    @property
    def columns(self):
        if not self._cols:
            cols = self.document.META.property('type', 'columns')
            columns = []
            if not cols:
                columns = [
                           {'rel': '%s.%s'%(self.document.META.doc_tablename, df.df_name), 
                            'label': df.df_label, 'class': df.df_type,
                            'style': '' if df.property("policy", "is_readable")!="NEVER" else 'hide' } for df in self.document.META.DOC_FIELDS if df.df_type in types.keys()]
            else:
                for col in cols:
                    df = self.document.META.get_doc_field(col)
                    columns.append({'rel': df.df_name, 'label': df.df_label})
            self._cols = columns
        return self._cols
    
    def build_table_header(self):
        return THEAD(TR(*[TH(A(I(_class='icon-plus icon-white'),' ', self.T('Add'), _href='javascript:void(0)', _class='btn btn-mini btn-info', **{'_data-url': URL(**self.base_url_child_add)}))]+[TH(c['label'], _rel=c['rel'], _class=c['style']) for c in self.columns]))

    def get_representation(self, doc_field, data):
        import locale
        locale.setlocale(locale.LC_ALL, '')        
        if doc_field:
            if doc_field.df_type == 'link':
                return data
                document = self.META.property('type', 'document')
                label = self.META.property('type', 'label')
                row = self.META.db[document](data)
                if row and label in row:
                    return row[label]
            elif doc_field.df_type == 'currency':
                return locale.currency(data, doc_field.property('type', 'symbol') or get_default(types.currency.options, 'symbol'), True, False)
            elif doc_field.df_type == 'money':
                return locale.currency(data, doc_field.property('type', 'international') or get_default(types.currency.options, 'symbol'), True, True)
            elif doc_field.df_type == 'filelink':
                document = self.db.File(data)
                if document and self.document.META.property('allow_file_links'):
                    label = document['title']
                    return A(URL('download', args=document.id), cid=self.request.cid if self.request.ajax else None)
                elif document:
                    return document['title']
            elif doc_field.df_type in ('blob', 'property'):
                return 'DATA'
            elif doc_field.df_type == 'smalltext' and data and len(data)>255:
                return 'DATA'
            elif isinstance(data, (list, tuple, dict)):
                return 'DATA'
            return data
        return data
        
    def build_table_body(self):
        from gluon.dal import Row
        
        def url_edit(row):
            base = self.base_url_child_edit.copy()
            base['vars']['__saved'] = row['__saved'][0]
            base['vars']['__idx'] = row['__saved'][1] 
            return URL(**base)
        
        def url_remove(row):
            base = self.base_url_child_remove.copy()
            base['vars']['__saved'] = row['__saved'][0]
            base['vars']['__idx'] = row['__saved'][1]
            return URL(**base)
        
        records = self.list_childs()
        tbody = []
        for record in records:
            row = []
            for column in self.columns:
                (tablename, fieldname) = column['rel'].split('.')
                doc_field = self.document.META.get_doc_field(fieldname)                    
                if tablename in record \
                    and isinstance(record, Row) \
                    and isinstance(record[tablename], Row):
                    d = record[tablename][fieldname]
                elif fieldname in record:
                    d = record[fieldname]
                else:
                    raise SyntaxError, 'something wrong in Rows object'
                d = self.get_representation(doc_field,  d) if d else ''
                row.append(TD(d or '', **{'_data-saved': record['__saved'][0], '_data-idx': record['__saved'][1], '_data-columnname': column['rel'], '_class': column['style']  }))
            row.insert(0, 
                TD(
                   '%06d'%int(record.id),
                   A(I(_class='icon-edit'), **{'_data-url': url_edit(record)}),
                   A(I(_class='icon-remove'), **{'_data-url': url_edit(record)})
                )
            )
            tbody.append(TR(*row, _class='many-childs-row', **{'_data-doc_parent': record.id, }))
            
        return TBODY(*tbody)
    
    def build_table(self):
        
        def url_add():
            return ''
        
        components = [self.build_table_header(), self.build_table_body()]
        return TAG[''](
            DIV(
                DIV(
                    SPAN(
                         
                    ),
                    _class='pull-right muted'
                ),
                _class='table-head'
            ),
            DIV(
                TABLE(*components, _id=self._id, _class='table table-hover table-condensed'),
                self.build_script_table(), 
                self.build_modal(),
                _class='table-content clearfix'
            )
        )
    
    def build_script_table(self):
        from helpers import ajax_set_files
        
        files = []
        files.append(URL(c='static', f='templates', args=['bootstrap', 'third-party', 'DataTables', 'js', 'jquery.dataTables.min.js']))
        files.append(URL(c='static', f='templates', args=['bootstrap', 'third-party', 'DataTables', 'extras', 'FixedColumns.min.js']))
        ajax_set_files(files)
        
        script = """
            ;(function($){
                $('table#%(id)s thead tr th a.btn').on('click', function(){
                    $.get($(this).data('url'), function(data){
                        $('div#%(id)s .modal-body').html(data);
                            $('div#%(id)s').modal();
                    });
                });
                $('table#%(id)s tbody tr td a').each(function(i){
                    $(this).on('click', function(){
                        $.get($(this).data('url'), function(data){
                            $('div#%(id)s .modal-body').html(data);
                            $('div#%(id)s').modal();
                        });
                    });
                });
                function initTable(){
                    var oTable = $('table#%(id)s').dataTable({
                        'sScrollY': '500px',
                        'sScrollX': '100%%25',
                        'sScrollXInner': '150%%25',
                        'bScrollCollapse': true,
                        'bPaginate': false,
                        'bFilter': false,
                        'oLanguage': {
                            'sInfo': '',
                            'sInfoFiltered': ''
                        },
                        'aoColumnDefs': [
                            {'bSortable': false, 'sClass': 'index', 'aTargets': [0]}
                        ],
                        'aaSorting': [[0, 'asc']]
                    });
                }
                
                if ($('table#%(id)s').dataTable === undefined) {
                    setTimeout(initTable, 1500);
                } else {
                    initTable();
                }
                                
            })(jQuery);
        """%{'id': self._id}
        if self.request.ajax:
            self.response.js = (self.response.js or '') + script
            return TAG['']()
        return SCRIPT(script)

    @classmethod
    def widget(cls, df, value, **attrs):
        db = df.PARENT._db
        document = db.get_document(df.property('type', 'document'))
        widget = ChildTable(document, attrs.pop('row'))
        return widget.component
            
widgets.childtable = ChildTable