// Copyright (c) 2012 Maxwell Morais [max.morais.dmm@gmail.com]
// 
// MIT License (MIT)
// 
// Permission is hereby granted, free of charge, to any person obtaining a 
// copy of this software and associated documentation files (the "Software"), 
// to deal in the Software without restriction, including without limitation 
// the rights to use, copy, modify, merge, publish, distribute, sublicense, 
// and/or sell copies of the Software, and to permit persons to whom the 
// Software is furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in 
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
// INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
// PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
// CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
// OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//

mgk.$import('mgk.model');
mgk.provide('mgk.doctype');

mgk.doctype.policy = {
	u: 'Unique',
	n: 'Required (not allow null)',
	r: 'Readable (is showed in form)',
	w: 'Writable',
};

var option = function(name, label, dft, type){ return Field(name, type, {'label': label, 'default': deft, });

mgk.doctype.types = new Class.$extend({
	__init__: function(){
	    this.string = {
	    	'native': 'string'
	    };
		this.text = {
			'native': 'string'
		};
		this.blob = {
			'native': 'string'
		};
		this.integer = {
			'native': 'integer'
		};
		this.double = {
			'native': 'float'
		};
		this.password = {
			'native': 'string'
		};
		this.boolena = {
			'native': 'boolean'
		};
	},
	decimal:{
		'native': 'float',
		'data-options': [
		     option('n', 'Digits', 10, 'integer' ),
		     option('m', 'Decimal Places', 2, 'integer' ),
		 ]
	},
	currency:{
		'native': 'float',
		'data-options': [
		     option('symbol', 'Symbol', '$', 'string'),
		     option('international', 'International', 'USD', 'string'),
		     option('decimal_digits', 'Decimal Digits', 2, 'integer' ),
		     option('decimal_separator', 'Decimal Separator', '.', 'string'),
		     option('thousand_digits', 'Thousand Digits', 3, 'integer'),
		     option('thousand_separator', 'Thousand Separator', '.'),
		 ]
	},
	date:{
		'native': 'date',
		'data-options': [
		     option('strftime', 'Format', '%Y-%m-%d', 'string'),
		]
	},
	time:{
		'native': 'time',
		'data-options': [
		     option('strftime', 'Format', '%H:%M:%S', 'string'),
		]
	},
	datetime:{
		'native': 'datetime',
		'data-options': [
		     option('strftime', 'Format', '%Y-%M-%d %H:%M:%S', 'string'),
		]
	},
	upload:{
		'native': 'text',
		'data-options': [
		     option('uploadfield', 'Field', null, 'string'),
		     option('uploadfolder', 'Folder', null, 'upload:raw'),
		     option('uploadseparated', 'Separated?', true, 'boolean'),
		     option('uploadfs', 'Diferenced File System', null, 'string')
		]
	},
	link:{
		'native': 'integer',
		'data-options': [
		     option('options', 'Options', null, 'string'),
		     option('with_doctype', 'With', null, 'string'),
		     option('doctype', 'DocType', null, 'link:mgk.model.Manager.listDoctypes();'),
		     option('docfield', 'DocField', null, 'link:mgk.model.Manager.get(this).listDocFields();'),
		     option('label', 'Label', '%(id)s', 'string')
		     
		]
	}
})();

mgk.model.doctype.DocField = Class.$extend({
	__init__: function(name, type, options){
					
	}
});


